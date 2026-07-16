# Python Packages

Use this reference when the package is a Python distribution, contains Python
extensions, or needs Python only as a build/test tool. Read the current
`distutils-r1`, `pypi`, `python-any-r1`, `python-single-r1`, or `python-r1`
eclass before relying on a variable or helper.

## Default Selection

- For a Python distribution, prefer `distutils-r1` because it owns the Python
  build, install, implementation, and test phase behavior.
- Add `pypi` when the release is actually distributed by PyPI and the PyPI
  normalized project name/layout matches. Set `PYPI_PN` or
  `PYPI_NO_NORMALIZE` before inherit only when the upstream identity requires
  it.
- Set `DISTUTILS_USE_PEP517` before inherit when the project uses a supported
  PEP 517 backend. The value must match the backend declared by the source;
  do not guess it from the project name.
- Set `DISTUTILS_EXT=1` when the distribution builds compiled extension
  modules. Let the eclass add the associated build behavior and dependencies.

Typical release shape, after verifying the supported implementations and
backend:

```bash
EAPI=8

PYTHON_COMPAT=( python3_{12..14} )
DISTUTILS_USE_PEP517=setuptools
DISTUTILS_EXT=1

inherit distutils-r1 pypi
```

The exact `PYTHON_COMPAT` range, backend value, `S`, license, and keywords
still come from the target source and repository policy.

## Dependency Ownership

`distutils-r1` contributes Python implementation, backend, and build
dependencies through the Portage eclass accumulation mechanism. In
particular, `DISTUTILS_EXT=1` makes the eclass contribute `${PYTHON_DEPS}` to
`DEPEND`, while the eclass also contributes its normal Python/backend
requirements to `BDEPEND` and `RDEPEND`. Do not add `${PYTHON_DEPS}` manually
just because the package builds an extension, and do not use
`BDEPEND="${BDEPEND}"` after `inherit` to preserve eclass dependencies; that
does not refer to Portage's `E_BDEPEND` channel.

`DISTUTILS_OPTIONAL` is an explicit exception: it disables the eclass's
automatic dependency and phase behavior, so the ebuild must provide the
documented dependencies and call the required helpers itself.

## PEP 517 Backend Preference

Read `[build-system] build-backend` and its `requires` from
`pyproject.toml`. `DISTUTILS_USE_PEP517` should name the backend that the
release declares, using the current eclass key. Do not replace it with a more
familiar backend just because the project also has `setup.py` or because
`setuptools` is more common in the tree.

| Upstream backend signal | Default key | Use this shape when |
| --- | --- | --- |
| `setuptools.build_meta` or a legacy `setup.py` project | `setuptools` | setuptools metadata/build hooks own the distribution, including ordinary C/C++ extensions |
| `flit_core.buildapi` | `flit-core` | the project declares Flit Core and follows its package/module layout |
| `flit_scm:buildapi` | `flit-scm` | Flit is combined with VCS-derived versioning |
| `hatchling.build` | `hatchling` | Hatchling owns metadata/build hooks; let the eclass account for declared Hatch plugins |
| `jupyter_packaging.build_api` | `jupyter-packaging` | the project uses the Jupyter packaging backend and its release metadata requires it |
| `poetry.core.masonry.api` | `poetry-core` | the project declares Poetry Core; do not add the Poetry application just to build it |
| `pdm.backend` | `pdm-backend` | PDM's backend is declared and its project configuration is authoritative |
| `mesonpy` | `meson-python` | the Python wheel is built by Meson, commonly for a native extension; let `distutils-r1` coordinate its Meson integration |
| `scikit_build_core.build` | `scikit-build-core` | the Python distribution uses scikit-build-core to drive CMake; use backend arguments rather than a hand-written pip/CMake loop |
| `maturin` | `maturin` | a Rust/PyO3 or similar project declares Maturin; inspect Rust vendoring separately |
| `sipbuild.api` | `sip` | SIP/Qt bindings declare SIP as the backend |
| `pbr.build` | `pbr` | an OpenStack-style project declares pbr; its setuptools dependencies remain backend-driven |
| `uv_build` | `uv-build` | the project explicitly declares uv-build; do not substitute the uv CLI for the backend |

Use `standalone` only when the source carries a local backend or the eclass
contract explicitly requires it. Use `no` only for a verified non-PEP 517
build that needs the legacy path. For new ebuilds, prefer current keys such as
`flit-core` and `poetry-core` over deprecated aliases unless the target EAPI
and current package policy explicitly require an older spelling.

Backend-specific configuration follows the eclass contract:

- Use `DISTUTILS_ARGS` only where the selected backend supports it, such as
  documented setuptools, maturin, meson-python, scikit-build-core, or SIP
  arguments.
- Use `DISTUTILS_UPSTREAM_PEP517` when deliberately forcing a different
  backend and preserve the actual upstream backend for verification.
- Use `DISTUTILS_CONFIG_SETTINGS_JSON` only for a standalone backend.
- Let `distutils-r1` add backend/build-tool dependencies. Add direct project
  dependencies separately and only when the source uses them.

If the backend is unsupported, contradictory, or changed between releases,
mark the decision unknown and inspect the eclass/current package precedent
before writing a custom build path.

## Implementation Semantics

Choose the Python implementation contract from how the package is used:

- `python-any-r1`: Python is a build-time or test-time tool and does not
  affect installed runtime behavior. This is commonly an integration with a
  non-Python build system, not a replacement for `distutils-r1`'s distribution
  phases.
- `python-single-r1`: the installed package or tool selects one Python
  implementation and cannot be installed for several implementations at the
  same time.
- `python-r1`: the package has a multi-implementation runtime or module model
  and must account for each supported implementation.

`distutils-r1` already provides the `python-r1` contract. Setting
`DISTUTILS_SINGLE_IMPL` before inherit switches it to the `python-single-r1`
contract; preserve its exported `pkg_setup` behavior, or call
`python-single-r1_pkg_setup` from a custom `pkg_setup` when the eclass contract
requires it. Do not add a second Python implementation eclass by habit.

Do not combine mutually exclusive implementation eclasses by habit. Verify
the current eclass contract and nearby packages when a distribution has both
runtime Python code and build-time Python tools.

## Phase Shape

Let Portage's default unpack the release archive. `distutils-r1` owns the
normal prepare, configure, compile, test, and install phases. Add standard
helpers such as `distutils_enable_tests pytest` when the upstream tests are
runnable. If a package-specific pseudo-phase is necessary, call the eclass
helper rather than replacing it:

```bash
python_prepare_all() {
	# package-specific source preparation, if evidenced
	distutils-r1_python_prepare_all
}
```

Use the actual exported helper and call order from the installed eclass. Keep
test-only dependencies conditional and separate from `RDEPEND`. Use a narrow
`EPYTEST_DESELECT` or `RESTRICT="test"` only with a source-level reason such
as unavailable fixtures, network-only tests, or an upstream test defect.

## Exceptions

Investigate instead of applying the default when:

- the source is a wheel-only or bundled binary artifact;
- the build backend is unsupported or generated outside the release archive;
- the project is a Python helper embedded in a CMake/Meson/other package;
- the package installs only a CLI or plugin and its Python implementation
  choice differs from the distribution default;
- the source name does not map to the PyPI project name;
- the upstream build invokes Python but does not install Python modules.
