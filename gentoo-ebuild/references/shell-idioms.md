# Gentoo Ebuild Shell Idioms

An ebuild is Bash, but it runs inside Portage and usually inherits eclass
contracts. Prefer the Portage/eclass helper that owns an operation because it
preserves `${D}`, `${ED}`, `${EPREFIX}`, cross-compilation, sandbox, QA, and
repository conventions. Raw shell is an exception for source-specific work,
not the default code-generation style.

## Intent To Helper

| Intent | Prefer | Raw form to avoid as the default |
| --- | --- | --- |
| install a regular file | `insinto` + `doins`, or `newins` | `mkdir -p "${D}/..."; cp ...` |
| install an executable | `dobin`, `dosbin`, `doexe`, or `newbin` | `cp` followed by `chmod +x` |
| install docs/manpages | `dodoc` or `doman` | hand-built `${D}` paths and `cp` |
| install icons or desktop menus | `doicon`, `newicon`, or `domenu` after `inherit desktop` | hand-built icon/application paths and `cp` |
| set installed ownership/permissions | `fowners`, `fperms`, `insopts`, `exeopts` | `chmod`/`chown` against the image |
| create directories/symlinks | `keepdir`, `dosym`, `dodir` where appropriate | `mkdir`/`ln` with guessed prefix paths |
| install services or hardware rules | `systemd_dounit`/`systemd_newunit` after `inherit systemd`; `udev_dorules`/`udev_newrules` after `inherit udev` | manually duplicating system directories |
| install desktop entries | upstream file with `domenu`, or `make_desktop_entry` after `inherit desktop` | hand-writing a duplicate `.desktop` file |
| declare or optionally ship license text | `LICENSE=` metadata; `dodoc`/`DOCS` only when the text carries user-relevant information beyond the metadata | `dolicense` or automatic license-file installation |
| apply patches | `PATCHES` and `eapply`/`default_src_prepare` | raw `patch` with an untracked path |
| configure/compile | `econf`, `emake`, and the build eclass helper | `./configure`, raw `make`, or manual DESTDIR plumbing |
| select toolchain programs | `tc-getCC`, `tc-getCXX`, `tc-getPKG_CONFIG`, and related helpers after `inherit toolchain-funcs` or a verified provider | hard-coded `gcc`, `g++`, or `pkg-config` |
| handle Gentoo versions/USE | `ver_cut`, `ver_rs`, `ver_test`, `use`, `usev`, `usex`, `has` | fragile string slicing or boolean guesses |

## Helper Availability And Ownership

The helper name alone does not make a command available. The following
providers and boundaries cover the helper families used by this skill:

| Helper family | Provider | Boundary |
| --- | --- | --- |
| `insinto`, `doins`, `newins`, `dobin`, `dosbin`, `doexe`, `newbin`, `dodoc`, `doman`, `fowners`, `fperms`, `insopts`, `exeopts`, `keepdir`, `dosym`, `dodir`, `eapply`, `econf`, `emake`, `default`, `die`, `nonfatal`, `einfo`, `ewarn`, `eqawarn`, `addread`, `addwrite`, `addpredict`, `ver_*`, `use*`, `has` | Portage | Core helpers are still subject to the selected EAPI; verify the target EAPI before using an EAPI-specific option or helper. |
| `doicon`, `newicon`, `domenu`, `make_desktop_entry` | `desktop.eclass` | Inherit `desktop` first. The current eclass supports EAPI 7, 8, and 9; `make_desktop_entry` has a changed option-style contract in EAPI 9. |
| `systemd_dounit`, `systemd_newunit`, `systemd_*` directory helpers | `systemd.eclass` | Inherit `systemd`; the current eclass supports EAPI 7 and 8. |
| `udev_dorules`, `udev_newrules`, `udev_reload`, `udev_hwdb_update` | `udev.eclass` | Inherit `udev`; the current eclass supports EAPI 7 and 8. Use reload/update calls only for files the package actually installs. |
| `gnome2_schemas_savelist`, `gnome2_schemas_update` | `gnome2-utils.eclass` or `gnome2.eclass` | Inherit the eclass that owns the schema lifecycle; the current helpers support EAPI 7 and 8. |
| `xdg_pkg_preinst`, `xdg_pkg_postinst`, `xdg_pkg_postrm` | `xdg.eclass`; `xdg_*_database_update` and `xdg_environment_reset` come from `xdg-utils.eclass` | Inherit `xdg` for package lifecycle hooks or `xdg-utils` for utility-only behavior; do not confuse either with the `desktop` file installer. |
| `cmake_src_*`, `cmake_use_find_package` | `cmake.eclass` | Inherit `cmake` and keep the eclass as the phase owner; the current eclass supports EAPI 8. |
| `meson_src_*`, `meson_use`, `meson_feature` | `meson.eclass` | Inherit `meson`; these helpers are not generic configure syntax and the current eclass supports EAPI 7 and 8. |
| `tc-get*` | `toolchain-funcs.eclass` | Inherit `toolchain-funcs` or verify that the selected eclass provides it transitively. |
| `python_gen_cond_dep` | `python-r1` or `python-single-r1` | Use only with the matching Python implementation contract; do not mix mutually exclusive implementation eclasses. |
| `python_gen_any_dep` | `python-r1` or `python-any-r1` | Use the any-implementation dependency helper only when the dependency is independent of the selected runtime implementation. |
| `python_foreach_impl` | `python-r1` | Use only for a multi-implementation package. |
| `python_setup` | `python-r1`, `python-single-r1`, or `python-any-r1` | Use the implementation contract selected by the eclass; do not call it as a substitute for the eclass's exported phases. |
| `distutils_enable_tests`, `distutils-r1_python_*` | `distutils-r1.eclass` | Inherit `distutils-r1`; preserve its pseudo-phase contract. The current eclass supports EAPI 8. |
| `java-pkg_dojar`, `java-pkg_dowar`, `java-pkg_dolauncher`, `eant` | `java-utils-2.eclass`, exposed by Java package eclasses such as `java-pkg-2` | Inherit the Java eclass that owns the package model; the current Java helpers support EAPI 8 and 9. |
| `cargo_src_*` | `cargo.eclass` | Inherit `cargo` and provide the offline crate source expected by its contract; the current eclass supports EAPI 8. |
| `go-module_*` | `go-module.eclass` | Inherit `go-module`; distinguish normal dependency-tarball use from the deprecated `EGO_SUM` proxy path and live-only vendoring. The current eclass supports EAPI 7, 8, and 9. |
| `multilib_src_*` | `multilib-minimal` or another verified multilib eclass | Inherit the multilib contract and use ABI pseudo-phases only for a real multi-ABI package; `multilib-minimal` currently supports EAPI 7 and 8. |
| `multilib_copy_sources` | `multilib-build.eclass` | Use only with the corresponding in-source multilib contract; `multilib-build` currently supports EAPI 7, 8, and 9. |
| `virtx` | `virtualx.eclass` | Inherit `virtualx`; the current eclass supports EAPI 7 and 8 and only belongs around tests that need Xvfb. |

`qt_use` is deliberately not a generic Qt helper. The current tree defines it
only in the `qt5-build.eclass`, which is marked `@DEAD` and restricted to
`dev-qt` split ebuilds; `qt6-build.eclass` does not provide it. For ordinary Qt
applications, use the primary build eclass's verified helper such as
`cmake_use_find_package` or `meson_*`, or inspect the current Qt application
precedent.

### License Metadata Versus Shipped Text

`dolicense` is not a current Portage helper. `LICENSE=` declares package
license metadata and must reflect the licenses that apply to installed or used
content. That metadata is independent of whether the upstream license text is
shipped in the package.

Do not install a `LICENSE` or `COPYING` file merely because it exists. Install
the text as ordinary documentation with `dodoc` or `DOCS` when it provides
information that a user of the installed package may need, such as:

- a mapping from bundled libraries, plugins, fonts, icons, or other components
  to their individual licenses;
- third-party copyright, attribution, or redistribution notices for content
  that the package actually installs or bundles;
- exceptions, additional terms, EULAs, or other conditions that a plain
  `LICENSE=` value cannot express;
- a vendor or binary bundle's user-facing license/notice information.

For a single-project package whose file is only a canonical MIT/GPL/BSD text,
keep the correct `LICENSE=` value and omit `dodoc LICENSE`. Do not copy source
license trees mechanically; select only the notice files relevant to installed
content. Gentoo's devmanual gives the same boundary: `dodoc COPYING` is usually
unnecessary, except when the file explains how different licenses apply to
different parts of the application.

Use the exact helper contract from the current eclass. For example, a
`cmake_src_install` call should remain the install owner, while an extra
`systemd_dounit` belongs beside it only when upstream CMake does not install
the unit.

## Phase And Error Semantics

- Use `default` or the eclass-exported phase helper before/after custom work
  according to the eclass contract; do not replace it silently.
- Use `die` for required command failures, `nonfatal` only for an operation
  whose failure is intentionally handled, and `einfo`/`ewarn`/`eqawarn` for
  user-visible diagnostics. Do not hide failures with `|| true`.
- Use `addread`, `addwrite`, or `addpredict` for a narrowly justified sandbox
  exception. Do not disable sandboxing or network policy globally to make a
  build pass.
- Quote paths and use Bash arrays for commands with optional arguments. Keep
  `${S}`, `${WORKDIR}`, `${T}`, `${D}`, and `${ED}` distinct; do not replace
  them with the current directory or a hard-coded `/usr` path.
- Use eclass-specific translators such as `meson_use`, `meson_feature`,
  `cmake_use_find_package`, `python_gen_cond_dep`, or `python_gen_any_dep`
  only after verifying their provider and the relevant syntax. `qt_use` is
  the narrow `qt5-build` exception described above, not a default for Qt
  applications.

## Raw Shell Exceptions

Raw `cp`, `mv`, `rm`, `sed`, `find`, `mkdir`, or `chmod` can still be correct
for source-tree patching, generated files, cleanup of files that upstream
cannot install correctly, or a documented eclass gap. Before using one, check
whether a Portage/eclass helper already owns the operation, use the correct
phase and path variable, and make failure handling explicit. The rule is not
"never use shell"; it is "do not make generic shell primitives stand in for a
Gentoo packaging helper."
