# QA

## Triage

Classify the issue:

- Metadata: invalid `metadata.xml`, missing remote-id, maintainer problems.
- Manifest/distfiles: checksum, stale files, mirror restrictions.
- Ebuild style: EAPI, variable ordering, quoting, phases, obsolete eclasses.
- Dependency: missing, invalid USE deps, circular, wrong `BDEPEND`/`RDEPEND`.
- Runtime/install: wrong paths, missing files, QA prestripped/bundled libs, desktop/icon/cache handling.
- Keywording: unsupported stable keywords, untested arches.
- Mechanical header lint: stale Gentoo copyright year in edited `.ebuild` or `.eclass` files.
- Preflight basics: missing required variables, stable keywords where only unstable keywords are allowed, or missing `SRC_URI` without an eclass/live-ebuild reason.

## Commands

```bash
python3 <gentoo-ebuild-skill>/scripts/ensure_copyright_year.py --fix path/to/package-version.ebuild
pkgcheck scan category/package
pkgcheck scan --commits
pkgcheck scan --commits --net
pkgdev manifest category/package
ebuild category/package/package-version.ebuild clean compile install
```

Run narrower commands while iterating, then broader commands before final reporting. Do not replace native QA tools with custom wrappers unless the repository explicitly requires them.

## Preflight Basics

Before running broader QA on an edited ebuild, scan for the easy mechanical failures:

- `EAPI`, `DESCRIPTION`, `HOMEPAGE`, `LICENSE`, `SLOT`, and usually `SRC_URI` are present and accurate.
- `SRC_URI` may be absent only when the inherited eclass or live ebuild behavior clearly provides the source.
- `KEYWORDS` follows repository policy; do not introduce stable keywords when the overlay expects unstable keywords only.
- `DEPEND`, `RDEPEND`, and `BDEPEND` reflect the build/runtime split instead of copying old dependencies blindly.
- `RESTRICT` and QA exceptions are justified by package behavior, not added only to silence checks.

## Loop Protocol

1. Read the exact finding and identify whether the owner is metadata, Manifest, ebuild logic, dependency declaration, installed files, keywords, or repository policy.
2. Make the smallest fix that addresses the root cause.
3. For edited `.ebuild` or `.eclass` files, run `scripts/ensure_copyright_year.py --fix` before Manifest/QA.
4. Re-run the command that exposed the issue.
5. After the same issue recurs twice, stop changing blindly; report the evidence, suspected cause, and next decision needed.
6. Run commit-level QA only after the package diff is stable.

## Fixing Rules

- Fix root causes, not only warnings.
- Do not silence QA unless the package type genuinely requires it.
- If adding QA exceptions, explain why they are correct for this package.
- Re-run the command that exposed the problem after each fix.
- When a warning is intentionally left, include the rationale and risk.
- If `--net` checks, build checks, or install checks cannot run locally, mark them skipped with the concrete reason.

## Final Report

Include:

- Commands run.
- Pass/fail result.
- Any checks skipped and why.
- Any remaining warnings or known limitations.
