# New Package

## Intake

Collect:

- Category/package name.
- Upstream URL.
- Release version and source archive URL.
- License.
- Build system and language ecosystem.
- Runtime files: binaries, libraries, services, desktop files, fonts, icons, shell completions, plugins.
- Expected keywords and what can be tested locally.

If any item is missing, try to discover it before asking the user. Do not rely on upstream metadata alone when the release archive, license file, or build files can be inspected.

## Workflow

1. Read repository policy and package layout rules.
2. Search for existing package names, forks, renamed projects, and same upstream in the overlay and main Gentoo tree.
3. Search for similar ebuilds in the same language/build system.
4. Run eclass discovery and write a short eclass decision record.
5. Draft `category/package/package-version.ebuild` using existing package style.
6. Draft or update `metadata.xml`.
7. Add files under `files/` only when patches, init scripts, service files, wrappers, or desktop integration cannot be generated cleanly in phases.
8. Check repository nvchecker coverage when the repository has `.github/workflows/overlay.toml`.
9. Run `scripts/ensure_copyright_year.py --fix` on the new ebuild.
10. Generate `Manifest` with `pkgdev manifest`.
11. Run package-level QA, then commit-level QA if preparing a PR.

Read-only searches in steps 2-4 can run in parallel. Drafting files, Manifest generation, and QA reruns stay serial.

## Ebuild Drafting Checks

- Set an appropriate EAPI by matching current Gentoo practice and local package style.
- Keep `DESCRIPTION`, `HOMEPAGE`, `SRC_URI`, `S`, and `LICENSE` accurate.
- Keep `SLOT`, `KEYWORDS`, `IUSE`, `RESTRICT`, `DEPEND`, `RDEPEND`, and `BDEPEND` minimal but complete.
- Use `src_prepare`, `src_configure`, `src_compile`, `src_install`, `pkg_postinst`, and `pkg_postrm` only when needed.
- Do not claim keywords that cannot be tested or justified under repository policy.
- Do not invent licenses. Verify upstream license files and Gentoo license names.
- For bundled binaries, verify architecture, redistribution constraints, install paths, and whether `strip` or QA exceptions are needed.
- Prefer normal phase functions and existing eclasses over generated wrappers or custom helper scripts.

## Nvchecker Coverage

If the target repository uses `.github/workflows/overlay.toml`, check whether the new `cat/pkg` has a matching nvchecker entry.

- If an entry already exists, make sure it matches the chosen upstream identity.
- If no entry exists and the upstream is clearly GitHub or PyPI, propose a candidate entry in the final report or PR notes and explain the evidence.
- Do not auto-edit `overlay.toml` as part of the package draft unless the user or repository policy asks for it.
- Treat GitLab, generic git, regex, vendor download pages, and renamed upstreams as manual nvchecker configuration unless the correct source rule is obvious from repository precedent.

## Validation

Use repository-required commands. Typical sequence: `pkgdev manifest`, package-level `pkgcheck scan`, build/install check when feasible, and commit-level `pkgcheck scan --commits --net` before PR when required.

Adapt for packages that cannot be built locally, but report the limitation clearly.

## Stop And Ask

Ask before proceeding when:

- Upstream license or redistribution rights are unclear.
- The package requires credentials, proprietary downloads, or click-through terms.
- The correct category/package name is ambiguous.
- The package needs major patching or vendoring decisions.
- A claimed keyword cannot be tested and repository policy does not answer what to do.
- Eclass choice remains ambiguous after local package examples and official Gentoo sources are checked.
