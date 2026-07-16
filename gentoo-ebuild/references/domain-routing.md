# Domain Routing

Use the strongest source signal to select a domain reference. The table is a
route to inspect an eclass contract, not a replacement for that inspection.

| Source or behavior signal | Default route | Do not infer from this alone |
| --- | --- | --- |
| `pyproject.toml` `[build-system]`, Python distribution metadata, Python modules/extensions | `python.md` | backend substitution or `python-any-r1` versus `python-single-r1` versus `python-r1` |
| `CMakeLists.txt` and CMake install/configure behavior | `native-builds.md` | `systemd`, `udev`, or multilib integration |
| `meson.build` and Meson options | `native-builds.md` | a custom configure phase |
| `configure.ac`, `configure.in`, `Makefile.am`, or autoreconf need | `native-builds.md` | whether autoreconf is required for every release |
| `Cargo.toml`, `Cargo.lock`, or vendored crates | `rust-go.md` | network access or a hand-written vendoring scheme |
| `go.mod`, `go.sum`, or Go module cache | `rust-go.md` | runtime dependencies from imports alone |
| Java sources plus Gradle/Maven/Ant build files | `java-perl.md` | `java-pkg-simple` |
| Java sources without upstream build instructions | `java-perl.md` | correct source roots and main class without inspection |
| `Makefile.PL`, `Build.PL`, or Perl distribution metadata | `java-perl.md` | dependencies copied from another Perl package |
| `9999` version or explicit git snapshot | `package-modes.md` | using git source logic in a release ebuild |
| `-bin` name or vendor archive with executables/libraries | `package-modes.md` | architecture, RPATH, and redistribution assumptions |
| installed systemd units or udev rules | `package-modes.md` | inheriting the integration eclass only for its name |
| Qt/GTK/GNOME/KDE libraries, `.desktop` files, icons, MIME or GSettings data | `gui-desktop.md` | toolkit eclass, XDG hooks, and GUI test display are separate decisions |

## Selection Rules

1. Identify the primary build owner first: Python distribution, native build
   system, module ecosystem, or a simple install model.
2. Add integration eclasses only when installed files or build flags require
   their behavior. `systemd` and `udev` are integration helpers, not generic
   markers for daemon-like or hardware-related software.
3. Treat helper eclasses such as `flag-o-matic` and `toolchain-funcs` as
   conditional support. Their high recurrence does not make them a default
   part of every package skeleton.
4. If multiple domains apply, read each candidate eclass and inspect packages
   that combine them before deciding inherit order and phase ownership.
5. When a source signal is missing or contradictory, keep the choice unknown
   and continue evidence gathering instead of selecting by frequency.

For GUI packages, identify the toolkit/framework and primary build system
separately. A Qt or GTK application normally keeps `cmake` or `meson` as the
build owner; `desktop`, `xdg`, `virtualx`, `ecm`, and `qt*-build` are selected
only when their narrower contracts match.
