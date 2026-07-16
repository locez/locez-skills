# Gentoo Ebuild Idiomatic Generation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (recommended) or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `gentoo-ebuild` so ebuild generation follows evidence-backed Gentoo defaults for a package profile while keeping scripts limited to mechanical validation.

**Architecture:** Keep `SKILL.md` as a short orchestrator. Add references for cross-cutting semantic preferences, profile routing, Gentoo shell idioms, and focused references for Python, native builds, Rust/Go, Java/Perl, GUI/desktop, and release/live/binary modes. Update eclass discovery so every eclass choice produces a generated skeleton and an exception condition. Keep package-specific evidence and repository policy authoritative.

**Tech Stack:** Markdown skill references, existing Python copyright helper, `quick_validate.py`, `unittest`, `rg`, `git diff --check`; no new semantic scripts or package database.

---

### Task 1: Preserve RED pressure scenarios

**Files:**
- Create: `gentoo-ebuild/tests/semantic-generation-scenarios.md`
- Reference: `docs/superpowers/specs/2026-07-16-gentoo-ebuild-idiomatic-generation-design.md`

- [ ] **Step 1: Record the three baseline prompts and failures**

  Add scenarios for: a PyPI PEP 517 extension package; a CMake release bump with
  systemd and a separate `9999`; and Java/Gradle plus Perl eclass selection.
  Each scenario must record the baseline weakness observed by the RED run:
  the current skill requires evidence but does not provide a domain decision
  matrix or canonical generated skeleton.

- [ ] **Step 2: Define pass criteria before editing the skill**

  Require each future run to identify a package profile, select an eclass from
  source/build signals, state the normal phase/helper shape, classify direct
  dependencies, and name the exception that would change the default. Require
  release/live separation and prohibit copying dependencies or inheriting an
  eclass solely from language frequency.

- [ ] **Step 3: Review the scenario file for non-goals**

  Confirm it contains no package index, lesson records, execution script, or
  requirement to make semantic decisions with shell/Python automation.

### Task 2: Add cross-cutting semantic generation rules

**Files:**
- Modify: `gentoo-ebuild/SKILL.md`
- Create: `gentoo-ebuild/references/semantic-generation.md`

- [ ] **Step 1: Add the semantic route to the entrypoint**

  In `SKILL.md`, keep the existing task routing and add one sentence requiring
  a package profile before eclass/phase generation. Link to
  `references/semantic-generation.md` and `references/domain-routing.md`.
  Keep the entrypoint concise and preserve the existing native-tool boundary.

- [ ] **Step 2: Define the profile-to-skeleton protocol**

  In `semantic-generation.md`, document the transient profile fields:
  operation, artifact mode, ecosystem/build system/backend, runtime role,
  desktop/toolkit integrations, ABI/implementation selection, and test mode.
  Define the sequence:
  inspect signals, choose eclass contract, generate standard skeleton, add
  only evidenced overrides, then mechanically validate.

- [ ] **Step 3: Encode default/conditional/exception wording**

  State that a default applies only when its profile signals match; a
  conditional choice requires an explicit source/runtime signal; and an
  exception needs evidence plus a short reason. Make frequency a candidate
  signal rather than a universal rule.

- [ ] **Step 4: Add global code-generation preferences**

  Cover eclass-owned phases, variables-before-inherit contracts, phase-chain
  preservation, direct dependency classification, minimal custom phases,
  selective test handling, root-cause fixes, no blanket QA suppression, and
  Gentoo shell helpers for install/patch/build/toolchain operations. Document
  Portage's `E_*` dependency accumulation so generated ebuilds do not duplicate
  eclass-owned outputs or use `BDEPEND="${BDEPEND}"` to preserve them.
  Explicitly say scripts validate mechanics and do not choose semantics.

### Task 3: Add domain routing and default eclass choices

**Files:**
- Create: `gentoo-ebuild/references/domain-routing.md`
- Create: `gentoo-ebuild/references/python.md`
- Create: `gentoo-ebuild/references/native-builds.md`
- Create: `gentoo-ebuild/references/rust-go.md`
- Create: `gentoo-ebuild/references/java-perl.md`
- Create: `gentoo-ebuild/references/gui-desktop.md`
- Create: `gentoo-ebuild/references/shell-idioms.md`

- [ ] **Step 1: Build a signal-to-domain matrix**

  Map source files and package behavior to candidate domains: `pyproject.toml`
  and Python distributions; `CMakeLists.txt`, `meson.build`, or Autotools;
  Cargo/Go module metadata; Java build files; Perl distribution metadata;
  live git sources; prebuilt archives; services and udev rules. State that
  build-system signals outrank language-name guesses.

- [ ] **Step 2: Document Python backend preferences and exceptions**

  Prefer `distutils-r1` for Python distribution lifecycle behavior and `pypi`
  for PyPI release source handling when the source matches. Map the declared
  PEP 517 backend to `setuptools`, `flit-core`, `flit-scm`, `hatchling`,
  `jupyter-packaging`, `poetry-core`, `pdm-backend`, `meson-python`,
  `scikit-build-core`, `maturin`, `sip`, `pbr`, or `uv-build` instead of
  choosing by popularity.
  Require `DISTUTILS_USE_PEP517` before inherit when needed and
  `DISTUTILS_EXT=1` for extension modules. Choose `python-any-r1`,
  `python-single-r1`, or `python-r1` from runtime/implementation semantics.
  Require eclass helper calls when overriding phases.

- [ ] **Step 3: Document native build defaults and exceptions**

  Select `cmake`, `meson`, or `autotools` from the actual build files and
  behavior. Prefer standard helpers such as `cmake_src_configure` and
  `cmake_src_install`; use package-specific argument variables for local
  options. Do not inherit helper eclasses merely because they are frequent.

- [ ] **Step 4: Document Rust and Go defaults**

  Use `cargo` or `go-module` when module metadata and source layout match the
  eclass contract. Distinguish vendored releases, dependency tarballs, live
  `go-module_live_vendor`, and legacy `EGO_SUM`/proxy handling. Let the eclass
  own vendoring/module layout and dependency setup. Treat custom vendoring,
  generated code, and network access as evidence-driven exceptions.

- [ ] **Step 5: Document Java and Perl boundaries**

  Treat Java as ecosystem context and Gradle/Maven/Ant or simple sources as
  the build-model signal. Use `java-pkg-simple` only for its simple-source
  model; retain the upstream build system when that is the package behavior.
  When no generic upstream-build eclass applies, generate a `java-pkg-2`
  plus verified offline build-command and `java-pkg_dojar`/`java-pkg_dowar`
  install skeleton. Use `perl-module` for Perl module distributions when its
  build model fits; do not infer dependencies from a sibling package.

- [ ] **Step 6: Document GUI/desktop routing**

  Create `gui-desktop.md` to separate toolkit, primary build system, desktop
  files/icons/MIME/GSettings integration, and display-dependent tests. Cover
  `ecm`, `qt5-build`/`qt6-build`, `qmake-utils`, `gnome2`, `desktop`, `xdg`,
  and `virtualx` only under their actual contracts.

### Task 4: Add Gentoo shell idioms

**Files:**
- Create: `gentoo-ebuild/references/shell-idioms.md`
- Modify: `gentoo-ebuild/SKILL.md`
- Modify: `gentoo-ebuild/references/semantic-generation.md`
- Modify: `gentoo-ebuild/references/eclass-discovery.md`

- [ ] **Step 1: Map common operations to native helpers**

  Prefer `doins`/`newins`, `dobin`/`doexe`, `dodoc`/`doman`/`doicon`,
  `fperms`/`fowners`, `eapply`, `econf`/`emake`, `tc-get*`, version/USE
  helpers, and integration helpers over raw `cp`, `chmod`, `./configure`,
  `make`, or hard-coded compiler/path commands.

- [ ] **Step 2: Define raw-shell exceptions**

  Allow raw shell for source-tree transforms, generated files, or documented
  eclass gaps only when the correct phase/path variables and failure handling
  are explicit. Require `die` for required failures and forbid silent
  `|| true` suppression.

### Task 5: Add package-mode and integration preferences

**Files:**
- Create: `gentoo-ebuild/references/package-modes.md`
- Modify: `gentoo-ebuild/references/eclass-discovery.md`

- [ ] **Step 1: Encode release/live separation**

  Require release ebuilds to use release artifacts and `9999` ebuilds to use
  live source handling such as `git-r3` when justified. Do not use a live
  ebuild as an automatic template for a release bump or remove `9999` during
  old-version cleanup.

- [ ] **Step 2: Encode source/prebuilt and integration checks**

  For `-bin` or other prebuilt packages, route through architecture, bundled
  library, RPATH, install-path, redistribution, and QA checks. Add `systemd`
  or `udev` behavior only when the package actually installs the corresponding
  files; use `udev_hwdb_update` for hwdb data. Treat multilib/ABI as a profile
  signal, not a popularity rule, and generate `multilib_src_*` plus
  `multilib_src_install_all` under the `multilib-minimal`-last contract.

- [ ] **Step 3: Extend eclass decision records**

  Update `eclass-discovery.md` so the decision record includes package
  profile, candidate eclasses, contract evidence, selected skeleton, rejected
  alternatives, exception trigger, and remaining uncertainty. Keep it as
  working notes or final-report content rather than a persistent database.

### Task 6: Integrate with existing task references

**Files:**
- Modify: `gentoo-ebuild/references/workflow.md`
- Modify: `gentoo-ebuild/references/new-package.md`
- Modify: `gentoo-ebuild/references/version-bump.md`
- Modify: `gentoo-ebuild/references/qa.md`

- [ ] **Step 1: Add profile inference before editing barriers**

  In the workflow, require profile inference during evidence gathering and
  require the semantic decision before package edits. Keep edits, Manifest,
  and QA serial.

- [ ] **Step 2: Add domain references at the relevant task points**

  New-package intake must inspect build metadata and runtime files before
  drafting. Version bumps must re-run profile inference when build system,
  source mode, service layout, or language behavior changes. QA must distinguish
  a wrong skeleton/eclass contract from a mechanical warning.

- [ ] **Step 3: Remove any wording that suggests scripts decide packaging**

  Preserve the copyright helper and native commands, but state that they only
  validate or repair deterministic mechanics after semantic generation.

### Task 7: Verify and refactor

**Files:**
- Verify: `gentoo-ebuild/SKILL.md`
- Verify: `gentoo-ebuild/references/*.md`
- Verify: `gentoo-ebuild/tests/semantic-generation-scenarios.md`

- [ ] **Step 1: Run structural and existing tests**

  Run:

  ```bash
  python3 <skill-creator-root>/scripts/quick_validate.py gentoo-ebuild
  python3 -m unittest discover -s gentoo-ebuild/scripts -p 'test_*.py'
  git diff --check
  ```

  Expected: the skill validator reports `Skill is valid!`, all existing unit
  tests pass, and `git diff --check` is silent.

- [ ] **Step 2: Run semantic reference checks**

  Use `rg` to confirm every pressure scenario has a linked default, signal,
  exception, and mechanical-validation boundary. Confirm no new reference
  says frequency alone mandates an eclass, no domain guide copies a package
  dependency list, and no script is assigned semantic responsibility.

- [ ] **Step 3: Review token and navigation cost**

  Check `SKILL.md` remains an entrypoint rather than a long domain manual,
  each new reference has one responsibility, and links are discoverable from
  the entrypoint or existing workflow. Remove redundant prose before final
  verification.

- [ ] **Step 4: Record final verification and residual risk**

  Report exact commands and results. Explicitly note that semantic compliance
  was reviewed against the pressure scenarios, while actual package builds
  were not run because this change edits the skill rather than a package.
