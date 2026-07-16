# Package Modes And Integrations

Use this reference when source mode, artifact format, installed integration,
or ABI behavior changes the ebuild skeleton.

## Release And Live

- A release ebuild normally uses the upstream release archive, stable source
  layout, release keywords, and release-specific patches.
- A `9999` ebuild normally uses live source handling such as `git-r3` only
  when the repository and package policy require it.
- Keep release and live source branches separate. Do not copy `EGIT_*` logic
  into a release ebuild or use a live ebuild as the automatic bump template.
- Validate a new release before removing an old version. Keep `9999` unless
  live behavior is explicitly being replaced.

## Prebuilt And Binary

For `-bin` and vendor-provided binaries, inspect architecture names, archive
layout, bundled libraries, RPATH/interpreter paths, stripping state, install
paths, and redistribution terms. Decide `RESTRICT`, `QA_PREBUILT`, or a
patch only from the actual files and repository policy. The package name alone
does not prove that a QA exception is correct.

Prefer the smallest install phase that preserves the vendor layout and Gentoo
paths. Do not add a source-build eclass to a binary package just because the
upstream project also publishes source.

## Services And Hardware Rules

Add `systemd` when the ebuild uses its unit-directory helpers or other
systemd-owned behavior. Add `udev` when the ebuild installs udev rules or hwdb
data and needs its directory/reload helpers. A daemon or hardware-facing
program is not enough by itself.

Typical integration shape:

```bash
inherit systemd udev

src_install() {
	default
	systemd_dounit "${FILESDIR}"/example.service
	udev_dorules "${FILESDIR}"/99-example.rules
}

pkg_postinst() {
	udev_reload
}

pkg_postrm() {
	udev_reload
}
```

Only include the functions that correspond to installed files. If upstream
already installs a unit or rule correctly, verify the image before duplicating
it in the ebuild. For hwdb files, keep the same `udev` ownership but use
`udev_hwdb_update` in `pkg_postinst` and `pkg_postrm` in addition to any
required `udev_reload`; `udev_reload` alone does not rebuild the hwdb binary.

## Multilib And ABI

Use a multilib eclass only when the package has a real multi-ABI build/install
model and current package precedent supports it. Identify whether the package
is a library, plugin, executable, or mixed output before choosing. Do not add
`multilib-minimal` because it is common in a language/build-system family.
When `multilib-minimal` is the chosen contract, inherit it last, implement
ABI-specific work in `multilib_src_configure`, `multilib_src_compile`,
`multilib_src_test`, and `multilib_src_install`, and put shared output in
`multilib_src_install_all`. For in-source builds, follow the eclass contract
for `multilib_copy_sources` and `ECONF_SOURCE` instead of inventing a second
ABI loop. Keep ABI-sensitive dependencies and install paths explicit.
