# Version Bump

## Classify The Change

- Add-only bump: add a new released ebuild while preserving existing versions.
- Version replacement: after the new ebuild passes checks, remove an older ebuild as a separate end-of-flow maintainer decision.
- Revision update: adjust `-rN` for the same upstream version.
- Live sync: update `9999` behavior separately from released ebuilds.

## Before Editing

1. Read existing ebuilds and package history.
2. Normalize the upstream version to a Gentoo PV and compare it with the current highest released ebuild.
3. Compare upstream release notes, build files, dependency changes, and license changes.
4. Check whether patches, files, services, wrappers, or desktop assets still apply.
5. Decide whether to copy the old ebuild, use `pkgdev bump` if available, or rewrite around newer eclass practice.
6. If the build system, language ecosystem, source layout, or helper behavior changed, run eclass discovery before editing.

## Version And Input Checks

- Normalize common upstream tags before editing: `v1.2.3` becomes `1.2.3`; `rc`, `beta`, `alpha`, and `pre` tags must use Gentoo suffixes such as `_rc`, `_beta`, `_alpha`, and `_pre` when appropriate.
- Do not assume prereleases should be bumped. Follow repository policy, user intent, or upstream's release channel.
- Stop if the normalized target PV is not newer than the current released ebuild, unless the request is a revision update or a deliberate rebuild.
- If the bump comes from an nvchecker issue, read the issue body and comments before editing. Treat comments mentioning broken builds, regressions, crashes, "do not bump", or similar blocker language as a stop-and-ask condition.
- Maintainer CC in an issue is ownership context, not by itself a reason to skip.

## Update Steps

- Copy the selected old ebuild to the new version first, usually `cp old.ebuild new.ebuild`, unless repository tooling or package history clearly suggests another approach.
- Update `SRC_URI`, checksums through `pkgdev manifest`, and any version-specific variables.
- Run `scripts/ensure_copyright_year.py --fix` on edited ebuild/eclass files before Manifest/QA.
- Check repository nvchecker coverage when `.github/workflows/overlay.toml` exists. If the package has no entry, propose a candidate only when the source is obvious; do not auto-edit the file without user or repository direction.
- Keep old versions in place while validating the new ebuild.
- Preserve old revisions if they are still needed for compatibility.
- Keep live `9999` ebuild behavior separate from release ebuild behavior.

## Package Type Focus

- Binary packages, especially `-bin`, need extra attention on `SRC_URI`, archive compression, architecture layout, bundled libraries, prestripped files, install paths, and redistribution constraints.
- Source packages need extra attention on dependency changes, patch applicability, test restrictions, build-system changes, and generated files.
- Packages with services, desktop files, icons, fonts, shell completions, or wrappers need path and install-behavior checks even when the ebuild diff is small.

## Patch And Files Check

Before treating a copied ebuild as ready, inspect `files/` entries referenced by the old ebuild.

- Re-check every patch against the new upstream source; do not keep patches only because filenames still match.
- Remove patches only after confirming the new source contains the fix or the patch is no longer relevant.
- Re-check init scripts, service files, desktop files, wrappers, icons, and completions for upstream path changes.
- If a patch or generated file changes, prefer a build phase check that reaches at least `src_prepare`; report skipped patch validation explicitly.

## Old Version Gate

After the new ebuild has passed the strongest feasible Manifest, QA, and build/install checks, ask whether to remove an old version if repository policy or package history does not already decide it.

Default to add-only when the user does not answer, when old-version compatibility is unclear, or when the new ebuild has not been validated.

If the old version is removed:

1. Treat the deletion as part of the same version-replacement PR, not unrelated cleanup.
2. Keep live `9999` ebuilds unless explicitly replacing live behavior.
3. List the exact old ebuild deletion candidate before deleting it.
4. Prefer Gentoo or Portage version ordering for choosing removal candidates; in scripts use `portage.versions.vercmp`, and do not rely on lexicographic filename order.
5. Run `pkgdev manifest` again after deletion.
6. Re-run package-level QA, and commit-level QA if preparing a PR.
7. Report both validation rounds: new-version validation before deletion, and post-deletion validation.

## Checks

Use repository-required commands. Regenerate Manifest when distfiles change. If compile/install is too expensive or not possible, run the strongest available subset and report the limitation.

## Common Bump Risks

- Upstream changed build system or dependency names.
- Source archive layout changed, requiring `S=`.
- License changed.
- Vendored dependencies changed.
- Tests need new restrictions.
- Desktop/service files changed path.
- Binary packages changed compression, architecture layout, or bundled library set.

## Stop And Ask

Ask before proceeding when keyword changes, license changes, or dependency interpretation is not settled by package history, repository policy, and upstream evidence. Ask at the old-version gate before deleting an old ebuild unless repository policy or the user already requested removal.
