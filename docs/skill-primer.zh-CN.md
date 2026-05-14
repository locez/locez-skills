# 面向新人的 Skill 入门

[English version](skill-primer.md)

这份文档整理自一次面向新人的 skill 讲解，重点解释 skill、plan skill、Locez Lens 和 workflow-skill-architect 的关系。它不是某个 skill 的运行说明，而是帮助读者理解这个仓库为什么要把工作方法沉淀成 skill。

## Skill 是什么？

在 coding agent 里，skill 不是普通提示词，也不只是“让模型记住一些知识”。更准确地说，skill 是一套可复用的工作协议：它告诉 agent 在某类任务出现时，应该如何判断问题、如何组织步骤、何时停下来验证、何时调用工具、何时把工作拆给子 agent、最后应该交付什么。

可以把 coding agent 理解成一个会读代码、改文件、跑命令、做判断的工程助手。没有 skill 时，它主要依赖当前对话里的指令和模型自己的经验。这样当然也能工作，但会有几个常见问题：

- 每次处理类似任务，都可能重新想一遍流程。
- 容易被用户给出的局部例子牵着走，只修表面问题。
- 复杂任务容易变成一长串模糊提示，缺少中间产物和验证。
- 多 agent 协作时，如果没有明确边界，容易重复工作、互相覆盖，或者最后合不起来。

Skill 的价值在于把“临场发挥”变成“可重复执行的专业流程”。一个好的 skill 通常会回答这些问题：

- 什么时候应该启用它？
- 它要解决哪一类问题？
- 进入任务后第一步看什么？
- 哪些事情必须串行，哪些事情可以并行？
- 哪些决策要交给主 agent，哪些可以交给 worker agent？
- 每个阶段产出什么 artifact，比如计划、规则、报告、验证结果？
- 怎样判断这次任务已经完成，而不是只是看起来完成？

一句话总结：

> Skill 是 coding agent 的可复用工程工作法，它把经验、边界、流程、验证和交付标准封装成可调用的能力。

## Skill 和 Plan Skill 的关系

很多刚接触 coding agent 的人会把 plan 理解成“先列个计划”。但在 agent 工作流里，plan skill 是一种更严格的实施计划协议。

普通计划可能只是：

1. 看代码。
2. 改功能。
3. 跑测试。
4. 提交。

这对人类来说可能够用，但对 agent 来说太松。Agent 在执行过程中容易遇到上下文丢失、文件边界不清、测试目标不清、任务粒度过大等问题。

更成熟的 plan skill 会要求计划里包含：

- 明确目标：到底要构建什么。
- 架构思路：为什么这样拆。
- 文件清单：每个文件负责什么。
- 任务拆分：每个任务足够小，方便执行和检查。
- 测试步骤：先写失败测试，再实现，再验证通过。
- 命令和预期结果：不是“跑测试”，而是具体跑什么、应该看到什么。
- 交付检查：怎样证明任务真的完成。

因此，plan skill 的重点不是“写一个好看的计划”，而是把需求变成 agent 可以稳定执行的工程路线图。

<a id="locez-lens-deep-dive"></a>

## Locez Lens：先判断问题有没有被框错

`Locez Lens` 是一个轻量级判断校准 skill。它的核心动作不是马上解决问题，而是在行动前先停一下，检查：

- 用户给的是不是一个局部例子？
- 这个问题是不是某个更大问题的症状？
- 明显的本地修复是不是会漏掉同类问题？
- 应该在线级、函数级、模块级、工作流级，还是系统级解决？
- 当前问题的边界是不是设错了？

它的定位可以概括为：

> Locez Lens 是一个问题 framing 校准器：防止 agent 只修眼前点，而忘了判断这个点到底代表什么。

例如用户说：“这个测试失败了，帮我改一下预期结果。”没有 Lens 的 agent 可能会直接改测试，让它变绿。用了 Lens 的 agent 会先想：

- 测试失败是因为代码错了，还是测试预期错了？
- 同类测试是不是也会失败？
- 这是一个边界条件问题，还是某个公共函数行为变了？
- 改预期会不会把真实 bug 掩盖掉？

如果检查后发现只是测试写错了，那就局部修。如果发现这是共享逻辑的行为契约变了，就不能只改一个测试。

Locez Lens 的价值是让 agent 不被“最显眼的问题”绑架，而是先判断应该在哪个层级解决。

<a id="workflow-skill-architect-deep-dive"></a>

## workflow-skill-architect：把复杂 skill 设计成工作流

`workflow-skill-architect` 是一个偏架构层的 skill。它用于创建或重构复杂多步骤 skill，尤其适合这些情况：

- 一个 skill 的主提示词太长，什么都塞在 `SKILL.md` 里。
- 分析、计划、执行、验证混在一起。
- 业务规则和操作步骤混在一起。
- 子 agent 有名字，但没有明确输入输出合同。
- 应该并行的事情被串行执行，浪费时间。
- 每一步没有中间产物，后续步骤只能依赖模型记忆。
- 验证不足，最终结果很难追溯到规则和输入。

它的定位可以概括为：

> workflow-skill-architect 是 skill 的工作流架构师：它把复杂提示词改造成有入口、有分工、有 artifact、有验证、有并发边界的可执行流程。

它特别强调一个核心原则：

> 主 `SKILL.md` 不应该承载整个任务，它应该负责激活条件、编排规则、资源导航和停止条件。

详细知识、模板、例子、领域规则应该放到 `references/`；可重复、确定性的工作应该尽量放到 `scripts/`；如果需要 worker agent，就要给它们明确的职责、输入、输出、禁止事项和质量标准。

## 为什么不是把所有内容写成长 prompt？

很多人写 skill 的第一反应是把所有说明都塞进一个很长的 prompt。短期看很直接，长期会带来几个问题：

- agent 每次都要读大量无关内容。
- 规则和流程混在一起，难维护。
- 改一个领域规则可能影响整个执行流程。
- 多人或多 agent 协作时，不知道谁负责哪一块。
- 输出结果不可追踪，也很难验证。

workflow-skill-architect 倾向把 skill 拆成工程结构：

- `SKILL.md`：入口、触发条件、核心规则、资源导航。
- `references/`：稳定知识、规则、模板、流程说明。
- `scripts/`：可确定执行的重复操作。
- agent contracts：worker agent 的职责边界。
- artifacts：阶段性产物，让下游步骤可消费。
- validation：证明结果正确的检查。

这就从“写提示词”变成了“设计可运行流程”。

## 中间产物为什么重要？

复杂任务如果只靠模型上下文推进，风险很高。上下文可能变长、变乱、被压缩，或者某些关键判断没有留下记录。

workflow-skill-architect 会鼓励重要阶段产出 artifact，例如：

- `intake-summary.md`
- `domain-model.md`
- `workflow-plan.md`
- `agent-contracts.md`
- `rules.yaml`
- `validation-report.md`
- `handoff-summary.md`

这些 artifact 的意义不是“多写文件”，而是让工作变得可追踪、可交接、可验证。一个简单判断是：如果某个 artifact 不会改变下游行为，就不要加；如果它能让后续步骤更稳定、更可审计，那就值得保留。

## 多 agent 协作为什么需要合同？

多 agent 并不天然更强。没有边界的多 agent 可能只是多个模型同时做重复工作，最后还需要大量合并。

worker agent 合同通常要说明：

- Purpose：这个 agent 负责什么转换。
- Inputs：它拿什么输入。
- Outputs：它必须产出什么。
- Concurrency：它能和谁并行，不能写哪些文件。
- Allowed Actions：它允许做什么。
- Forbidden Actions：哪些事情必须留给主 agent 或其他 agent。
- Quality Bar：产出要满足什么标准。
- Escalation：什么情况下不能猜，要上报不确定性。

这让多 agent 从“喊几个人一起干”变成“有边界的协作系统”。

<a id="lens-and-workflow-skill-architect"></a>

## 两个 skill 的关系

可以这样理解：

- `Locez Lens` 负责问：我们是不是在解决正确的问题？
- `workflow-skill-architect` 负责问：如果这是一个复杂且可复用的问题，应该怎样把它设计成稳定工作流？

它们的层级不同，但很互补。

假设你有一个数据清洗 skill，用户反馈：“它总是在字段缺失时问我问题，太烦了。”

先用 Locez Lens：

- 这只是一个字段缺失问题，还是整个 skill 的确认机制有问题？
- 是某个规则没写清楚，还是 workflow 缺少批量 review gate？
- 直接加一个默认值，会不会掩盖业务不确定性？

如果 Lens 判断这是系统性 workflow 问题，再用 workflow-skill-architect：

- 把 scattered confirmation 改成集中 review gate。
- 把字段规则放进 `references/rules.md` 或结构化规则文件。
- 给异常情况产出 `exceptions.csv`，集中交给用户审。
- 增加 validation report，确认清洗结果符合规则。
- 如果任务规模大，把 profiling、domain analysis、validation 拆成不同 worker agent。

这样，最终解决的不是“这次少问一个问题”，而是“整个 skill 以后遇到类似不确定性时都有稳定处理方式”。

## 给新人快速解释的版本

> Skill 是给 coding agent 用的可复用工作方法，不只是提示词。它规定 agent 在某类任务里怎么判断、怎么拆分、怎么验证、怎么交付。
>
> Locez Lens 是一个轻量判断镜头，作用是在动手前检查：用户给的点是不是太局部？我们是不是应该在更高或更低的层级解决？它避免 agent 修了眼前 bug，却没解决真正问题。
>
> workflow-skill-architect 是一个 skill 架构工具，作用是把复杂 skill 从“大段提示词”改造成真正的工作流：主入口、参考资料、脚本、子 agent 合同、中间产物、并发边界和验证标准都分清楚。
>
> Plan skill 则是把具体需求变成可执行实施计划。它更偏“接下来怎么一步步做”；Locez Lens 更偏“问题是不是框对了”；workflow-skill-architect 更偏“这个复杂能力应该怎样设计成可复用流程”。

## 总结

`Locez Lens` 的含金量在于把资深工程师的 scope 判断显式化，让 agent 不急着动手，而是先确认问题层级是否正确。

`workflow-skill-architect` 的含金量在于把 skill 设计从“写长 prompt”提升为“设计可验证、可维护、可并发、可交接的 workflow”。

这两个 skill 加起来，一个管方向，一个管结构。对于新接触 coding agent 的人来说，它们展示了一个关键观念：

> 好的 agent 工作，不只是模型聪明，而是有清晰的工作法、边界、产物和验证。
