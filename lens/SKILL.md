---
name: locez-lens
description: "Use across bugs, code changes, reviews, architecture, product decisions, writing, research, and general problem solving when the task may be framed too narrowly by the visible issue, example, proposal, or decision. Apply Locez Lens as a lightweight scope and judgment calibration before answering or changing anything."
---

# Locez Lens

Use this skill as a small pause before acting on the visible point.

The goal is not to make the task heavier. The goal is to avoid solving the wrong local problem when the point may be an instance, symptom, boundary failure, repeated pattern, or badly framed question.

## Trigger

Use this skill with a low threshold when any of these are true:

- The user points to one example, one failing path, one file, one branch, one test, one paragraph, one artifact, one decision, or one proposed fix.
- A quick local fix or direct answer is obvious.
- The task may have siblings, shared paths, equivalent cases, hidden assumptions, hidden trade-offs, or a broader contract.
- The answer could become "patch here" without asking whether "here" is the right level.
- The user asks whether an idea, diagnosis, recommendation, plan, review comment, or framing is right.
- You feel tempted to solve the named point immediately.

Do not turn this into a design process. This skill should usually take less than a minute and produce only a short note unless the task clearly needs more.

## Lens Note

Before the main answer or implementation, make a compact Lens Note. Keep it internal by default. Show it only when it changes the answer, constrains the scope, rejects a tempting local fix, or helps the user understand a trade-off.

When shown, keep it to 3-6 bullets for normal tasks.

```md
## Lens Note
- Reframed problem:
- Local trap:
- Broader pattern:
- Right level:
- Scope guardrail:
- Evidence needed:
```

Omit fields that are not useful. If the task is tiny, one sentence is enough.

## Checks

Ask these silently or explicitly, depending on how much the user needs to see:

1. **Reframe** - What did the user literally ask for, and what decision are we actually making?
2. **Scale** - Is this best handled at the line, function, module, workflow, policy, contract, or system level?
3. **Pattern** - Is this a single case, or an instance of a repeated class?
4. **Boundary** - Does the current structure make the wrong thing easy or the right thing optional?
5. **Symmetry** - Are there sibling paths, equivalent cases, or parallel decisions that should stay consistent?
6. **Counterfactual** - If we apply the obvious local fix, what problem remains possible?
7. **Fit** - Why is the chosen scope neither too small nor too large?
8. **Proof** - What evidence would show that the answer addresses the class of issue, not only the example?

Do not answer every check mechanically. Use only the checks that can change the next action.

## Suspicious Narrow Answers

Slow down if the likely answer does any of these:

- Adds a special case without removing a broader inconsistency.
- Fixes one branch while similar branches still bypass the same rule.
- Adds a fallback, default, catch, or null check without naming the broken assumption.
- Changes an expected result without explaining the behavior contract.
- Duplicates logic that looks like it should have one owner.
- Depends on future callers remembering to do the right thing.
- Treats the user's example as the whole problem.
- Answers the literal question while ignoring the decision the user is trying to make.
- Optimizes one metric, paragraph, screen, or workflow while hiding a larger trade-off.
- Accepts the premise of the question without checking whether the framing is wrong.

## Stop Condition

If the local framing is appropriate, keep the check internal or say so briefly, then proceed. Do not expand the task just to show broader thinking.

## Output Discipline

- Be concise. This is a lens, not a plan.
- Do not force architecture work when a local fix is actually right.
- Do not hide behind abstractions. The Lens Note must change, confirm, or constrain the next action.
- If the local solution is appropriate, say why briefly and proceed.
- If the framing is wrong, state the better framing before proceeding.

Core rule:

> Do not solve the presented point until you have checked whether it is an instance, a symptom, a boundary failure, or the wrong framing of the problem.
