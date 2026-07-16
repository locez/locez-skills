# GUI And Desktop Packages

GUI packaging has several independent dimensions: toolkit, build system,
desktop integration, and test display. Identify each before choosing eclasses.
The toolkit is not automatically the build owner.

## Package Profile

Inspect:

- toolkit/framework: Qt5, Qt6, GTK, GNOME, KDE/ECM, Wayland, X11, or a
  toolkit-neutral desktop application;
- build owner: CMake, Meson, Autotools, qmake, Python, Rust, or another
  system;
- installed integration: upstream `.desktop` files, icons, MIME handlers,
  GSettings schemas, portals, shell/session files, translations, and plugins;
- optional features: X11, Wayland, OpenGL, multimedia, printing, Qt modules,
  GTK/GNOME services, KDE frameworks, or hardware backends;
- test environment: headless, Xvfb/`virtualx`, Wayland compositor, or tests
  that must remain disabled with a source-level reason.

## Eclass Responsibilities

| Signal | Default preference | Boundary |
| --- | --- | --- |
| Qt application using CMake/Meson | Use the primary build eclass and declare the required Qt runtime/build dependencies | `qt5-build`/`qt6-build` are for their intended Qt split packages, notably `dev-qt`, not every Qt application |
| qmake project outside the Qt split packages | Use `qmake-utils`/current Qt helper precedent and the actual qmake wrapper | Do not hand-write compiler flags or inherit `qt*-build` by toolkit name alone |
| GNOME release archive hosted on `gnome.org` | Use `gnome.org` for the release `SRC_URI`/`S` contract, then choose the actual build eclass | `gnome.org` is source-archive handling; it does not make `gnome2` or `meson` the build owner |
| KDE application/library using ECM | Prefer `ecm` when the source uses ECM/KDE CMake modules or current KDE-family precedent matches; use the matching KDE source eclass only for the upstream release family | `ecm` owns a CMake-based phase model; do not mix incompatible phase owners casually |
| GNOME/Gtk package with the legacy GNOME eclass model | Use `gnome2` when its exported phases and source conventions match | A GTK dependency alone does not justify `gnome2`; modern Meson packages may use `meson` plus narrower GNOME helpers |
| GSettings/GConf schemas or GNOME icon/cache updates without the legacy `gnome2` phase model | Use `gnome2-utils` helpers such as `gnome2_schemas_savelist`/`gnome2_schemas_update` when their installed files require them | `gnome2-utils` is helper-only; it does not replace the primary build eclass or justify `gnome2` |
| valid upstream `.desktop`/icon/MIME files | Install or minimally patch the upstream files, then use `xdg` for lifecycle updates when required | Do not generate a duplicate desktop file with `make_desktop_entry` |
| no usable upstream desktop file | Use `desktop` and `make_desktop_entry`, with `doicon`/`newicon` for icons; usually pair with `xdg` when installed desktop/icon/MIME data needs cache updates | Generate only from the installed command, app ID, icon path, categories, and actual optional features |
| tests require an X display | Use `virtualx` with `VIRTUALX_REQUIRED=test` or the package's existing conditional | A GUI package does not imply a display dependency for all builds or tests |

`xdg.eclass` owns package preinst/postinst/postrm handling for installed
desktop, icon, and MIME files. If a package overrides those phases, preserve
the `xdg_*` helper calls or the corresponding eclass phase chain. Use
`xdg-utils` directly only when its helper-only contract is what the package
needs. `desktop` generates entries and installs icons; it does not replace the
toolkit or build eclass. The two are often paired when the ebuild generates a
desktop entry, but verify the package's actual installed metadata and current
precedent.

## Generated Shape

For an ordinary CMake desktop application with valid upstream desktop assets,
the skeleton is normally the build eclass plus `xdg`, not every GUI eclass:

```bash
inherit cmake xdg

src_configure() {
	local mycmakeargs=(
		$(cmake_use_find_package wayland Wayland)
		$(cmake_use_find_package opengl OpenGL)
	)
	cmake_src_configure
}
```

The exact USE flags and CMake package names must come from the source and
current package family. Add `desktop` only if the ebuild creates or repairs a
desktop entry, and add `virtualx` only when the test command requires an X
display. A test that needs a Wayland compositor requires its own supported
test environment and should not be forced through `virtualx`.

## Runtime And QA Checks

- Verify each desktop `Exec` target exists in the image and does not contain
  build-tree paths or unsupported wrapper assumptions.
- Verify the desktop ID, icon names/paths, MIME associations, and optional
  feature conditions together; a file installing successfully is not enough.
- Put toolkit libraries and direct runtime integrations in `RDEPEND`, header
  and link requirements in `DEPEND`, and build/test display tools in
  `BDEPEND` or the relevant conditional.
- Validate desktop files and inspect the final `${D}` image. Do not silence
  desktop-file or installed-file QA to hide a wrong generated entry.

## Exceptions

Use a different skeleton when the package is a Qt/GNOME/KDE framework module,
a desktop portal/session component, a compositor/window manager, a GUI
library without an application entry, or a package that supports both GUI and
headless modes. In those cases, route the package family and build system
separately, then record which integration helpers own real behavior.
