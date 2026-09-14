#!/usr/bin/env python3
"""Workspace health check — READ-ONLY.

The mechanical half of `jobs/review-the-system`. It looks at your private
workspace and prints the signals a person can't see by opening files one at a
time. It changes nothing.

Run from the product folder:
    python3 scripts/health-check.py                 # workspace from cos-os.yaml
    python3 scripts/health-check.py --workspace /path/to/workspace

What it reports:
  1. Broken links — a Markdown or [[wiki]] link whose target file doesn't exist.
  2. Isolated notes — files with no links in or out. Nothing can reach them.
  3. Dead ends — files that link out but nothing links to. Reachable only by
     search, invisible to anyone navigating from the folder READMEs.
  4. Stale entities — files whose `review-by` date has passed.
  5. Nested git repositories — a folder with its own .git inside the workspace.
     One tree, one repo: a nested repo is invisible to your backup and shows up
     as a pile of orphans in any graph view.
  6. Uncommitted work — files git has not recorded yet (only if the workspace is
     a git repository). A finished file that was never committed is not backed
     up, and later session closes may keep stepping around it. This is the check
     that catches work that ended without an ending.

Deliberately excluded from the orphan checks: `reports/` (disposable views),
`log/runs/` (receipts), and `private/` (never scanned).
"""
import argparse
import collections
import datetime
import os
import re
import subprocess
import sys

HERE = os.path.abspath(os.path.dirname(__file__))
PRODUCT = os.path.dirname(HERE)

SKIP_DIRS = {".git", ".obsidian", ".cache", "node_modules", "private"}
NO_INBOUND_EXEMPT_DIRS = ("reports", "log")
NO_INBOUND_EXEMPT_FILES = {"README.md", "now.md", "tasks.md", "tasks-done.md",
                           "task-source.md", "connections.md", "cos-workspace.yaml"}
TODAY = datetime.date.today()
WORKSPACE_PATH = re.compile(
    r'''^\s*workspace_path\s*:\s*(?:"([^"]*)"|'([^']*)'|([^#]*?))\s*(?:#.*)?$'''
)


def find_workspace(explicit):
    if explicit:
        return os.path.abspath(os.path.expanduser(explicit))
    cfg = os.path.join(PRODUCT, "cos-os.yaml")
    if os.path.exists(cfg):
        with open(cfg, encoding="utf-8") as config:
            for line in config:
                m = WORKSPACE_PATH.match(line)
                if m:
                    value = next(group for group in m.groups() if group is not None)
                    value = value.strip()
                    if value:
                        return os.path.abspath(os.path.expanduser(value))
                    break
    inside = os.path.join(PRODUCT, "workspace")
    if os.path.isdir(inside):
        return inside
    return None


def main():
    ap = argparse.ArgumentParser(description="Read-only workspace health check.")
    ap.add_argument("--workspace", help="path to the private workspace (default: from cos-os.yaml)")
    ap.add_argument("--strict", action="store_true", help="exit 1 when anything is found")
    args = ap.parse_args()

    root = find_workspace(args.workspace)
    if not root or not os.path.isdir(root):
        sys.exit("No workspace found. Pass --workspace PATH or set workspace_path in cos-os.yaml.")

    files = {}
    nested = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        # A nested checkout may carry .git as a directory or as a file (for
        # example, a worktree or submodule). Both create the same tree boundary.
        if rel_dir != "." and (".git" in dirnames or ".git" in filenames):
            nested.append(rel_dir)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, f), root)
                try:
                    files[rel] = open(os.path.join(root, rel), encoding="utf-8").read()
                except OSError as e:
                    print(f"  could not read {rel}: {e}")

    by_base = collections.defaultdict(list)
    for rel in files:
        by_base[os.path.splitext(os.path.basename(rel))[0].lower()].append(rel)

    fence = re.compile(r"```.*?```", re.S)
    code_span = re.compile(r"`[^`]*`")
    wikilink = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\|[^\]]*)?\]\]")
    mdlink = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

    out_edges = collections.defaultdict(set)
    in_edges = collections.defaultdict(set)
    broken = []
    for rel, raw in files.items():
        text = code_span.sub("", fence.sub("", raw))
        srcdir = os.path.dirname(rel)
        for m in wikilink.finditer(text):
            t = m.group(1).strip()
            cands = by_base.get(os.path.splitext(os.path.basename(t))[0].lower(), [])
            if cands:
                out_edges[rel].add(cands[0]); in_edges[cands[0]].add(rel)
            else:
                broken.append(f"{rel} -> [[{t}]]")
        for m in mdlink.finditer(text):
            t = m.group(1).strip()
            if t.startswith("<") and t.endswith(">"):
                t = t[1:-1].strip()
            if not t or t.startswith(("http://", "https://", "mailto:", "#")):
                continue
            t2 = t.split("#")[0]
            resolved = None
            for cand in (os.path.normpath(os.path.join(srcdir, t2)), os.path.normpath(t2)):
                if cand in files:
                    resolved = cand; break
            if resolved:
                out_edges[rel].add(resolved); in_edges[resolved].add(rel)
            elif t2.endswith(".md") and not os.path.exists(os.path.join(root, srcdir, t2)):
                broken.append(f"{rel} -> {t}")  # links into skipped folders (private/) still count as present

    def exempt_from_inbound(rel):
        return (rel.split(os.sep)[0] in NO_INBOUND_EXEMPT_DIRS
                or os.path.basename(rel) in NO_INBOUND_EXEMPT_FILES)

    isolated = sorted(r for r in files if not out_edges.get(r) and not in_edges.get(r)
                      and not exempt_from_inbound(r))
    dead_ends = sorted(r for r in files if out_edges.get(r) and not in_edges.get(r)
                       and not exempt_from_inbound(r))

    # stale entities: frontmatter review-by in the past
    fm = re.compile(r"\A---\n(.*?)\n---", re.S)
    rb = re.compile(r"^review-by:\s*(\d{4}-\d{2}-\d{2})", re.M)
    stale = []
    for rel, raw in files.items():
        m = fm.match(raw)
        if not m:
            continue
        d = rb.search(m.group(1))
        if d:
            try:
                due = datetime.date.fromisoformat(d.group(1))
            except ValueError:
                continue
            if due < TODAY:
                stale.append(f"{rel} (review-by {due}, {(TODAY - due).days} days ago)")

    # uncommitted work, if the workspace is a git repository
    untracked, modified, is_git = [], [], False
    try:
        top = subprocess.run(["git", "-C", root, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=10)
        # only when the workspace is its own repository — a workspace nested inside
        # another repo (the product folder, say) would otherwise report that repo's files
        is_git = top.returncode == 0 and os.path.realpath(top.stdout.strip()) == os.path.realpath(root)
        if is_git:
            st = subprocess.run(["git", "-C", root, "status", "--porcelain", "--untracked-files=all"],
                                capture_output=True, text=True, timeout=20)
            for line in st.stdout.splitlines():
                code, path = line[:2], line[3:]
                (untracked if code == "??" else modified).append(path)
    except (OSError, subprocess.SubprocessError):
        pass
    untracked_unlinked = [p for p in untracked if p.endswith(".md") and p in files and not in_edges.get(p)]

    edges = sum(len(v) for v in out_edges.values())
    print(f"Workspace health check — {TODAY}")
    print(f"Workspace: {root}")
    print(f"Notes: {len(files)} · links: {edges} · isolated: {len(isolated)} · dead ends: {len(dead_ends)}"
          f" · stale: {len(stale)} · nested repos: {len(nested)}"
          f" · uncommitted: {len(untracked) + len(modified) if is_git else 'n/a (workspace is not its own git repo)'}\n")

    found = False

    def section(title, items, hint, limit=20):
        nonlocal found
        if not items:
            return
        found = True
        print(f"✗ {title} ({len(items)}) — {hint}")
        for i in items[:limit]:
            print(f"    {i}")
        if len(items) > limit:
            print(f"    … and {len(items) - limit} more")
        print()

    section("nested git repositories", [f"{n}/" for n in nested],
            "move each one out to a sibling folder; one tree, one repo")
    section("broken links", broken, "fix the path or remove the link")
    section("isolated notes", isolated, "link them from their folder README, or delete them")
    section("dead ends", dead_ends, "nothing links here — add them to their folder README")
    section("stale entities", stale, "confirm the facts and move last-confirmed / review-by forward")
    if is_git and (untracked or modified):
        found = True
        print(f"✗ uncommitted work ({len(untracked)} untracked, {len(modified)} modified) — "
              "not backed up; a live session may own some of it, the rest is work that ended without an ending")
        for p in modified[:15]:
            print(f"    M  {p}")
        for p in untracked[:15]:
            print(f"    ?? {p}" + ("   ← also unlinked" if p in untracked_unlinked else ""))
        if len(untracked) + len(modified) > 30:
            print("    …")
        print()

    if not found:
        print("✓ Clean: nothing broken, nothing orphaned, nothing stale, nothing nested, nothing uncommitted.")
    print("(Read-only. Fix things in a session, then re-run. Log meaningful fixes in log/activity.md.)")
    return 1 if (found and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
