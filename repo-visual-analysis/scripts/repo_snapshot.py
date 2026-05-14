#!/bin/sh
"exec" "$(command -v python3 || command -v python)" "$0" "$@"

from __future__ import annotations

__doc__ = "Create a lightweight repository snapshot for repo-visual-analysis."

import argparse
import json
import os
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "target",
    ".next",
    ".nuxt",
    "coverage",
}

MANIFEST_NAMES = {
    "package.json",
    "pnpm-workspace.yaml",
    "yarn.lock",
    "package-lock.json",
    "pyproject.toml",
    "requirements.txt",
    "uv.lock",
    "poetry.lock",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "go.sum",
    "pom.xml",
    "build.gradle",
    "settings.gradle",
    "Gemfile",
    "composer.json",
    "Makefile",
    "justfile",
    "Dockerfile",
    "docker-compose.yml",
}

CI_PARTS = {".github/workflows", ".gitlab-ci.yml", "circle.yml", ".circleci", "azure-pipelines.yml"}
DOC_NAMES = {"README", "README.md", "README.rst", "docs", "CONTRIBUTING.md", "AGENTS.md", "CLAUDE.md"}
TEST_MARKERS = {"test", "tests", "spec", "specs", "__tests__", "pytest.ini", "vitest.config", "jest.config"}
ENTRY_MARKERS = {
    "main.py",
    "app.py",
    "server.py",
    "index.js",
    "index.ts",
    "main.ts",
    "main.tsx",
    "src/main.rs",
    "cmd",
}


def run_git(repo: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def is_ignored(path: Path, repo: Path) -> bool:
    rel_parts = path.relative_to(repo).parts
    return any(part in IGNORE_DIRS for part in rel_parts)


def iter_files(repo: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for root, dirs, names in os.walk(repo):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not is_ignored(root_path / d, repo)]
        for name in names:
            path = root_path / name
            if is_ignored(path, repo):
                continue
            files.append(path)
            if len(files) >= max_files:
                return files
    return files


def rel(path: Path, repo: Path) -> str:
    return path.relative_to(repo).as_posix()


def collect(repo: Path, max_files: int) -> dict[str, Any]:
    files = iter_files(repo, max_files)
    ext_counts: Counter[str] = Counter()
    top_dirs: Counter[str] = Counter()
    largest: list[dict[str, Any]] = []
    manifests: list[str] = []
    docs: list[str] = []
    tests: list[str] = []
    ci: list[str] = []
    entries: list[str] = []

    for path in files:
        relative = rel(path, repo)
        parts = Path(relative).parts
        if len(parts) > 1:
            top_dirs[parts[0]] += 1
        else:
            top_dirs["."] += 1

        suffix = path.suffix.lower() or "[no extension]"
        ext_counts[suffix] += 1

        name = path.name
        if name in MANIFEST_NAMES:
            manifests.append(relative)
        if name in DOC_NAMES or parts[0] in DOC_NAMES:
            docs.append(relative)
        if any(marker in parts or name.startswith(marker) for marker in TEST_MARKERS):
            tests.append(relative)
        if any(relative.startswith(part) or name == part for part in CI_PARTS):
            ci.append(relative)
        if name in ENTRY_MARKERS or relative in ENTRY_MARKERS or parts[0] in ENTRY_MARKERS:
            entries.append(relative)

        try:
            size = path.stat().st_size
        except OSError:
            size = 0
        largest.append({"path": relative, "bytes": size})

    largest.sort(key=lambda item: item["bytes"], reverse=True)

    return {
        "repo": str(repo),
        "git": {
            "head": run_git(repo, ["rev-parse", "--short", "HEAD"]),
            "branch": run_git(repo, ["branch", "--show-current"]),
            "status_short": run_git(repo, ["status", "--short"]),
        },
        "counts": {
            "files_scanned": len(files),
            "max_files": max_files,
            "truncated": len(files) >= max_files,
        },
        "top_directories": top_dirs.most_common(30),
        "extensions": ext_counts.most_common(30),
        "manifests": sorted(manifests)[:80],
        "docs": sorted(docs)[:80],
        "tests": sorted(tests)[:120],
        "ci": sorted(ci)[:80],
        "entry_candidates": sorted(entries)[:120],
        "largest_files": largest[:40],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root to scan.")
    parser.add_argument("--out", help="Write JSON snapshot to this path. Prints to stdout when omitted.")
    parser.add_argument(
        "--out-dir",
        help="Directory for snapshot output. Uses snapshot.json by default or a timestamped name with --timestamped.",
    )
    parser.add_argument("--timestamped", action="store_true", help="Write snapshot-YYYYMMDDTHHMMSSZ.json.")
    parser.add_argument("--max-files", type=int, default=20000, help="Maximum files to scan.")
    args = parser.parse_args()

    if args.out and args.out_dir:
        parser.error("--out and --out-dir are mutually exclusive")

    repo = Path(args.repo).resolve()
    data = collect(repo, args.max_files)
    text = json.dumps(data, indent=2, ensure_ascii=False)

    if args.out_dir:
        out_dir = Path(args.out_dir)
        if args.timestamped:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            out = out_dir / f"snapshot-{stamp}.json"
        else:
            out = out_dir / "snapshot.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    elif args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
