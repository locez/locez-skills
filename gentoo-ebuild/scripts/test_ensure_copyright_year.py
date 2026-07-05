#!/usr/bin/env python3
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("ensure_copyright_year.py")


class EnsureCopyrightYearTest(unittest.TestCase):
    def run_script(self, *args, cwd=None):
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_check_reports_stale_ebuild_year(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "app-misc" / "demo" / "demo-1.ebuild"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# Copyright 1999-2024 Gentoo Authors\n"
                "# Distributed under the terms of the GNU General Public License v2\n"
                "\n"
                "EAPI=8\n",
                encoding="utf-8",
            )

            result = self.run_script("--year", "2026", str(path))

            self.assertEqual(result.returncode, 1)
            self.assertIn("would update", result.stdout)
            self.assertEqual(
                path.read_text(encoding="utf-8").splitlines()[0],
                "# Copyright 1999-2024 Gentoo Authors",
            )

    def test_fix_updates_stale_ebuild_year(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "app-misc" / "demo" / "demo-1.ebuild"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# Copyright 1999-2024 Gentoo Authors\n"
                "# Distributed under the terms of the GNU General Public License v2\n"
                "\n"
                "EAPI=8\n",
                encoding="utf-8",
            )

            result = self.run_script("--fix", "--year", "2026", str(path))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("updated", result.stdout)
            self.assertEqual(
                path.read_text(encoding="utf-8").splitlines()[0],
                "# Copyright 1999-2026 Gentoo Authors",
            )

    def test_default_paths_include_untracked_ebuilds(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                ["git", "init"],
                cwd=tmp,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            path = Path(tmp) / "app-misc" / "demo" / "demo-1.ebuild"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# Copyright 1999-2024 Gentoo Authors\n"
                "# Distributed under the terms of the GNU General Public License v2\n"
                "\n"
                "EAPI=8\n",
                encoding="utf-8",
            )

            result = self.run_script("--year", "2026", cwd=tmp)

            self.assertEqual(result.returncode, 1)
            self.assertIn("app-misc/demo/demo-1.ebuild", result.stdout)

    def test_ignores_non_gentoo_author_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "app-misc" / "demo" / "demo-1.ebuild"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# Copyright 2024 Someone Else\n"
                "\n"
                "EAPI=8\n",
                encoding="utf-8",
            )

            result = self.run_script("--fix", "--year", "2026", str(path))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                path.read_text(encoding="utf-8").splitlines()[0],
                "# Copyright 2024 Someone Else",
            )


if __name__ == "__main__":
    unittest.main()
