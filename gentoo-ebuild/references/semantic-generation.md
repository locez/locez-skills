# Semantic Ebuild Generation

Use this reference before writing a non-trivial ebuild. It describes the
semantic decisions that produce the ebuild; `pkgdev`, `pkgcheck`, `ebuild`, and
the bundled copyright helper only validate or repair deterministic mechanics
after those decisions.

## Package Profile

Keep a compact profile in working notes. Do not create a persistent package
record. Capture only fields that affect the generated ebuild:

- operation: new package, release bump, revision, live update, or QA fix;
- artifact mode: release source, live source, prebuilt/binary, or generated
  source;
- ecosystem and build system: Python/PEP 517, CMake, Meson, Autotools, Rust,
  Go, Java, Perl, or another detected model;
- runtime role: library, executable, module, plugin, service, kernel module,
  desktop integration, or build-only tool;
- integration and portability: systemd, udev, multilib, ABI, implementation
  selection, optional features, and installed paths;
- test mode: runnable, selectively restricted, or unavailable with a reason.

The build model and installed behavior outrank the language name. For example,
Java plus Gradle is not automatically a `java-pkg-simple` package, and a C++
program is not automatically a reason to inherit a helper eclass.

## Generation Sequence

1. Inspect repository policy, the target package, upstream build metadata, and
   current eclass contracts.
2. Match the profile to a domain reference and choose the eclass that owns the
   relevant lifecycle behavior.
3. Generate the standard skeleton: EAPI, variables required before inherit,
   inherit order, source handling, package metadata, dependency classes, and
   only the necessary phase overrides.
4. Preserve the eclass phase chain when overriding an exported phase. Call the
   eclass helper at the documented point and keep package-specific work next
   to it.
5. Add an exception only when source evidence, package precedent, repository
   policy, or the eclass contract requires it. Record the reason in working
   notes or the final report.
6. Run mechanical validation after the semantic draft: copyright helper,
   Manifest, package QA, and build/install checks where feasible.

## Recommendation Levels

Use precise language so defaults do not become cargo cult:

- **Default:** use this shape when the listed profile signals are present.
- **Conditional:** choose it only when the stated source or runtime signal is
  present.
- **Exception:** deviate from the default only with evidence and a reason.
- **Unknown:** keep investigating; do not fill the gap with a popular eclass
  or a copied dependency list.

Main-tree frequency can nominate a default, but it cannot establish the
condition. Similar packages are useful for finding evidence, not for copying
their dependencies, USE flags, patches, or phase bodies without rechecking the
target source.

## Global Preferences

- Prefer eclass-owned variables, phases, and pseudo-phases over hand-written
  equivalents.
- Set variables marked pre-inherit before `inherit`; inspect the eclass when
  the ordering is not obvious.
- Keep custom phases minimal and use conventional helper names such as
  `cmake_src_configure`, `meson_src_install`, or an eclass-specific helper.
- Classify direct dependencies by build host (`BDEPEND`), compile/link
  (`DEPEND`), runtime (`RDEPEND`), post-install ordering (`PDEPEND`), test, or
  optional feature. Do not pad the graph with transitive dependencies.
- Enable tests by default when they are runnable. Prefer a narrow deselection
  or documented restriction with a root cause over disabling all tests.
- Fix source/build/install causes before using QA exceptions or suppression.
- Keep release and live source handling separate, and keep old versions while
  validating a bump unless repository policy says otherwise.

## Decision Record

For a non-obvious choice, use a short working-note record:

```text
Package profile: <operation>; <artifact>; <ecosystem/build>; <runtime role>
Signals: <files, metadata, installed behavior>
Default skeleton: <eclass>; <phase helpers>; <dependency shape>
Exception tested: <condition that would change the default>
Evidence: <target package, eclass contract, current examples>
Uncertainty: <what still needs confirmation>
```

