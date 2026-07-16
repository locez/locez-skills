# Java And Perl Packages

Language identity is context. The upstream build model, installed artifact,
and eclass contract decide the generated skeleton.

## Java

Use `java-pkg-2` for pure Java packages or packages that need the Gentoo Java
environment. It owns Java setup and the common Java package dependency shape.
Use `java-pkg-simple` only after `java-pkg-2` (or the documented compatible
variant) and only when compiling Java sources without using upstream build
instructions. It expects the ebuild to describe source roots, resources,
classpath, and optional main class through its variables.

For Gradle, Maven, Ant, or another upstream build system, treat that build
system as the primary signal. Do not reduce the package to
`java-pkg-simple` merely because the output is a JAR, and do not invent a
Gradle eclass when the current tree has no applicable eclass. Inspect current
Java package precedent and make the build offline and reproducible.

## Perl

Use `perl-module` for a Perl module distribution whose source uses a Perl
build system such as ExtUtils::MakeMaker or Module::Build. The eclass owns
the standard Perl prepare, configure, compile, test, and install behavior and
adds its documented Perl dependencies. Use `perl-functions` when the package
needs Perl installation helpers but does not use a Perl-specific build system.

Read `Makefile.PL`, `Build.PL`, module metadata, installed `.pm`/compiled
artifacts, and tests before setting dependencies. Use `PERL_USEDEP` where the
installed feature compatibility requires it. Do not copy a sibling package's
dependency list or assume every Perl-adjacent tool is a module distribution.

## Phase And Test Rules

Preserve the eclass phase chain when adding patches, native code, resources,
or test setup. Keep test dependencies under `test? ( ... )` when repository
policy and eclass behavior permit it. A test restriction needs a concrete
upstream or environment reason, not just an unverified failing test.

