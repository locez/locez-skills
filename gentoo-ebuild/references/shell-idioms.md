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
| install docs/manpages/icons | `dodoc`, `doman`, `doicon`, `newicon`, `domenu` | hand-built `${D}` paths and `cp` |
| set installed ownership/permissions | `fowners`, `fperms`, `insopts`, `exeopts` | `chmod`/`chown` against the image |
| create directories/symlinks | `keepdir`, `dosym`, `dodir` where appropriate | `mkdir`/`ln` with guessed prefix paths |
| install services or hardware rules | `systemd_dounit`, `systemd_newunit`, `udev_dorules`, `udev_newrules` | manually duplicating system directories |
| install desktop entries | upstream file, or `make_desktop_entry` | hand-writing a duplicate `.desktop` file |
| apply patches | `PATCHES` and `eapply`/`default_src_prepare` | raw `patch` with an untracked path |
| configure/compile | `econf`, `emake`, and the build eclass helper | `./configure`, raw `make`, or manual DESTDIR plumbing |
| select toolchain programs | `tc-getCC`, `tc-getCXX`, `tc-getPKG_CONFIG`, and related helpers | hard-coded `gcc`, `g++`, or `pkg-config` |
| handle Gentoo versions/USE | `ver_cut`, `ver_rs`, `ver_test`, `use`, `usev`, `usex`, `has` | fragile string slicing or boolean guesses |

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
  `cmake_use_find_package`, `qt_use`, `python_gen_cond_dep`, or
  `python_gen_any_dep` when they own the relevant syntax.

## Raw Shell Exceptions

Raw `cp`, `mv`, `rm`, `sed`, `find`, `mkdir`, or `chmod` can still be correct
for source-tree patching, generated files, cleanup of files that upstream
cannot install correctly, or a documented eclass gap. Before using one, check
whether a Portage/eclass helper already owns the operation, use the correct
phase and path variable, and make failure handling explicit. The rule is not
"never use shell"; it is "do not make generic shell primitives stand in for a
Gentoo packaging helper."
