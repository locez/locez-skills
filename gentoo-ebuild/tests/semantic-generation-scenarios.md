# Semantic Generation Pressure Scenarios

These are human/subagent review scenarios for the semantic layer of the
`gentoo-ebuild` skill. They are deliberately not executable packaging
scripts. The existing Gentoo tools validate the generated result; these
scenarios validate whether the skill chooses an idiomatic shape before those
tools run.

## RED Baseline

The scenarios were run against the pre-refactor skill with its existing task
references only. The agents generally followed the evidence-first workflow,
but all three exposed the same missing layer: the skill did not provide a
domain decision matrix or a canonical generated skeleton.

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

## GREEN Acceptance Criteria

For every scenario, the skill must make the agent produce all of the
following before editing an ebuild:

1. A compact package profile derived from source and installed-runtime
   signals.
2. A default eclass/build-system choice with the contract that justifies it.
3. The normal variable order and phase/helper skeleton.
4. Direct dependency classification into build, compile/link, runtime, test,
   optional, or eclass-owned requirements.
5. An explicit exception signal that would change the default.
6. A statement that frequency and similar-package precedent are evidence, not
   permission to copy behavior or dependencies.
7. A mechanical validation sequence that does not make semantic decisions.

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
- A copied dependency list is justified only by a similar package.
- A release ebuild reuses live source logic or deletes `9999` as cleanup.
- `pkgcheck` or a helper script is treated as the authority for eclass or
  dependency semantics.

