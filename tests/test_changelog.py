import unittest
import tempfile
import os
import shutil
import subprocess
from generate_changelog import generate_changelog, parse_commit

class TestChangelogGenerator(unittest.TestCase):
    def test_parse_commit_conventional(self):
        cat, msg, scope = parse_commit("feat(auth): implement JWT refresh tokens")
        self.assertEqual(cat, "Added")
        self.assertEqual(scope, "auth")
        self.assertEqual(msg, "implement JWT refresh tokens")

        cat, msg, scope = parse_commit("fix(api): resolve 500 error on nil pointer")
        self.assertEqual(cat, "Fixed")
        self.assertEqual(scope, "api")

        cat, msg, scope = parse_commit("refactor: simplify database connection pool")
        self.assertEqual(cat, "Changed")
        self.assertIsNone(scope)

        cat, msg, scope = parse_commit("remove(legacy): delete deprecated v1 endpoints")
        self.assertEqual(cat, "Removed")
        self.assertEqual(scope, "legacy")

    def test_repo_generation(self):
        tmp_dir = tempfile.mkdtemp()
        try:
            # Initialize git repo
            subprocess.run(["git", "init"], cwd=tmp_dir, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "TestUser"], cwd=tmp_dir, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_dir, check=True)

            # Commit 1
            f1 = os.path.join(tmp_dir, "file1.txt")
            with open(f1, "w") as f:
                f.write("hello")
            subprocess.run(["git", "add", "."], cwd=tmp_dir, check=True)
            subprocess.run(["git", "commit", "-m", "feat: initial commit with core engine"], cwd=tmp_dir, check=True)

            # Tag v1.0.0
            subprocess.run(["git", "tag", "v1.0.0"], cwd=tmp_dir, check=True)

            # Commit 2 & 3
            with open(f1, "a") as f:
                f.write(" world")
            subprocess.run(["git", "add", "."], cwd=tmp_dir, check=True)
            subprocess.run(["git", "commit", "-m", "fix(core): fix buffer overflow in parser"], cwd=tmp_dir, check=True)

            f2 = os.path.join(tmp_dir, "file2.txt")
            with open(f2, "w") as f:
                f.write("new feature")
            subprocess.run(["git", "add", "."], cwd=tmp_dir, check=True)
            subprocess.run(["git", "commit", "-m", "feat(export): add CSV export feature"], cwd=tmp_dir, check=True)

            # Generate changelog
            out_md = os.path.join(tmp_dir, "CHANGELOG.md")
            res = generate_changelog(repo_path=tmp_dir, version="v1.1.0", output_path=out_md)

            self.assertTrue(os.path.exists(out_md))
            self.assertIn("## [v1.1.0]", res)
            self.assertIn("### Added", res)
            self.assertIn("### Fixed", res)
            self.assertIn("add CSV export feature", res)
            self.assertIn("fix buffer overflow in parser", res)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

if __name__ == "__main__":
    unittest.main()

