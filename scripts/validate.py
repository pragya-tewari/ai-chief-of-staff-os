#!/usr/bin/env python3
"""Dependency-free structural validation for AI Chief of Staff OS."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []
SPEC_VERSION = "0.1"

CAPABILITIES = {
    "task.read", "task.create", "task.update", "task.assign",
    "calendar.read", "sheet.read", "sheet.write", "chat.read", "chat.send",
    "mail.read", "mail.send", "meeting.read", "doc.read", "doc.create",
}
APPROVALS = {
    "external-write", "tell-a-person", "decision-record", "private-write",
    "rule-change", "sensitive-read", "sheet-write",
}
ENTITY_TYPES = {"profile", "person", "project", "org", "meeting", "decision"}
ENTITY_STATUSES = {"active", "planning", "dormant", "closed"}
CONFIDENCE = {"confirmed", "inferred", "unconfirmed"}
TASK_TYPES = {"commitment", "follow-up", "waiting", "decision-action"}
TASK_STATUSES = {"todo", "doing", "blocked", "waiting-on", "done", "cancelled"}
ROLES = {"task", "chat", "mail", "docs", "sheets", "calendar", "meetings"}
RUN_STATUSES = {"planned", "in-progress", "needs-verification", "blocked", "complete"}
ACTION_STATES = {"planned", "in-progress", "succeeded", "failed", "uncertain", "skipped"}
EXPECTED_DEDUP_KEYS = {
    "capacity-and-headcount": "as-of-date+scope",
    "draft-a-message": "recipient+purpose+source-id",
    "goals-and-numbers": "goal-quarter+mode+period",
    "intake-a-request": "request-id",
    "manage-a-decision": "decision-id+mode",
    "meeting-to-tasks": "meeting-source-id",
    "people-moves": "person-move-id",
    "post-mortem": "incident-id",
    "prepare-a-meeting": "meeting-id-or-person+meeting-date+mode",
    "protect-the-calendar": "calendar-scope+date-range",
    "review-the-system": "review-period",
    "run-a-sweep": "sweep-period+mode",
    "spend-check": "source+reporting-period+mode",
    "write-an-update": "audience+reporting-period",
}
PERIODIC_RECOVERY_JOBS = {
    "capacity-and-headcount", "draft-a-message", "prepare-a-meeting",
    "protect-the-calendar", "review-the-system", "run-a-sweep",
    "spend-check", "write-an-update",
}


def fail(message: str) -> None:
    ERRORS.append(message)


def _real_date(value: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def scalar(value: str):
    value = value.strip()
    if value in {"[]", ""}:
        return [] if value == "[]" else ""
    if value == "true":
        return True
    if value == "false":
        return False
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value.split(" #", 1)[0].strip()


def frontmatter(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        fail(f"unclosed frontmatter: {path.relative_to(ROOT)}")
        return {}
    result: dict = {}
    current = None
    for number, line in enumerate(lines[1:end], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"^\s+-\s+(.+?)\s*$", line)
        if item:
            if current is None or not isinstance(result.get(current), list):
                fail(f"orphan YAML list item: {path.relative_to(ROOT)}:{number}")
            else:
                result[current].append(scalar(item.group(1)))
            continue
        field = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not field:
            fail(f"unsupported frontmatter syntax: {path.relative_to(ROOT)}:{number}")
            continue
        current, value = field.group(1), field.group(2) or ""
        result[current] = [] if not value.strip() else scalar(value)
    return result


def yaml_field(path: Path, key: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*['\"]?([^'\"#]+)")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    return ""


def validate_versions() -> None:
    spec_text = (ROOT / "SPEC-VERSION.md").read_text(encoding="utf-8")
    if f"`{SPEC_VERSION}`" not in spec_text:
        fail("SPEC-VERSION.md does not declare the supported version")
    expected = {
        ROOT / "cos-os.yaml.example": ("spec_version", SPEC_VERSION),
        ROOT / "setup/workspace-template/cos-workspace.yaml": ("workspace_version", SPEC_VERSION),
        ROOT / "example-company/cos-workspace.yaml": ("workspace_version", SPEC_VERSION),
    }
    for path, (key, value) in expected.items():
        if yaml_field(path, key) != value:
            fail(f"version mismatch in {path.relative_to(ROOT)}: expected {key} {value}")


def validate_links() -> tuple[int, set[Path]]:
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    count = 0
    targets: set[Path] = set()
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        # an --inside workspace is the user's private data; never scan it
        if path.relative_to(ROOT).parts[0] == "workspace":
            continue
        text = path.read_text(encoding="utf-8")
        for raw in pattern.findall(text):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            count += 1
            resolved = (path.parent / target).resolve()
            targets.add(resolved)
            if not resolved.exists():
                fail(f"broken link: {path.relative_to(ROOT)} -> {target}")
    return count, targets


def validate_jobs() -> None:
    required_files = {
        "manifest.md", "when-to-run.md", "how-to-do-it.md",
        "where-things-go.md", "example.md", "test.md",
    }
    required_fields = {
        "job", "spec-version", "reads", "writes-internal",
        "external-capabilities", "approval-actions", "dedup-key",
        "supports-dry-run",
    }
    job_dirs = sorted(p for p in (ROOT / "jobs").iterdir() if p.is_dir())
    if len(job_dirs) != 14:
        fail(f"expected 14 job directories, found {len(job_dirs)}")
    for directory in job_dirs:
        for name in required_files:
            path = directory / name
            if not path.is_file() or path.stat().st_size == 0:
                fail(f"missing job file: {path.relative_to(ROOT)}")
        manifest = frontmatter(directory / "manifest.md")
        missing = required_fields - manifest.keys()
        if missing:
            fail(f"{directory.name} manifest missing: {', '.join(sorted(missing))}")
        if manifest.get("job") != directory.name:
            fail(f"manifest job mismatch: {directory.name} != {manifest.get('job')}")
        if manifest.get("spec-version") != SPEC_VERSION:
            fail(f"unsupported manifest spec version: {directory.name}")
        if manifest.get("supports-dry-run") is not True:
            fail(f"dry-run must be true: {directory.name}")
        internal_writes = manifest.get("writes-internal", [])
        for runtime_destination in ("log/activity.md", "log/runs/"):
            if runtime_destination not in internal_writes:
                fail(
                    f"{directory.name} manifest omits runtime write "
                    f"{runtime_destination}"
                )
        dedup_key = str(manifest.get("dedup-key", "")).strip()
        if not dedup_key or dedup_key == "none":
            fail(f"job must declare a concrete dedup-key: {directory.name}")
        elif dedup_key != EXPECTED_DEDUP_KEYS.get(directory.name):
            fail(f"unexpected dedup-key for {directory.name}: {dedup_key}")
        if directory.name in PERIODIC_RECOVERY_JOBS:
            method = (directory / "how-to-do-it.md").read_text(encoding="utf-8")
            test = (directory / "test.md").read_text(encoding="utf-8")
            if "## Run identity" not in method:
                fail(f"periodic/unkeyed job lacks run-identity method: {directory.name}")
            if "Rerun" not in test:
                fail(f"periodic/unkeyed job lacks rerun invariant: {directory.name}")
        for capability in manifest.get("external-capabilities", []):
            if capability not in CAPABILITIES:
                fail(f"unknown capability in {directory.name}: {capability}")
        for approval in manifest.get("approval-actions", []):
            if approval not in APPROVALS:
                fail(f"unknown approval action in {directory.name}: {approval}")


def validate_connections() -> None:
    for path in sorted((ROOT / "connections").glob("*.md")):
        data = frontmatter(path)
        if not data:
            continue
        declared_roles = data.get("roles")
        if declared_roles is None:
            declared_roles = [data.get("role")]
        if not isinstance(declared_roles, list) or not declared_roles or any(
            r not in ROLES for r in declared_roles
        ):
            fail(f"invalid connection role(s): {path.relative_to(ROOT)}")
        provided = data.get("provides")
        if not isinstance(provided, list) or not provided:
            fail(f"connection provides list missing: {path.relative_to(ROOT)}")
            continue
        for capability in provided:
            if capability not in CAPABILITIES:
                fail(f"unknown connection capability in {path.name}: {capability}")


def validate_entities_and_tasks() -> None:
    sample = ROOT / "example-company"
    entity_patterns = [
        "people/*.md", "projects/*/index.md", "meetings/*.md",
        "decisions/*.md", "profile/about-me.md",
    ]
    entities: dict[str, tuple[Path, dict]] = {}
    for pattern in entity_patterns:
        for path in sample.glob(pattern):
            data = frontmatter(path)
            if not data:
                continue
            required = {"type", "id", "name", "status", "last-confirmed", "review-by", "confidence"}
            missing = required - data.keys()
            if missing:
                fail(f"entity missing fields {sorted(missing)}: {path.relative_to(ROOT)}")
                continue
            if data["type"] not in ENTITY_TYPES:
                fail(f"invalid entity type {data['type']}: {path.relative_to(ROOT)}")
            if data["status"] not in ENTITY_STATUSES:
                fail(f"invalid entity status {data['status']}: {path.relative_to(ROOT)}")
            if data["confidence"] not in CONFIDENCE:
                fail(f"invalid confidence {data['confidence']}: {path.relative_to(ROOT)}")
            if not _real_date(str(data["last-confirmed"])):
                fail(f"invalid last-confirmed date: {path.relative_to(ROOT)}")
            review = str(data["review-by"])
            if review != "never" and not _real_date(review):
                fail(f"invalid review-by value: {path.relative_to(ROOT)}")
            if data["id"] in entities:
                fail(f"duplicate entity id {data['id']}: {path.relative_to(ROOT)}")
            entities[data["id"]] = (path, data)

    people = {key for key, (_, data) in entities.items() if data["type"] == "person"}
    projects = {key for key, (_, data) in entities.items() if data["type"] == "project"}
    meeting_ids = set()
    register = sample / "registers/meetings.md"
    for line in register.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*(M\d+)\s*\|", line)
        if match:
            meeting_ids.add(match.group(1))

    task_ids: set[str] = set()
    for path in (sample / "tasks.md", sample / "tasks-done.md"):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not re.match(r"^\|\s*T\d+\s*\|", line):
                continue
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(columns) != 9:
                fail(f"task row must have nine fields: {path.relative_to(ROOT)}:{number}")
                continue
            task_id, task, kind, owner, project, due, status, waiting, source = columns
            if task_id in task_ids:
                fail(f"duplicate task id: {task_id}")
            task_ids.add(task_id)
            if kind not in TASK_TYPES:
                fail(f"invalid task type {kind}: {task_id}")
            if status not in TASK_STATUSES:
                fail(f"invalid task status {status}: {task_id}")
            if owner != "me" and owner not in people:
                fail(f"unknown task owner {owner}: {task_id}")
            if project not in {"", "—"} and project not in projects:
                fail(f"unknown task project {project}: {task_id}")
            if due not in {"", "—"} and not _real_date(due):
                fail(f"invalid task due date {due}: {task_id}")
            if (
                source != "user"
                and source not in meeting_ids
                and not re.fullmatch(r"[a-z][a-z0-9-]{2,}", source)
            ):
                fail(f"unknown task source {source}: {task_id}")

    expected_open = {"T14", "T15", "T16", "T18", "T19", "T20", "T21", "T22"}
    if not expected_open.issubset(task_ids):
        fail(f"sample task set missing: {sorted(expected_open - task_ids)}")


def validate_sample(targets: set[Path]) -> None:
    sample = ROOT / "example-company"
    required_workspace = {
        "README.md", "cos-workspace.yaml", "connections.md", "task-source.md",
        "tasks.md", "tasks-done.md", "now.md", "profile/about-me.md",
        "profile/overrides.md", "log/activity.md", "log/corrections.md",
        "log/runs/README.md", "meetings/README.md", "private/README.md",
    }
    for name in required_workspace:
        if not (sample / name).is_file():
            fail(f"sample workspace missing required file: {name}")
    def hidden(path):
        return any(part.startswith(".") for part in path.relative_to(sample).parts)

    for directory in [sample] + sorted(p for p in sample.rglob("*") if p.is_dir() and not hidden(p)):
        if not any(child.is_file() and not hidden(child) for child in directory.iterdir()):
            continue
        if directory == sample:
            index = directory / "README.md"
        else:
            index = directory / "README.md"
            if not index.exists():
                index = directory / "index.md"
        if not index.exists():
            fail(f"sample folder has no README/index: {directory.relative_to(ROOT)}")

    for path in sample.rglob("*"):
        if not path.is_file() or hidden(path) or path.name in {"README.md", "index.md"}:
            continue
        if path.resolve() not in targets:
            fail(f"sample file is not linked from an index: {path.relative_to(ROOT)}")

    # The exact-string checks below are deliberate tripwires, not incidental
    # pattern matches: each pins a worked example to the sample fixture it
    # describes. If you reword one of those examples, update its tripwire here
    # in the same change — the pair drifting apart is exactly what they catch.
    tasks = (sample / "tasks.md").read_text(encoding="utf-8")
    people_example = (ROOT / "jobs/people-moves/example.md").read_text(encoding="utf-8")
    if not re.search(r"\| T20 .*\| per-vikram \| prj-rollout \| — \| doing \|", tasks):
        fail("T20 must be owned by per-vikram and undated before the demo")
    if "Reassigning T20 from Vikram to Ravi" not in people_example:
        fail("people-moves example must reassign T20 from Vikram")
    calendar_example = (ROOT / "jobs/protect-the-calendar/example.md").read_text(encoding="utf-8")
    if "~1 hour a week" not in calendar_example or "4–5 hours a month" not in calendar_example:
        fail("calendar example recovery calculation is missing or inconsistent")
    prep = (ROOT / "jobs/prepare-a-meeting/example.md").read_text(encoding="utf-8")
    if "one-to-one first" in prep:
        fail("prepare-a-meeting example leaks a private observation")
    for identifier in ("T23", "T24", "Q8", "U4", "M4"):
        for path in sample.rglob("*.md"):
            if path.name == "EXPECTED-STATE.md":
                continue
            if identifier in path.read_text(encoding="utf-8"):
                fail(f"demo output {identifier} is pre-present in {path.relative_to(ROOT)}")

    meeting_example = (ROOT / "jobs/meeting-to-tasks/example.md").read_text(encoding="utf-8")
    if "T20" not in meeting_example or "recorded-but-now-stale" not in meeting_example:
        fail("meeting-to-tasks example must reconcile the existing undated T20")

    for path in (
        ROOT / "CLAUDE.md", ROOT / "AGENTS.md", ROOT / "adapters/generic-prompt.md",
    ):
        if "90 days" in path.read_text(encoding="utf-8"):
            fail(f"profile review period contradicts the 30-day schema: {path.relative_to(ROOT)}")

    for path in (
        ROOT / "adapters/claude.md", ROOT / "adapters/agents.md",
        ROOT / "adapters/generic-prompt.md",
    ):
        if "demo" not in path.read_text(encoding="utf-8").lower():
            fail(f"adapter lacks isolated demo handling: {path.relative_to(ROOT)}")

    demo_script = (ROOT / "setup/demo.sh").read_text(encoding="utf-8")
    if "generic-demo-bundle.md" not in demo_script:
        fail("demo.sh must create a bundle for paste-in assistants")


def validate_run_receipts() -> None:
    recovery_test = ROOT / "schemas/run-receipt-test.md"
    if not recovery_test.is_file():
        fail("run-receipt recovery acceptance test is missing")
    else:
        recovery_text = recovery_test.read_text(encoding="utf-8")
        required_scenarios = {
            "## Scenario 1: a completed local action is not duplicated",
            "## Scenario 2: a failed local action is retried selectively",
            "## Scenario 3: an interrupted external action is verified before retry",
            "## Concurrency boundary",
        }
        for heading in required_scenarios:
            if heading not in recovery_text:
                fail(f"run-receipt recovery test lacks: {heading}")
        if "Do not send" not in recovery_text:
            fail("interrupted external-action test must forbid an ambiguous resend")

    receipt_schema = (ROOT / "schemas/run-receipt.md").read_text(encoding="utf-8")
    for contract in ("Normalize each component separately", "--attempt-2", "not execution order"):
        if contract not in receipt_schema:
            fail(f"run-receipt schema lacks stable-key contract: {contract}")

    receipts = sorted((ROOT / "example-company/log/runs").glob("*.md"))
    receipts = [path for path in receipts if path.name != "README.md"]
    if len(receipts) != 3:
        fail(f"expected three sample run receipts, found {len(receipts)}")
    seen: set[str] = set()
    required = {"run-key", "job", "status", "started", "updated", "source-or-scope"}
    jobs = {path.parent.name for path in (ROOT / "jobs").glob("*/manifest.md")}
    runs_index = (ROOT / "example-company/log/runs/README.md").read_text(encoding="utf-8")
    activity = (ROOT / "example-company/log/activity.md").read_text(encoding="utf-8")
    for path in receipts:
        data = frontmatter(path)
        missing = required - data.keys()
        if missing:
            fail(f"run receipt missing fields {sorted(missing)}: {path.relative_to(ROOT)}")
            continue
        if data["run-key"] in seen:
            fail(f"duplicate sample run-key: {data['run-key']}")
        seen.add(data["run-key"])
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*(?:--[a-z0-9]+(?:-[a-z0-9]+)*)+", str(data["run-key"])):
            fail(f"run-key is not canonically normalized: {path.relative_to(ROOT)}")
        if path.stem != data["run-key"]:
            fail(f"receipt filename does not match run-key: {path.relative_to(ROOT)}")
        if path.name not in runs_index:
            fail(f"receipt is not linked from its run index: {path.relative_to(ROOT)}")
        if data["job"] not in jobs:
            fail(f"receipt names unknown job {data['job']}: {path.relative_to(ROOT)}")
        if not re.search(rf"^\|\s*\d{{4}}-\d{{2}}-\d{{2}}\s*\|\s*{re.escape(str(data['job']))}\s*\|", activity, re.MULTILINE):
            fail(f"receipt job has no sample activity row: {path.relative_to(ROOT)}")
        if data["status"] not in RUN_STATUSES:
            fail(f"invalid receipt status {data['status']}: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        if "| action-key | destination | approval | state |" not in text:
            fail(f"receipt is missing the action checkpoint table: {path.relative_to(ROOT)}")
        action_count = 0
        action_keys: set[str] = set()
        action_states: list[str] = []
        for line in text.splitlines():
            if not line.startswith("|"):
                continue
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(columns) != 5 or columns[0] in {"action-key", "---"}:
                continue
            action_count += 1
            action_key, destination, approval, state, _ = columns
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", action_key):
                fail(f"action-key is not canonically normalized: {path.relative_to(ROOT)}")
            if action_key in action_keys:
                fail(f"duplicate action-key {action_key}: {path.relative_to(ROOT)}")
            action_keys.add(action_key)
            if not destination:
                fail(f"action has an empty destination: {path.relative_to(ROOT)}")
            if approval not in {"free", "yes"}:
                fail(f"invalid action approval {approval}: {path.relative_to(ROOT)}")
            action_states.append(state)
            if state not in ACTION_STATES:
                fail(f"invalid action state {state}: {path.relative_to(ROOT)}")
        if action_count == 0:
            fail(f"receipt contains no checkpointed actions: {path.relative_to(ROOT)}")
        if data["status"] == "complete" and any(
            state not in {"succeeded", "skipped"} for state in action_states
        ):
            fail(f"complete receipt contains unfinished/failed action: {path.relative_to(ROOT)}")


def validate_workspace_template() -> None:
    template = ROOT / "setup/workspace-template"
    required = {
        "README.md", "cos-workspace.yaml", "connections.md", "task-source.md",
        "tasks.md", "tasks-done.md", "now.md", "profile/overrides.md",
        "log/activity.md", "log/corrections.md", "log/runs/README.md",
        "meetings/README.md", "private/README.md",
    }
    for name in required:
        if not (template / name).exists():
            fail(f"workspace template missing: {name}")
    if not (ROOT / "rules/about-me.template.md").exists():
        fail("profile source template is missing: rules/about-me.template.md")
    else:
        profile = frontmatter(ROOT / "rules/about-me.template.md")
        required_profile = {
            "type", "id", "name", "status", "last-confirmed", "review-by", "confidence",
        }
        missing_profile = required_profile - profile.keys()
        if missing_profile:
            fail(f"profile template missing fields: {sorted(missing_profile)}")
        if profile.get("type") != "profile" or profile.get("id") != "profile-me":
            fail("profile template type/id is inconsistent")
    text = "\n".join(path.read_text(encoding="utf-8") for path in template.rglob("*.md"))
    if "Written once, never edited" in text or "not edited later" in text:
        fail("workspace template still treats derived meeting notes as immutable")
    overrides = (template / "profile/overrides.md").read_text(encoding="utf-8")
    if overrides.startswith("---") or "type: profile" in overrides:
        fail("profile/overrides.md must be an operational rule file, not a profile entity")

    private_notes = (ROOT / "example-company/private/people-notes.md").read_text(encoding="utf-8")
    if private_notes.startswith("---") or "type: profile" in private_notes:
        fail("private people-notes collection must not masquerade as a profile entity")

    entity_schema = (ROOT / "schemas/entity-header.md").read_text(encoding="utf-8")
    if "evidence, frozen" in entity_schema:
        fail("entity schema still treats correctable meeting notes as frozen evidence")


def main() -> int:
    links, targets = validate_links()
    validate_versions()
    validate_jobs()
    validate_connections()
    validate_entities_and_tasks()
    validate_sample(targets)
    validate_run_receipts()
    validate_workspace_template()
    if ERRORS:
        for error in ERRORS:
            print(f"  FAIL {error}")
        print(f"\nSTRUCTURAL CHECKS FAILED ({len(ERRORS)} error(s))")
        return 1
    print(f"  ok   {links} internal links resolve")
    print(f"  ok   product, workspace, sample and job versions agree ({SPEC_VERSION})")
    print("  ok   14 job manifests and required files are valid")
    print("  ok   connection capabilities are valid")
    print("  ok   entity headers, IDs and task references are valid")
    print("  ok   sample indexes, fixtures and demo freshness are valid")
    print("  ok   sample run receipts and lightweight rerun contract are valid")
    print("  ok   workspace template contract is consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
