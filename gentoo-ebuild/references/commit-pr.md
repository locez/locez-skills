# Commit And PR

## Commit Preparation

1. Inspect `git diff --stat` and package-specific diff.
2. Confirm ebuild and `Manifest` changes are in the same logical commit.
3. Run repository-required QA.
4. Use `pkgdev commit` unless repository policy requires another command.

## Commit Command

Follow the repository's exact command when specified. If none is specified, prefer:

```bash
pkgdev commit
```

If repository policy requires signing and signing is unavailable, fall back only when policy allows it or the user approves it, and report the fallback.

## Commit Message

Prefer Gentoo package style:

```text
category/package: short imperative or descriptive summary

Optional explanation of why the change is needed.
Reference bugs or upstream issues when relevant.
```

For version bumps:

```text
category/package: add new_version, drop old_version
```

Use the add/drop wording only when the old ebuild is actually removed. Treat that as a version replacement decision, not as unrelated cleanup.

Follow repository-specific rules when they differ.

Do not add AI-generated attribution, generated-by footers, or unrelated co-author lines.

## PR Preparation

- One topic branch per logical PR.
- One PR may include multiple packages only when they are one logical contribution.
- Mention package testing and QA commands.
- Mention untested arches or skipped build/install checks.
- Keep unrelated cleanup out of the PR.
- When creating a PR with `gh`, write the body to a temporary Markdown file and pass it with `--body-file` instead of inline `--body` text. This preserves headings, lists, checkboxes, and command output formatting.

Example:

```bash
gh pr create --title "category/package: add 1.2.3" --body-file /tmp/category-package-pr.md
```

Remove the temporary body file after confirming the PR was created if it contains no information that needs to be kept.
