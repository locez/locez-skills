# Binpkg Policy

Use this reference when the user cares more about avoiding local compilation than about keeping every optional feature.

## Core Principle

Preserve core function first. Non-core features may be trimmed when the host role and user preference allow it.

## Feature Triage

### Core Function

Features without which the package fails its main purpose.

Examples:

- a media server must still serve media
- a terminal application must still perform its main interactive role
- a desktop compositor must still provide the compositor path the user actually uses

### Important Integration

Frequently used but not strictly core:

- desktop integration
- notification support
- common network or IPC support

Trim only if the user accepts the tradeoff.

### Non-Core Features

Good candidates for trimming on VPS or builder hosts:

- docs
- examples
- optional GUI frontends
- secondary codecs or backends
- rarely used plugins

## Preferred Decision Order

1. Change USE or package selection
2. Prefer binpkg-compatible choices if acceptable
3. Patch an ebuild only if earlier steps are insufficient

## Recording Policy

- stable host-wide tolerance belongs in the local host profile
- durable package-group tradeoffs belong in `package.use/<topic>`
- short-lived experiments stay in `/tmp/gentoo-maintenance/`

## Anti-Patterns

- patching first instead of checking USE policy
- silently importing VPS tradeoffs into desktop systems
- treating every compile-saving change as worth permanent policy cost
