# Rust And Go Packages

Use module metadata and source layout as the primary signal. Both ecosystems
commonly require offline dependency material, so the generated ebuild must
make the dependency source explicit before any build phase is written.

## Rust

Use `cargo` when the package is built from Cargo metadata. Inspect
`Cargo.toml`, `Cargo.lock`, workspace members, vendored crates, and any git
crates. The normal shape uses `CRATES`/`CARGO_CRATE_URIS` or the repository's
current equivalent and lets `cargo_src_unpack`, `cargo_src_configure`,
`cargo_src_compile`, `cargo_src_test`, and `cargo_src_install` own the common
phases.

Use `myfeatures` or the documented helper arguments for feature selection.
Only add custom `--package`, `--bin`, path, or frozen arguments when the
workspace or live-source layout requires them. Do not make Cargo fetch the
network during a normal build. Treat `CRATE_PATHS_OVERRIDE`, git crates, and
live vendoring as explicit exceptions that need source and version evidence.

## Go

Use `go-module` when the top-level source has `go.mod`. Prefer a dependency
tarball for non-vendored release modules according to the current eclass
documentation; `EGO_SUM` is a legacy/deprecated mode in the current tree.
When `go-module` is inherited, let it verify modules and establish the offline
module environment.

Choose the source branch explicitly:

| Source signal | Default shape | Exception boundary |
| --- | --- | --- |
| Release archive contains `vendor/` | `inherit go-module`; keep the eclass `src_unpack` path | Do not add a dependency tarball or run a second vendoring step |
| Release archive lacks `vendor/` | Add the eclass dependency tarball and keep `go-module_src_unpack` as the unpack path | Do not let `go` download modules during build |
| Live source lacks `vendor/` | `git-r3_src_unpack`, then `go-module_live_vendor` in `src_unpack` | `go-module_live_vendor` is only for live ebuilds and only before build phases |
| Existing ebuild still uses `EGO_SUM` | Treat it as migration debt; call `go-module_set_globals` in global scope and use the eclass proxy path | If custom `src_unpack` is unavoidable, call `go-module_setup_proxy` exactly as documented; do not introduce this mode for a new ebuild |

If a custom `src_unpack` is needed for signatures or live/release branching,
call `go-module_src_unpack` for the release branch unless the eclass contract
requires the legacy proxy helper directly. Do not confuse
`go-module_setup_proxy` with the normal dependency-tarball path.

Go binaries are often statically linked. Inspect and include the licenses of
statically linked dependencies; do not assume the main project's license is
the complete `LICENSE` value.

## Exceptions

Stop and inspect more evidence when the source mixes Cargo and Go, uses a
workspace with several installable targets, vendors only part of its graph,
requires generated code, or uses live git dependencies. Do not invent a
generic Rust/Go wrapper or copy another package's module list.
