# New Package

## Intake

Collect:

- Category/package name.
- Upstream URL.
- Release version and source archive URL.
- License.
- Build system and language ecosystem.
- Build metadata and package profile: primary build system, source versus live/binary mode, runtime role, services/rules, ABI or implementation selection, and test model.
- Runtime files: binaries, libraries, services, desktop files, fonts, icons, shell completions, plugins.
- Expected keywords and what can be tested locally.

If any item is missing, try to discover it before asking the user. Do not rely on upstream metadata alone when the release archive, license file, or build files can be inspected.

## Workflow

1. Read repository policy and package layout rules.
2. Search for existing package names, forks, renamed projects, and same upstream in the overlay and main Gentoo tree.
3. Search for similar ebuilds in the same language/build system.
4. Infer the package profile and read `references/domain-routing.md`, `references/shell-idioms.md`, plus the matching domain reference.
5. Run eclass discovery and write a short eclass decision record with the generated skeleton and exception trigger.
6. Draft `category/package/package-version.ebuild` using existing package style.
7. Audit dependencies before treating the draft as ready.
8. Draft or update `metadata.xml`.
9. Add files under `files/` only when patches, init scripts, service files, wrappers, or desktop integration cannot be generated cleanly in phases.
10. Check repository nvchecker coverage when the repository has `.github/workflows/overlay.toml`.
11. Run `scripts/ensure_copyright_year.py --fix` on the new ebuild.
12. Generate `Manifest` with `pkgdev manifest`.
13. Run package-level QA, then commit-level QA if preparing a PR.

Read-only searches in steps 2-3 can run in parallel. Step 4 consumes that
evidence and settles the package profile before drafting. Drafting files,
Manifest generation, and QA reruns stay serial.

## Ebuild Drafting Checks

- Set an appropriate EAPI by matching current Gentoo practice and local package style.
- Keep `DESCRIPTION`, `HOMEPAGE`, `SRC_URI`, `S`, and `LICENSE` accurate.
- Keep `SLOT`, `KEYWORDS`, `IUSE`, `RESTRICT`, `DEPEND`, `RDEPEND`, and `BDEPEND` minimal but complete.
- Use `src_prepare`, `src_configure`, `src_compile`, `src_install`, `pkg_postinst`, and `pkg_postrm` only when needed.
- Do not claim keywords that cannot be tested or justified under repository policy.
- Do not invent licenses. Verify upstream license files and Gentoo license names.
- For bundled binaries, verify architecture, redistribution constraints, install paths, and whether `strip` or QA exceptions are needed.
- Prefer normal phase functions and existing eclasses over generated wrappers or custom helper scripts.
- Generate the eclass-owned phase skeleton first, then add only package-specific arguments or install steps supported by source evidence.

## Dependency Audit

Do not add dependencies defensively. Every `DEPEND`, `RDEPEND`, `BDEPEND`, test dependency, and optional dependency must have a concrete reason from upstream build files, source imports/linkage, installed runtime behavior, enabled features, eclass requirements, or same-package precedent.

- Classify each dependency as build-time, runtime, test-only, optional feature/plugin, or eclass/tooling requirement before placing it in `DEPEND`, `RDEPEND`, `BDEPEND`, or a USE-conditional branch.
- Do not copy dependencies from upstream packaging, generated metadata, distribution packages, old ebuilds, or similar packages without checking that the new ebuild actually uses each one.
- Do not declare transitive dependencies unless the package directly imports, links, executes, loads, or otherwise requires them, or repository/Gentoo policy requires explicit declaration.
- Keep optional integrations behind matching USE flags when they are supported; otherwise omit dependencies for disabled features instead of enabling extra functionality accidentally.
- Treat test-only dependencies separately from build/runtime dependencies, and do not add them when tests are disabled or cannot be run unless repository policy requires them.
- If a dependency cannot be justified after checking upstream evidence and local precedent, leave it out or stop and ask with the evidence instead of padding the dependency list.

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
