#!/usr/bin/env python3
"""Check or update Gentoo copyright years in changed ebuild/eclass files."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path


SUPPORTED_SUFFIXES = {".ebuild", ".eclass"}
COPYRIGHT_RE = re.compile(
    r"^(?P<prefix># Copyright )(?:\d{4}-)?(?P<year>\d{4})(?P<suffix> Gentoo Authors)$"
)


def changed_paths() -> list[Path]:
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMR"],
        ["git", "diff", "--name-only", "--cached", "--diff-filter=ACMR"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    paths: list[Path] = []
    seen: set[Path] = set()
    for command in commands:
        result = subprocess.run(
            command, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            path = Path(line)
            if path not in seen:
                seen.add(path)
                paths.append(path)
    return paths


def candidate_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.suffix not in SUPPORTED_SUFFIXES:
            continue
        if not path.is_file():
            continue
        files.append(path)
    return files


def update_file(path: Path, year: int, fix: bool) -> str | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if not lines:
        return None

    match = COPYRIGHT_RE.match(lines[0].rstrip("\n"))
    if not match:
        return None

    current_year = int(match.group("year"))
    if current_year >= year:
        return None

    old_line = lines[0]
    newline = "\n" if old_line.endswith("\n") else ""
    lines[0] = f"{match.group('prefix')}1999-{year}{match.group('suffix')}{newline}"
    if fix:
        path.write_text("".join(lines), encoding="utf-8")
        return "updated"
    return "would update"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check or update Gentoo copyright years in ebuild/eclass files."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Files to check. Defaults to changed git ebuild/eclass files.",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Rewrite stale copyright years instead of only reporting them.",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=dt.date.today().year,
        help="Expected copyright year. Defaults to the current year.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = args.paths or changed_paths()
    files = candidate_files(paths)

    stale: list[tuple[Path, str]] = []
    for path in files:
        result = update_file(path, args.year, args.fix)
        if result:
            stale.append((path, result))

    for path, result in stale:
        print(f"{path}: {result} copyright year to {args.year}")

    if stale and not args.fix:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
