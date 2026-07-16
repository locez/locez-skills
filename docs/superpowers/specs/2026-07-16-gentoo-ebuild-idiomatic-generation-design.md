# Gentoo Ebuild Idiomatic Generation Design

## Objective

Improve `gentoo-ebuild` as a semantic code-generation guide for ebuilds. The
skill should infer a package profile from source and package evidence, select
the normal Gentoo eclass and phase shape for that profile, and then generate
the smallest idiomatic ebuild. Native tools remain the validation surface.

The `gentoo-tree-lessons` corpus is evidence for discovering reusable
patterns, not a runtime database or an instruction list. A lesson is promoted
only when its behavior is repeatable across unrelated packages, supported by
an eclass contract or current-tree precedent, and explainable by a stable
packaging concern.

## Scope

The change is a protocolization refactor. The existing task workflows for new
packages, bumps, QA, eclass discovery, and PR preparation remain in place.
The missing dimension is package shape:

- operation: new package, bump, revision, live update, QA/review;
- artifact mode: release source, live source, prebuilt/binary;
- ecosystem and build system: Python, C/C++, Rust, Go, Java, Perl, CMake,
  Meson, Autotools, and related native systems;
- runtime role: library, executable, plugin, service, kernel module, desktop
  integration, or build-only tool;
- integration and portability: systemd, udev, multilib, ABI, implementation
  selection, and optional features;
- test mode: enabled, selectively disabled, or restricted with a reason.

These fields are transient reasoning inputs. They are not persisted as package
records and are not intended to become a knowledge-base schema.

## Recommendation Model

Recommendations have three levels:

1. Default: the normal code shape when the package profile matches.
2. Conditional: a choice selected by an explicit source or runtime signal.
3. Exception: a deviation that requires evidence and a short reason.

Evidence is ordered as follows:

1. target repository policy and the target package;
2. same-project and same-family package precedent;
3. current local main-tree examples;
4. local eclass implementation and official Gentoo documentation;
5. recurrence in the main tree as a candidate signal;
6. mined lessons and generic memory.

Frequency can nominate a default, but cannot make an eclass universal. For
example, `git-r3` is common but is a live-source choice, while `systemd` is a
runtime integration choice only when the package installs or uses a systemd
unit.

## Code-Generation Protocol

For every non-trivial ebuild edit:

1. Inspect package and upstream build signals before choosing an eclass.
2. Write a compact package profile in working notes.
3. Select the default eclass and identify the eclass-owned variables and
   phase helpers.
4. Generate the conventional skeleton: EAPI, compatibility variables,
   pre-inherit variables, inherit order, source handling, dependencies, and
   only the phases that need package-specific behavior.
5. When overriding an exported phase, preserve the documented eclass phase
   chain and call the eclass helper at the appropriate point.
6. Add an exception only when source evidence, package precedent, repository
   policy, or an eclass contract requires it.
7. Run Manifest, pkgcheck, build/install checks, and the copyright helper as
   mechanical validation. These tools must not be treated as the source of
   semantic packaging decisions.

The generated ebuild should prefer eclass-owned behavior over hand-written
equivalents, direct dependencies over copied transitive dependencies, narrow
test restrictions over blanket disabling, and root-cause fixes over QA
suppression.

## Initial Domain Coverage

The first references should encode these stable defaults and their exception
signals:

- Python distributions: `distutils-r1`, `pypi`, PEP 517 selection,
  extensions, and the distinction between `python-r1`, `python-single-r1`,
  and `python-any-r1`.
- Native builds: `cmake`, `meson`, and `autotools`, including standard phase
  helpers and the boundary between build-system behavior and package-specific
  arguments.
- Rust and Go: `cargo`/`go-module`, module metadata, vendoring, and source
  layout decisions owned by the eclass.
- Java and Perl: `java-pkg-2`, `java-pkg-simple`, and `perl-module` based on
  the actual build model rather than language-name matching alone.
- Package modes and integrations: release versus live, source versus
  prebuilt, systemd/udev, multilib, ABI, and service or desktop installation.

## Pressure Scenarios

The refactor is successful when the skill can answer these scenarios without
turning frequency into an unconditional rule:

- A PyPI package using a declared PEP 517 backend and compiling an extension
  selects the corresponding `distutils-r1`/`pypi` shape, places required
  variables before inherit, and preserves the eclass preparation phase when
  adding a package-specific step.
- A Python utility used only during build does not get a runtime Python
  implementation dependency merely because it is Python; the profile selects
  `python-any-r1` when the source and installed files support that choice.
- A CMake package with a systemd unit uses `cmake_src_configure` and
  `cmake_src_install`, adds systemd integration only when the unit is
  installed, and does not inherit unrelated helpers solely because they are
  frequent in the tree.
- A `9999` package and its release ebuild keep live `git-r3` source handling
  separate from release distfile handling.
- A Java package with a real upstream build system is not reduced to
  `java-pkg-simple`; the simple eclass is selected only when its stated input
  model matches.
- A mined lesson that appears once, contains a package-specific workaround,
  or conflicts with the current eclass contract is not promoted to a default.

## Non-Goals

- No lesson database, package-frequency index, retrieval script, or workflow
  driver.
- No attempt to encode every current-tree package as a template.
- No replacement for target repository policy, eclass source inspection, or
  native Gentoo validation.
- No automatic semantic decisions made by shell or Python scripts.

## Planned Files

- Extend `gentoo-ebuild/SKILL.md` with profile routing and the generation
  protocol.
- Add a core preference reference and a domain-routing reference.
- Add focused domain references only for the initial coverage above.
- Update `eclass-discovery.md` so an eclass decision includes the generated
  skeleton and exception conditions.

