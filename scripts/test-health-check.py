"""Regression tests use disposable fictional workspaces only."""
import datetime
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import sys

spec = importlib.util.spec_from_file_location("health", Path(__file__).with_name("health-check.py"))
health = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health)
DAY = datetime.date(2026, 8, 24)

class HealthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def put(self, name, body=""):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(body if isinstance(body, bytes) else body.encode())
        return p

    def scan(self):
        return health.scan(self.root, DAY)

    def test_link_formats_and_assets(self):
        self.put("README.md", '[A](my%20note.md) [B](b.md "title") ![[image.png]] [[folder/c]]')
        for name in ("my note.md", "b.md", "folder/c.md", "image.png"):
            self.put(name)
        self.assertFalse(any(self.scan()[2].values()))

    def test_missing_assets_and_wrong_wiki_path(self):
        self.put("README.md", '[[missing/a]] ![image](missing.png)')
        self.put("elsewhere/a.md")
        self.assertEqual(len(self.scan()[2]["broken or ambiguous links"]), 2)

    def test_duplicate_wiki_names(self):
        self.put("README.md", "[[a]]")
        self.put("one/a.md")
        self.put("two/a.md")
        self.assertIn("ambiguous", self.scan()[2]["broken or ambiguous links"][0])

    def test_relative_path_cannot_fall_back_to_root(self):
        self.put("README.md", "[note](folder/note.md)")
        self.put("folder/note.md", "[A](a.md)")
        self.put("a.md")
        self.assertEqual(len(self.scan()[2]["broken or ambiguous links"]), 1)

    def test_private_and_symlinks_are_not_read(self):
        self.put("README.md", "[[private/secret]] [P](private/missing.md) [Alias](alias.md)")
        secret = self.put("private/secret.md", "[hidden](never-disclose.md)")
        (self.root / "alias.md").symlink_to(secret)
        (self.root / "alias-dir").symlink_to(secret.parent, target_is_directory=True)
        notes, _, findings, _, _ = self.scan()
        self.assertEqual(set(notes), {"README.md"})
        self.assertEqual(len(findings["skipped symlinks"]), 2)
        self.assertNotIn("never-disclose", str(findings))
        self.assertFalse(findings["broken or ambiguous links"])

    def test_disconnected_cycle_and_root_exemption(self):
        self.put("README.md")
        self.put("a.md", "[B](b.md)")
        self.put("b.md", "[A](a.md)")
        self.put("project/tasks.md")
        self.assertEqual(set(self.scan()[2]["unreachable"]), {"a.md", "b.md", "project/tasks.md"})

    def test_review_dates(self):
        for name, value in (("a", '"2020-01-01"'), ("b", "'2020-01-01'"),
                            ("c", "2020-01-01"), ("d", "never"), ("e", "2026-08-24"),
                            ("f", "invalid"), ("g", "2027-01-01")):
            self.put(name + ".md", "---\nreview-by: " + value + "\n---\n")
        findings = self.scan()[2]
        self.assertEqual(len(findings["stale"]), 3)
        self.assertEqual(findings["invalid review dates"], ["f.md"])

    def test_bad_encoding_and_read_failure_are_incomplete(self):
        self.put("bad.md", b"\xff")
        self.put("good.md")
        self.assertTrue(self.scan()[3])
        with patch.object(health.os, "open", side_effect=PermissionError):
            self.assertEqual(len(self.scan()[3]), 2)

    def test_git_failure_never_clean(self):
        responses = [subprocess.CompletedProcess([], 0, str(self.root), ""),
                     subprocess.CompletedProcess([], 128, b"", b"failed")]
        with patch.object(health.subprocess, "run", side_effect=responses):
            self.assertIn("Git status failed", self.scan()[3])

    def test_git_timeout_is_incomplete(self):
        with patch.object(health.subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 10)):
            self.assertTrue(self.scan()[3])

    def test_git_nul_names_and_private_redaction(self):
        responses = [subprocess.CompletedProcess([], 0, str(self.root), ""),
                     subprocess.CompletedProcess([], 0,
                        b"R  new name.md\0old.md\0?? private/secret.md\0?? line\nname.md\0", b"")]
        with patch.object(health.subprocess, "run", side_effect=responses):
            items = self.scan()[2]["uncommitted"]
        self.assertEqual(len(items), 3)
        self.assertNotIn("secret.md", str(items))
        self.assertIn("line\nname.md", items[-1])

    def test_nested_repo_is_reported_and_excluded(self):
        self.put("nested/.git", "gitdir: elsewhere")
        self.put("nested/note.md", "[hidden](missing.md)")
        notes, _, f, _, _ = self.scan()
        self.assertNotIn("nested/note.md", notes)
        self.assertEqual(f["nested repos"], ["nested"])

    def test_selected_workspace_and_read_only(self):
        self.put("README.md")
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = subprocess.run([sys.executable, str(Path(health.__file__)),
                                 "--workspace", str(self.root), "--strict"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertIn(str(self.root), result.stdout)

    def test_exit_codes(self):
        self.put("README.md", "[missing](missing.md)")
        cmd = [sys.executable, str(Path(health.__file__)), "--workspace", str(self.root)]
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(cmd + ["--strict"], capture_output=True).returncode, 1)
        self.put("bad.md", b"\xff")
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)

    def test_sample_fixed_date(self):
        _, _, f, errors, _ = health.scan(health.PRODUCT / "example-company", DAY)
        self.assertFalse(errors)
        self.assertEqual(len(f["stale"]), 1)
        self.assertFalse(f["unreachable"])

    def test_config_and_explicit_workspace_isolation(self):
        product = self.root / "product"
        product.mkdir()
        configured = self.root / "configured#space"
        configured.mkdir()
        (product / "cos-os.yaml").write_text('workspace_path: "' + str(configured) + '"')
        with patch.object(health, "PRODUCT", product):
            self.assertEqual(health.workspace(None), configured)
            self.assertEqual(health.workspace(str(self.root)), self.root)
            (product / "cos-os.yaml").write_text('workspace_path: ""')
            with self.assertRaises(ValueError):
                health.workspace(None)

    def test_code_examples_do_not_create_links(self):
        self.put("README.md", '```md\n[bad](missing.md)\n```\n~~~md\n[[missing]]\n~~~\n')
        self.assertFalse(any(self.scan()[2].values()))

if __name__ == "__main__":
    unittest.main()
