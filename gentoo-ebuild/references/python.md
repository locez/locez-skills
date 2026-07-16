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

Do not combine mutually exclusive implementation eclasses by habit. Verify
the current eclass contract and nearby packages when a distribution has both
runtime Python code and build-time Python tools.

## Phase Shape

Let `distutils-r1` own normal unpack, prepare, configure, compile, and install
behavior. Add standard helpers such as `distutils_enable_tests pytest` when
the upstream tests are runnable. If a package-specific phase is necessary,
call the eclass helper rather than replacing it:

```bash
python_prepare_all() {
	# package-specific preparation, if evidenced
	...
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

