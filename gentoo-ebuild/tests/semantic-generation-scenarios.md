# Semantic Generation Pressure Scenarios

These are human/subagent review scenarios for the semantic layer of the
`gentoo-ebuild` skill. They are deliberately not executable packaging
scripts. The existing Gentoo tools validate the generated result; these
scenarios validate whether the skill chooses an idiomatic shape before those
tools run.

## RED Baseline

The original three scenarios were run against the pre-refactor skill with its
existing task references only. The agents generally followed the
evidence-first workflow, but exposed the same missing layer: the skill did not
provide a domain decision matrix or a canonical generated skeleton. The three
additional scenarios below were also run against the previous commit before
the corresponding references were added.

### Python distribution

Input profile: a PyPI release with `pyproject.toml`, a declared PEP 517
setuptools backend, a C extension, multiple supported Python implementations,
pytest tests, and a CLI entry point.

Observed baseline behavior:

- It proposed `distutils-r1` and the relevant Python variables, but described
  them as provisional because the skill did not name the Python contract.
- It left `PYTHON_COMPAT`, `DISTUTILS_USE_PEP517`, extension handling, test
  helpers, and phase helper names to further evidence gathering.
- It correctly identified likely wrong paths such as manually invoking
  `pip`/`setup.py`, looping implementations by hand, padding dependencies, or
  putting pytest in `RDEPEND`.

Missing behavior: a stable default skeleton and explicit conditions for
`python-any-r1`, `python-single-r1`, and `python-r1`.

The backend pressure case must also distinguish at least these source signals:

- `setuptools.build_meta` or legacy `setup.py` -> `setuptools`;
- `flit_core.buildapi`/`flit_scm:buildapi` -> `flit-core`/`flit-scm`;
- `hatchling.build`, `poetry.core.masonry.api`, or `pdm.backend` -> the
  matching backend key;
- `mesonpy`, `scikit_build_core.build`, or `maturin` -> the matching hybrid
  backend, with Meson/CMake/Rust vendoring inspected separately.

The agent must not substitute a more popular backend, add a Poetry/uv CLI just
because the project name mentions it, or use `standalone` without evidence.

Against the old skill, none of the backend selectors was deterministic. It
showed a `setuptools` example but did not map backend module paths to eclass
keys, leaving room for `setuptools` for every project, literal module paths in
`DISTUTILS_USE_PEP517`, or abandoning `distutils-r1` for hybrid backends.

### CMake release with live sibling

Input profile: a released CMake C++ package installs a systemd service; the
new release changes a CMake option and the service unit path; a separate
`9999` ebuild uses a git snapshot.

Observed baseline behavior:

- It kept release distfiles and `9999` git handling separate and preserved the
  old-version gate.
- It selected `cmake` only as a candidate and left the service integration,
  helper calls, and exact phase skeleton unresolved.
- It identified likely shortcuts: inheriting `systemd` by association,
  carrying stale CMake arguments, copying old dependencies, skipping install
  validation, or using the live ebuild as the release template.

Missing behavior: a default CMake phase shape and a conditional integration
rule saying when `systemd` owns real behavior.

### Java and Perl eclass boundaries

Input profile: one Java package uses Gradle; another is a standard Perl module
distribution. The pressure is to select familiar eclasses from language names
and copy dependencies from sibling packages.

Observed baseline behavior:

- It treated Gradle/build metadata and Perl distribution metadata as the
  controlling evidence rather than language names.
- It correctly treated `java-pkg-simple` and `perl-module` as candidates that
  require contract checks, and rejected copied dependency lists.
- It did not provide a concise default/exception rule for the generated Java
  or Perl skeleton.

Missing behavior: explicit boundaries for upstream build systems versus
simple Java compilation and Perl-specific module build behavior.

### GUI desktop application

Input profile: a Qt6 or GTK desktop application with CMake or Meson as its
build owner, upstream `.desktop` and icon files, optional Wayland/OpenGL
features, and tests that need an X display.

The old skill could route CMake or Meson, but could not distinguish Qt6 from
GTK, `ecm` from plain `cmake`, `qt6-build` from an ordinary Qt application,
`desktop` from `xdg`, or a display-dependent test needing `virtualx`. It left
optional Wayland/OpenGL dependencies and desktop-file ownership to guesswork.

The expected route is the primary build eclass plus the toolkit/runtime
dependencies, `xdg` for installed desktop/icon/MIME lifecycle handling when
needed, and `virtualx` only for display-dependent tests. `desktop` is added
only when the ebuild must create or repair a desktop entry. `qt6-build` is not
selected for an ordinary Qt application merely because it uses Qt; it is
reserved for its intended Qt split-package contract. KDE/ECM and GNOME
helpers are similarly conditional.

The generated ebuild must verify desktop `Exec`, app ID, icon paths, MIME
associations, USE-conditional toolkit features, and the final install image.

### Gentoo shell idioms

Input profile: a package needs to install an executable, a service unit, an
icon, and a generated configuration file, and needs a compiler and patch.

The old skill named some eclass helpers abstractly but did not map common
operations to `doins`, `dobin`, `doicon`, `eapply`, `econf`, `emake`, or
`tc-get*`. A generator could therefore fall back to raw `cp`, `mkdir`,
`chmod`, `./configure`, `make`, and host compiler names while still appearing
to follow the workflow.

The expected generated operations use `dobin`/`doexe`, `systemd_dounit`,
`doicon`/`newicon`, `insinto` + `doins`, `eapply`/`PATCHES`, `econf`/`emake`,
and `tc-get*` as appropriate. Raw `cp`, image-tree `mkdir`, `chmod`,
`./configure`, and hard-coded compiler names are exceptions requiring a
source/eclass reason. Required commands must fail with `die`; failures must
not be hidden with `|| true`.

### Portage eclass dependency accumulation

Input profile: an eclass sets dependency variables during `inherit`, while
the ebuild also declares its own `DEPEND`, `RDEPEND`, or `BDEPEND`. A Python
distribution uses `DISTUTILS_EXT=1` and `distutils-r1` as a concrete example.

The old skill said to let eclasses own dependencies but did not explain the
mechanism. An agent could therefore add `${PYTHON_DEPS}` to `DEPEND` even when
`distutils-r1` already supplies it, or write `BDEPEND="${BDEPEND}"` after
`inherit` believing that it preserves eclass dependencies.

The expected rule is that `inherit` evaluates eclass metadata into Portage's
accumulation channels such as `E_DEPEND`, `E_RDEPEND`, and `E_BDEPEND`; Portage
appends those channels to the ebuild's final dependency variables after
inherit processing. Ebuild code should declare only package-owned additions,
avoid duplicating eclass-owned dependencies, and avoid replacing generated
dependency variables without reading the eclass contract.

### Java upstream build fallback

Input profile: a pure-Java release ships a Gradle or Maven build, does not
match the source model of `java-pkg-simple`, and has a reproducible set of
Gentoo-provided or explicitly packaged offline dependencies.

The generated shape must keep the upstream build model, use `java-pkg-2` for
Java setup, invoke the verified offline build target, and install the actual
JAR/WAR with `java-pkg_dojar`/`java-pkg_dowar`. It must not invent a Gradle
eclass, let a wrapper download dependencies, or silently fall back to
`java-pkg-simple`.

### Go source modes

Input profile: one Go release contains `vendor/`, another needs a dependency
tarball, a `9999` source does not vendor dependencies, and an old ebuild still
uses `EGO_SUM`.

The generated shape must distinguish the eclass default unpack path, the
dependency-tarball path, live `go-module_live_vendor`, and the deprecated
`EGO_SUM`/`go-module_setup_proxy` migration path. It must not treat the proxy
helper as the normal dependency-tarball mechanism or permit network fetches.

### Multilib phase contract

Input profile: a library or plugin has a real multi-ABI build and current
precedent uses `multilib-minimal`.

The generated shape must inherit `multilib-minimal` last, use
`multilib_src_configure`/`multilib_src_compile`/`multilib_src_test`/
`multilib_src_install` for ABI-specific work, and use
`multilib_src_install_all` for shared output. It must not generate a manual
ABI loop or add multilib from frequency alone.

## GREEN Acceptance Criteria

For every scenario, the skill must make the agent produce all of the
following before editing an ebuild:

1. A compact package profile derived from source and installed-runtime
   signals.
2. A default eclass/build-system choice with the contract that justifies it.
3. The normal variable order and phase/helper skeleton.
4. The matching PEP 517 backend key when the package is a Python distribution,
   or a documented reason for `standalone`/`no`.
5. Direct dependency classification into build, compile/link, runtime, test,
   optional, or eclass-owned requirements.
6. Gentoo helper idioms for install, patch, build, permissions, toolchain, and
   integration operations.
7. An explicit exception signal that would change the default.
8. A statement that frequency and similar-package precedent are evidence, not
   permission to copy behavior or dependencies.
9. A mechanical validation sequence that does not make semantic decisions.
10. A source-mode or ABI branch whose phase contract is explicit when the
    profile requires one.
11. An explicit distinction between package-owned dependency additions and
    dependencies accumulated by inherited eclasses.

The agent must preserve release/live separation, call inherited phase helpers
when overriding exported phases, and avoid blanket test or QA suppression
without a root cause.

## REFACTOR Red Flags

If a future run produces any of these, the semantic references need another
clarifying rule:

- “This eclass is common, so inherit it” without a matching source signal.
- “It is Python/Java/Perl, so the language eclass is enough” while ignoring
  the build model or runtime role.
- A custom phase duplicates behavior owned by an eclass helper.
- A generated ebuild uses `cp`, `chmod`, or hard-coded compiler/build commands
  where a Portage/eclass helper owns the operation.
- A generated ebuild manually adds an eclass-owned dependency or treats
  `BDEPEND="${BDEPEND}"` as a way to preserve Portage's accumulated eclass
  dependencies.
- A copied dependency list is justified only by a similar package.
- A release ebuild reuses live source logic or deletes `9999` as cleanup.
- `pkgcheck` or a helper script is treated as the authority for eclass or
  dependency semantics.
