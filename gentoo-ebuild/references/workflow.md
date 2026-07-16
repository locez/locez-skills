# Workflow

Use this file when a request spans multiple maintenance modes or any package edit has enough risk that ordering matters. Keep the agent as the decision-maker and native Gentoo tools as the execution surface.

## Task Routing

- New upstream project not packaged before: use `new-package.md`.
- Existing package new version: use `version-bump.md`.
- Existing ebuild failure, review, or QA finding: use `qa.md`.
- Any eclass, phase, or helper uncertainty: use `eclass-discovery.md`.
- Commit or PR preparation: use `commit-pr.md`.

## Stage Protocol

Do not force persistent artifact files for ordinary ebuild work. The outcome can be notes in the final report, review comment, or commit/PR description.

| Stage | Type | Outcome | Barrier Before |
| --- | --- | --- | --- |
| Policy and scope | serial | target repo rules, package set, PR scope | evidence gathering |
| Evidence gathering | parallelizable | package history, package profile, similar ebuilds, upstream facts, eclass facts | decisions |
| Semantic package decision | barrier | default eclass, generated skeleton, dependency classes, exceptions | edits |
| Maintainer decisions | barrier | license, redistribution, keywords, patch strategy, PR boundaries | edits |
| Package edit | serial | ebuild, metadata, files, patches | Manifest |
| Mechanical lint/fix | serial | current Gentoo copyright year in edited ebuild/eclass files | Manifest |
| Manifest | serial | updated `Manifest` when distfiles change | QA |
| QA loop | serial | fixed findings or documented limitations | commit/PR |
| Old version gate | barrier | add-only decision, or old-version deletion followed by renewed Manifest/QA | commit/PR |
| Commit/PR prep | barrier | final diff, test evidence, residual risk | final report |

Parallelize only read-only discovery such as `rg`, `sed`, `ls`, package history reads, and upstream/eclass evidence checks. Serialize all file edits, mechanical lint/fix scripts, `pkgdev manifest`, QA reruns that depend on edits, commits, pushes, and PR creation.

During evidence gathering, infer the package profile before drafting code. Read
`semantic-generation.md`, `domain-routing.md`, and `shell-idioms.md`, then the
matching domain reference. The semantic barrier must settle the normal eclass,
phase/helper skeleton, Gentoo shell idioms, direct dependency split, and any
exception before package edits.

## Repository Policy Boundary

Generic Gentoo guidance belongs in this skill. Overlay-specific policy belongs in `AGENTS.md`, `README`, `CONTRIBUTING`, PR templates, or CI config. When they conflict, follow the target repository.

## Automation Boundary

- Do not create broad helper tools, workflow drivers, queue systems, or project-specific command layers as part of this skill.
- Prefer existing tools: `pkgdev`, `pkgcheck`, `ebuild`, `emerge`, `git`, `gh`, `nvchecker`.
- Scripts are only justified when native tools cannot express a repeated, deterministic, low-judgment operation. Keep them narrow lint/fix helpers, not workflow drivers.
- Use the bundled `scripts/ensure_copyright_year.py --fix` on edited `.ebuild` and `.eclass` files before Manifest/QA unless repository policy says otherwise.
- Human or maintainer judgment is required for eclass choice, license ambiguity, redistribution, dependency interpretation, patch strategy, keyword claims, version removal, and PR scope.
- Scripts do not make eclass, dependency, phase, test, or QA-exception decisions. They may only perform a narrow deterministic check or repair after the semantic draft.

## Review Gates

Ask once, with defaults and impact, when evidence cannot settle:

- License, redistribution, proprietary downloads, credentials, or click-through terms.
- Category/package naming or upstream identity ambiguity.
- Major patching, vendoring, bundled binary, or QA exception strategy.
- Keyword claims that cannot be tested under repository policy.
- Old-version removal after a successful version bump, unless repository policy or the user already requested it.
- Whether multiple packages belong in one PR.

Do not stop for low-risk reversible choices that package precedent or repository policy already answers.

## Finish Criteria

For any non-trivial package change:

1. Gather repository policy and package history.
2. Gather local and official evidence.
3. Make the smallest package change.
4. Run narrow deterministic lint/fix helpers for edited files.
5. Regenerate Manifest when distfiles change.
6. Run targeted QA, then repository-required broader QA.
7. For version bumps, pass through the old-version gate after new-version validation.
8. If an old ebuild is removed, regenerate Manifest and rerun affected QA.
9. Report exact commands, pass/fail status, skipped checks, and remaining risk.
