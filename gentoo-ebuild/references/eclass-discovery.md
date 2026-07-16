# Eclass Discovery

## Goal

Choose eclasses by evidence, not by memory or frequency. The eclass decision is
also a code-generation decision: identify which lifecycle behavior the eclass
owns, then state the standard variables and phase helpers that the generated
ebuild should use. For non-obvious cases, produce a short decision record in
working notes or the final report; do not create a package database.

## Local First

1. Locate the main Gentoo tree:
   - Prefer `/var/db/repos/gentoo` when present.
   - Otherwise inspect `repos.conf`, `eselect repository list`, or existing user context.
2. Search similar packages:
   - Same upstream project family.
   - Same language/build system.
   - Same binary/source packaging style.
   - Same desktop integration, service manager, font, kernel, Python, Rust, Go, Qt, CMake, Meson, npm, or Electron pattern.
3. Inspect candidate eclasses directly under `eclass/*.eclass`.
4. Read comments, variables, and exported functions before relying on phase behavior.

## Commands

```bash
GENTOO=/var/db/repos/gentoo
rg -n "inherit .*cmake|inherit .*meson|inherit .*python|inherit .*cargo|inherit .*go|inherit .*desktop|inherit .*font" "$GENTOO"
sed -n '1,220p' "$GENTOO/eclass/cmake.eclass"
rg -n "^EXPORT_FUNCTIONS|^src_|^pkg_|^src_compile|^src_install|@FUNCTION|@ECLASS_VARIABLE" "$GENTOO/eclass"
```

Use narrower searches once the ecosystem is known.

## Official Fallback

Use official Gentoo sources when local data is absent, old, or ambiguous:

- Gentoo devmanual.
- Gentoo eclass reference.
- gentoo.git package examples and eclass files.
- Project pages under gentoo.org.

For network lookups, prefer official Gentoo sources and current upstream documentation. Cite or summarize evidence when it changes the implementation.

## Decision Heuristics

- Use an eclass when it owns real package behavior: build system phases, language dependency handling, desktop integration, font installation, init/service helpers, kernel modules, Python implementation handling, cargo/go module handling.
- Do not inherit an eclass just for one helper when simple phase code is clearer and established local precedent agrees.
- Prefer modern eclasses used by current Gentoo packages over old compatibility eclasses.
- Treat the build model and installed behavior as stronger signals than the language name. `java-pkg-simple` is for its simple-source model, `perl-module` is for Perl-specific module build systems, and `systemd`/`udev` are for their installed integration behavior.
- Compare live ebuilds and release ebuilds separately; `9999` ebuilds often need different source handling.
- If two eclasses overlap, read both eclasses and existing packages using both before combining them.
- If package precedent and official eclass docs conflict, state the conflict and prefer the safer local package pattern unless it is clearly obsolete.

## Decision Record Template

```text
Package profile: <operation>; <artifact>; <ecosystem/build>; <runtime role>
Eclass decision:
- Candidates and contract evidence:
- Chosen eclass:
- Generated skeleton: <pre-inherit variables>; <inherit order>; <phase helpers>
- Rejected alternatives and why:
- Exception trigger:
- Remaining uncertainty:
```

## Skeleton Rules

- Read `@PRE_INHERIT` variables and set them before `inherit`.
- Use the eclass's exported phases and pseudo-phases as the starting skeleton.
- When overriding a phase, call the eclass helper at the documented point;
  do not silently replace dependency setup, source preparation, or install
  behavior.
- Remember that `inherit` accumulates eclass dependency assignments through
  Portage's `E_*` channels and appends them to final metadata later. Do not
  mirror those dependencies manually or treat a post-inherit
  `BDEPEND="${BDEPEND}"` assignment as access to `E_BDEPEND`.
- Add a helper/integration eclass only when a concrete function, variable,
  installed file, or package contract requires it.
- Prefer the eclass/Portage helper for the generated operation (`doins`,
  `fperms`, `eapply`, `econf`, `emake`, `tc-get*`, or an integration helper)
  before writing an equivalent raw shell command.
- Validate the generated result with native tools after the semantic choice;
  `pkgcheck` can expose a bad skeleton but does not choose the correct one.
