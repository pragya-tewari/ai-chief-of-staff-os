#!/usr/bin/env python3
"""Read-only workspace checks. Exit 0: completed; 1: strict findings; 2: incomplete.
Without --strict, findings are reported but exit 0. No repairs are performed.
Folder READMEs and the known root operational notes are navigation entry points.
Reports and logs are excluded from orphan checks; private contents are never read.
Symlinks and nested repositories are reported and not traversed. This is a local
diagnostic, not protection against another process changing files during a scan.
"""
import argparse
import collections
import datetime
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

PRODUCT = Path(__file__).resolve().parent.parent
SKIP = {".git", ".obsidian", ".cache", "node_modules", "private"}
ROOT_ENTRIES = {"README.md", "now.md", "tasks.md", "tasks-done.md",
                "task-source.md", "connections.md"}
EXEMPT = {"reports", "log"}
SCALAR = re.compile(r"""^\s*(?:"([^"]*)"|'([^']*)'|([^#]*?))\s*(?:#.*)?$""")
WIKI = re.compile(r"\[\[([^\]]+)\]\]")
MD = re.compile(r"""\[[^\]]*\]\(\s*(?:<([^>]+)>|((?:[^\s()]|\([^()]*\))+))(?:\s+(?:"[^"]*"|'[^']*'))?\s*\)""")

def scalar(value):
    m = SCALAR.fullmatch(value.strip())
    if not m:
        raise ValueError("unsupported scalar format")
    return next(g for g in m.groups() if g is not None).strip()

def workspace(explicit):
    if explicit:
        return Path(explicit).expanduser().absolute()
    cfg = PRODUCT / "cos-os.yaml"
    if cfg.exists():
        for line in cfg.read_text(encoding="utf-8").splitlines():
            if line.startswith("workspace_path:"):
                value = scalar(line.split(":", 1)[1])
                if not value:
                    raise ValueError("workspace_path is empty")
                p = Path(value).expanduser()
                if not p.is_absolute():
                    raise ValueError("workspace_path must be absolute")
                return p
        raise ValueError("workspace_path is missing")
    p = PRODUCT / "workspace"
    if p.is_dir():
        return p
    raise ValueError("No workspace found; pass --workspace PATH")

def scan(root, today):
    findings = collections.defaultdict(list)
    errors = []
    notes = {}
    present = set()
    blocked = set()
    def walk_error(error):
        errors.append("directory could not be read: " + str(error.filename))
    for directory, dirs, names in os.walk(root, onerror=walk_error, followlinks=False):
        rel_dir = Path(directory).relative_to(root).as_posix()
        if rel_dir != "." and ".git" in dirs + names:
            findings["nested repos"].append(rel_dir)
            blocked.add(rel_dir)
            dirs[:] = []
            continue
        for name in list(dirs):
            p = Path(directory) / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                findings["skipped symlinks"].append(rel)
                blocked.add(rel)
                dirs.remove(name)
            elif name in SKIP:
                dirs.remove(name)
        for name in names:
            p = Path(directory) / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                findings["skipped symlinks"].append(rel)
                blocked.add(rel)
                continue
            present.add(rel)
            if p.suffix.lower() == ".md":
                try:
                    # Reject symlink replacement between enumeration and open.
                    fd = os.open(p, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
                    with os.fdopen(fd, encoding="utf-8") as stream:
                        notes[rel] = stream.read()
                except (OSError, UnicodeError):
                    errors.append("note could not be read: " + rel)
    by_name = collections.defaultdict(list)
    for rel in present:
        by_name[Path(rel).name].append(rel)
        if rel.endswith(".md"):
            by_name[Path(rel).stem].append(rel)
    edges = collections.defaultdict(set)
    incoming = collections.defaultdict(set)

    def candidate(base, target, wiki):
        path = os.path.normpath(str(Path(base) / target)).replace(os.sep, "/")
        if path == ".." or path.startswith("../") or Path(path).is_absolute():
            return "outside", None
        parts = Path(path).parts
        if any(part in SKIP for part in parts):
            return "excluded", None
        if any(path == b or path.startswith(b + "/") for b in blocked):
            return "excluded", None
        options = [path]
        if wiki and not Path(path).suffix:
            options.append(path + ".md")
        options.append(path.rstrip("/") + "/README.md")
        for option in options:
            if option in present:
                return "found", option
        return "missing", None

    for rel, raw in notes.items():
        body = re.sub(r"(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$", "", raw)
        body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        body = re.sub(r"`[^`]*`", "", body)
        links = [(m.group(1).split("|", 1)[0], True) for m in WIKI.finditer(body)]
        links += [(m.group(1) or m.group(2), False) for m in MD.finditer(body)]
        for target, wiki in links:
            if not target or target.startswith("#") or re.match(r"^[a-zA-Z][\w+.-]*:", target):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            status, dest = candidate(Path(rel).parent, target, wiki)
            if wiki and status == "missing" and not target.startswith("."):
                status, dest = candidate(".", target, True)
                if status == "missing" and "/" not in target:
                    matches = sorted(set(by_name.get(target, [])))
                    if len(matches) == 1:
                        status, dest = "found", matches[0]
                    elif len(matches) > 1:
                        status = "ambiguous"
            if status == "found" and dest in notes:
                edges[rel].add(dest)
                incoming[dest].add(rel)
            elif status in {"missing", "ambiguous", "outside"}:
                findings["broken or ambiguous links"].append(rel + " -> " + target + " (" + status + ")")
            # Excluded targets are not classified as broken or read for existence.

        fm = re.match(r"\A---\n(.*?)\n---", raw, re.S)
        if fm:
            match = re.search(r"^review-by:\s*(.*)$", fm.group(1), re.M)
            if match:
                try:
                    value = scalar(match.group(1))
                    if value == "never" or value.startswith("<"):
                        continue
                    due = datetime.date.fromisoformat(value)
                    if due < today:
                        findings["stale"].append(rel + " (review-by " + value + ")")
                except ValueError:
                    findings["invalid review dates"].append(rel)

    entries = {r for r in notes if r in ROOT_ENTRIES or Path(r).name == "README.md"}
    reached = set(entries)
    queue = list(entries)
    while queue:
        for target in edges[queue.pop()]:
            if target not in reached:
                reached.add(target)
                queue.append(target)
    for rel in sorted(notes):
        if rel in entries or Path(rel).parts[0] in EXEMPT:
            continue
        if not incoming[rel] and not edges[rel]:
            findings["isolated"].append(rel)
        elif not incoming[rel]:
            findings["dead ends"].append(rel)
        if rel not in reached:
            findings["unreachable"].append(rel)

    git_state = "unavailable"
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=10)
        if top.returncode:
            if "not a git repository" in top.stderr.lower() and not (root / ".git").exists():
                git_state = "n/a (no workspace repository)"
            else:
                errors.append("Git repository detection failed")
        elif Path(top.stdout.strip()).resolve() != root.resolve():
            git_state = "n/a (workspace is not its own repository)"
        else:
            st = subprocess.run(["git", "-C", str(root), "status", "--porcelain=v1", "-z",
                                 "--untracked-files=all"], capture_output=True, timeout=20)
            if st.returncode:
                errors.append("Git status failed")
            else:
                records = st.stdout.decode("utf-8", errors="replace").split("\0")
                i = 0
                while i < len(records):
                    record = records[i]
                    i += 1
                    if not record:
                        continue
                    code, path = record[:2], record[3:]
                    # A rename/copy has one additional NUL-delimited source name.
                    if "R" in code or "C" in code:
                        i += 1
                    if "private" in Path(path).parts:
                        path = "[private path withheld]"
                    findings["uncommitted"].append(code + " " + path)
                git_state = str(len(findings["uncommitted"]))
    except (OSError, subprocess.SubprocessError):
        errors.append("Git check could not complete")
    return notes, edges, findings, errors, git_state

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workspace")
    ap.add_argument("--as-of", type=datetime.date.fromisoformat, default=datetime.date.today())
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    try:
        root = workspace(args.workspace)
        if root.is_symlink() or not root.is_dir():
            raise ValueError("workspace must be an existing, non-symlink directory")
        notes, edges, findings, errors, git_state = scan(root, args.as_of)
    except (OSError, ValueError) as exc:
        print("INCOMPLETE: " + str(exc), file=sys.stderr)
        return 2
    print("Workspace health check — " + str(args.as_of))
    print("Workspace: " + str(root))
    print("Notes: " + str(len(notes)) + " · links: " + str(sum(map(len, edges.values()))) +
          " · uncommitted: " + git_state)
    for category in ("broken or ambiguous links", "isolated", "dead ends", "unreachable",
                     "stale", "invalid review dates", "nested repos", "skipped symlinks"):
        print(category + ": " + str(len(findings[category])))
    for category, items in findings.items():
        if items:
            print("\n" + category + ":")
            for item in items:
                print("  " + repr(item))
    if errors:
        print("\nINCOMPLETE: " + "; ".join(errors))
    elif any(findings.values()):
        print("\nFindings require review.")
    else:
        print("\nClean: all applicable checks completed without findings.")
    print("Read-only. Private and ignored folders are excluded; their links are not verified. "
          "Unreachable means no path from folder READMEs or root entry notes. "
          "Uncommitted work lacks a local Git snapshot; backup status is not checked.")
    return 2 if errors else (1 if args.strict and any(findings.values()) else 0)

if __name__ == "__main__":
    sys.exit(main())
