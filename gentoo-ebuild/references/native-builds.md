# Native Build Systems

Select the primary build eclass from the files and commands the release
actually uses. Do not select `cmake`, `meson`, or `autotools` because the
project merely contains C or C++ code.

## CMake

Use `cmake` when CMake is the package's build and install owner. The eclass
provides out-of-source builds and exports the standard prepare, configure,
compile, test, and install phases. The normal custom shape is:

```bash
inherit cmake

src_configure() {
	local mycmakeargs=(
		-DPROJECT_OPTION=OFF
	)
	cmake_src_configure
}

src_install() {
	cmake_src_install
	# add only files not installed by upstream CMake
}
```

Set pre-inherit variables such as `CMAKE_MAKEFILE_GENERATOR` before inherit.
Use the eclass's `mycmakeargs` convention for package options. Keep
`src_prepare` and `src_install` overrides only when patches or install assets
are not handled by the CMake project.

## Meson

Use `meson` when `meson.build` is the active build description. Put feature
options in the `emesonargs` array and finish with `meson_src_configure`.
Prefer `meson_src_install` and `meson_src_test` over manually invoking Meson.
The same rule applies to cross and native files: use the eclass helpers and
inspect the package precedent when the project needs a custom machine file.

## Autotools

Use `autotools` when the package needs autoreconf/autotool regeneration or the
eclass's tool-version and helper behavior. A project with a pre-generated
`configure` script does not automatically need `autotools`; verify whether
the release contains the generated files and whether Gentoo must regenerate
them. Use the normal `econf`, `emake`, and `default` phases unless the source
requires a documented preparation step.

## Cross-Cutting Rules

- If several build descriptions exist, identify which one the release and
  package precedent actually use before inheriting multiple build eclasses.
- Use eclass-provided dependency variables and phase helpers instead of
  duplicating their build-tool dependencies.
- Keep USE-controlled feature arguments adjacent to the configure helper.
- If a build system installs a service, desktop file, or udev rule itself,
  verify the image before adding a second manual install path.
- Treat `flag-o-matic`, `toolchain-funcs`, and similar helpers as conditional
  support. Inherit them when their functions or variables are needed, not
  because they are common in the tree.
