# Skill Primer For Newcomers

[中文版本](skill-primer.zh-CN.md)

This guide explains skills, plan skills, Locez Lens, and workflow-skill-architect for people who are new to agent workflows. It is not the operating manual for any single skill. It explains why this repository treats working methods as reusable skill assets.

## What Is A Skill?

In a coding agent, a skill is not just a prompt, and it is not merely a way to make the model remember some knowledge. A skill is better understood as a reusable working protocol. It tells the agent, for a specific class of task, how to frame the problem, how to organize steps, when to stop and verify, when to call tools, when to split work across subagents, and what the final handoff should contain.

You can think of a coding agent as an engineering assistant that can read code, edit files, run commands, and make technical judgments. Without skills, it mainly relies on the current conversation and the model's general experience. That can work, but it commonly leads to these problems:

- Similar tasks get re-designed from scratch every time.
- The agent may follow a local example too literally and only fix the surface symptom.
- Complex work can become a long vague prompt with no intermediate artifacts or validation.
- Multi-agent work can duplicate effort, overwrite shared files, or fail to merge cleanly when roles are unclear.

The value of a skill is to turn improvisation into a repeatable professional workflow. A good skill usually answers:

- When should it be activated?
- What class of problem does it solve?
- What should the agent inspect first?
- Which steps must be serial, and which can run in parallel?
- Which decisions belong to the main agent, and which can be delegated to workers?
- What artifacts should each stage produce, such as plans, rules, reports, or validation results?
- How can the agent know the task is actually complete, rather than merely looking complete?

In one sentence:

> A skill is a reusable engineering working method for coding agents. It packages experience, boundaries, process, validation, and delivery standards into a callable capability.

## Skills And Plan Skills

New users often interpret a plan as "write down the steps first." In agent workflows, a plan skill is a stricter implementation planning protocol.

A loose plan might say:

1. Read the code.
2. Change the feature.
3. Run tests.
4. Commit.

That may be enough for a human, but it is too vague for an agent. During execution, agents often face context loss, unclear file ownership, ambiguous test goals, and tasks that are too large to verify cleanly.

A stronger plan skill asks the plan to include:

- Clear goal: what exactly is being built or changed.
- Architecture approach: why the work is split this way.
- File list: which file owns which responsibility.
- Task breakdown: small units that can be executed and checked.
- Test steps: write a failing test, implement, then verify it passes.
- Commands and expected results: not just "run tests", but which command and what output matters.
- Completion checks: how to prove the work is done.

The point of a plan skill is not to write a nice-looking plan. It turns a requirement into an engineering route that an agent can execute reliably.

<a id="locez-lens-deep-dive"></a>

## Locez Lens: Check Whether The Problem Is Framed Correctly

`Locez Lens` is a lightweight judgment-calibration skill. Its core move is not to solve the problem immediately. It pauses before action and checks:

- Did the user provide a local example?
- Is this issue a symptom of a larger problem?
- Would the obvious local fix miss sibling cases?
- Should the fix happen at the line, function, module, workflow, or system level?
- Is the current boundary wrong?

Its role can be summarized as:

> Locez Lens is a problem-framing calibrator. It prevents the agent from fixing the visible point before understanding what that point represents.

For example, a user says: "This test failed, update the expected value."

Without Lens, an agent may directly edit the test until it passes. With Lens, the agent first asks:

- Did the code break, or was the test expectation wrong?
- Are similar tests failing too?
- Is this a boundary-condition issue, or did a shared function's behavior contract change?
- Would changing the expectation hide a real bug?

If the test is simply wrong, a local fix is fine. If the shared behavior contract changed, changing one test is not enough.

The value of Locez Lens is that it keeps the agent from being captured by the most visible point. It asks which level the problem should be solved at before work begins.

<a id="workflow-skill-architect-deep-dive"></a>

## workflow-skill-architect: Turn Complex Skills Into Workflows

`workflow-skill-architect` is an architecture-level skill. It is used to create or refactor complex multi-step skills, especially when:

- The main `SKILL.md` is too long and carries everything.
- Analysis, planning, execution, and validation are mixed together.
- Business rules and execution steps are tangled.
- Subagents are named but lack input/output contracts.
- Work that could run in parallel is forced through a serial path.
- Stages have no intermediate artifacts, so later work depends on model memory.
- Validation is weak, making the final result hard to trace back to rules and inputs.

Its role can be summarized as:

> workflow-skill-architect is a workflow architect for skills. It turns complex prompts into executable workflows with an entry point, role boundaries, artifacts, validation, and concurrency rules.

It emphasizes one core principle:

> The main `SKILL.md` should not carry the whole task. It should own activation conditions, orchestration rules, resource navigation, and stop conditions.

Detailed knowledge, templates, examples, and domain rules should live in `references/`. Repeated deterministic work should usually live in `scripts/`. If worker agents are needed, they need clear responsibilities, inputs, outputs, forbidden actions, and quality standards.

## Why Not Put Everything In One Long Prompt?

The first instinct when writing a skill is often to put every instruction into one long prompt. That is direct in the short term, but it creates long-term problems:

- The agent must read lots of irrelevant content every time.
- Rules and workflow become hard to maintain because they are mixed together.
- Changing one domain rule may accidentally affect the whole execution path.
- Humans and subagents cannot tell who owns which part of the work.
- Outputs are hard to trace and validate.

workflow-skill-architect tends to split a skill into an engineering structure:

- `SKILL.md`: entry point, triggers, core rules, and resource navigation.
- `references/`: stable knowledge, rules, templates, and detailed workflow guidance.
- `scripts/`: repeatable operations that should be deterministic.
- agent contracts: responsibility boundaries for worker agents.
- artifacts: stage outputs that downstream steps can consume.
- validation: checks that prove the result is correct.

That shifts the work from "writing a prompt" to "designing an executable workflow."

## Why Intermediate Artifacts Matter

Complex tasks are risky if they only move through model context. Context can get long, noisy, compacted, or lose key decisions.

workflow-skill-architect encourages important stages to produce artifacts such as:

- `intake-summary.md`
- `domain-model.md`
- `workflow-plan.md`
- `agent-contracts.md`
- `rules.yaml`
- `validation-report.md`
- `handoff-summary.md`

These artifacts are not paperwork for its own sake. They make work traceable, handoff-friendly, and verifiable. A simple test is: if an artifact does not change downstream behavior, do not add it; if it makes later steps more stable or auditable, it may be worth keeping.

## Why Multi-Agent Work Needs Contracts

Multiple agents are not automatically better. Without boundaries, multiple agents may just duplicate work and create a difficult merge.

A worker-agent contract usually states:

- Purpose: what transformation this agent owns.
- Inputs: what it receives.
- Outputs: what it must produce.
- Concurrency: what can run in parallel, and which files it must not write.
- Allowed actions: what it may do.
- Forbidden actions: what must remain with the main agent or another worker.
- Quality bar: what the result must satisfy.
- Escalation: when uncertainty must be reported instead of guessed through.

That turns multi-agent work from "ask several agents to help" into a bounded collaboration system.

<a id="lens-and-workflow-skill-architect"></a>

## How The Two Skills Work Together

A useful way to separate them:

- `Locez Lens` asks: are we solving the right problem?
- `workflow-skill-architect` asks: if this is a complex reusable problem, how should we design a stable workflow for it?

They work at different levels, but they are complementary.

Suppose a data-cleaning skill keeps asking the user questions whenever a field is missing, and the user says: "It asks too many questions."

First, use Locez Lens:

- Is this only one missing-field problem, or is the skill's confirmation mechanism wrong?
- Is a rule missing, or does the workflow need a batched review gate?
- Would adding a default value hide real business uncertainty?

If Lens shows that this is a workflow-level problem, use workflow-skill-architect:

- Replace scattered confirmations with a grouped review gate.
- Move field rules into `references/rules.md` or a structured rules file.
- Produce `exceptions.csv` for uncertain cases and review them together.
- Add a validation report to check that cleaning follows the rules.
- If the task is large, split profiling, domain analysis, and validation across worker agents.

The result does not merely ask one fewer question this time. It gives the skill a stable way to handle similar uncertainty in future runs.

## Short Version For Newcomers

> A skill is a reusable working method for a coding agent, not just a prompt. It defines how the agent should judge, split, verify, and deliver work for a class of tasks.
>
> Locez Lens is a lightweight judgment lens. Before action, it checks whether the user's visible point is too local and whether the solution belongs at a different level. It prevents the agent from fixing the visible bug while missing the real problem.
>
> workflow-skill-architect is a skill architecture tool. It turns complex skills from long prompts into real workflows with an entry point, references, scripts, subagent contracts, intermediate artifacts, concurrency boundaries, and validation standards.
>
> A plan skill turns a concrete requirement into an executable implementation plan. Plan skills ask "how do we do this next"; Locez Lens asks "is the problem framed correctly"; workflow-skill-architect asks "how should this reusable capability be designed?"

## Summary

`Locez Lens` is valuable because it makes senior-engineer scope judgment explicit. It keeps the agent from rushing into a patch before confirming the right level of solution.

`workflow-skill-architect` is valuable because it upgrades skill design from "write a long prompt" to "design a verifiable, maintainable, parallelizable, handoff-friendly workflow."

Together, one handles direction and the other handles structure. For newcomers to coding agents, they show a key idea:

> Good agent work is not only about a smart model. It is about clear working methods, boundaries, artifacts, and verification.
