# locez-skills

面向 agent 工程工作的可复用 AI skills 仓库。

[English README](README.md)

这个仓库收集工作流、维护、分析和判断校准类 skills，用来在不同 agent、机器和项目之间复用，不把私人主机状态写进仓库。Skill 不只是提示词；它是一份小型、可版本化的工作协议，告诉 agent 什么时候启用、怎样判断任务、哪些产物或检查重要，以及什么情况下可以交付。

给新人的更详细说明见 [docs/skill-primer.zh-CN.md](docs/skill-primer.zh-CN.md)。

新人文档里的深入解释：

- [Locez Lens：为什么 scope 校准重要](docs/skill-primer.zh-CN.md#locez-lens-deep-dive)
- [workflow-skill-architect：怎样把长 prompt 改成 workflow](docs/skill-primer.zh-CN.md#workflow-skill-architect-deep-dive)
- [Locez Lens 和 workflow-skill-architect 如何配合](docs/skill-primer.zh-CN.md#lens-and-workflow-skill-architect)

## Skill 目录

| Skill | 仓库目录 | 什么时候用 | 主要作用 |
| --- | --- | --- | --- |
| `$gentoo-maintenance` | `gentoo-maintenance/` | 处理 Portage 冲突、`@world` 升级、`/etc/portage` 清理、binpkg 取舍，或判断 Gentoo 本地规则应该放在哪里。 | 先判断主机角色和任务类型，区分本地偏好与生成规则，把候选 Portage 改动暂存到 `/tmp`，并在任何非 `/tmp` 写入前停下来给用户审。 |
| `$locez-overlay-bump-workflow` | `locez-overlay-bump-workflow/` | 维护 `/home/locez/locez-overlay` 里的包，尤其是 bump、删除、或对齐 nvchecker 跟踪状态。 | 区分 release-managed、live-only、removed 包；让 nvchecker 自动化与包状态一致；对有意义的 ebuild 改动要求本地验证。 |
| `$repo-visual-analysis` | `repo-visual-analysis/` | 理解一个仓库、生成架构/流程图、产出可打开的可视化报告，或寻找有证据支撑的改进机会。 | 产出 quick scan、focused map、Mermaid 或 HTML 可视化报告、claim/evidence 追踪和基于仓库证据的机会列表，同时避免把弱证据写成确定结论。 |
| `$workflow-skill-architect` | `workflow-skill-architect/` | 创建或重构复杂 workflow skill，尤其是主 `SKILL.md` 过载、子 agent 角色不清、反复向用户确认、缺少中间产物或验证弱的时候。 | 把长 prompt 改成结构化 workflow skill：入口编排、references、artifact 协议、可选 agent 合同、并发边界和验证门都分清楚。 |
| `$locez-lens` | `lens/` | bug、review、写作、架构、产品、研究或代码改动中，用户给出的可见问题可能太窄时。 | 在行动前做轻量 scope 校准，判断当前请求是一个实例、症状、边界失败、重复模式，还是 framing 本身有问题。 |

## 应该先用哪个 Skill？

- Gentoo 系统维护：从 `$gentoo-maintenance` 开始。
- `locez-overlay` 包 bump 或 nvchecker 工作：从 `$locez-overlay-bump-workflow` 开始。
- 代码仓库理解、可视化图、架构报告：从 `$repo-visual-analysis` 开始。
- 设计或修复另一个 skill：从 `$workflow-skill-architect` 开始。
- 修复、评审、决策或写作的边界可能太窄：从 `$locez-lens` 开始。

典型请求：

```text
$gentoo-maintenance 分析这次 @world slot conflict
$gentoo-maintenance 帮我整理 package.accept_keywords
$locez-overlay-bump-workflow 帮我 bump app-misc/example
$repo-visual-analysis 给这个仓库生成一份 visual report
$workflow-skill-architect 把这个数据清洗 prompt 改成 workflow skill
$locez-lens 看看这个修复是不是框太窄了
```

## 安装到不同 Agent

这些 skills 使用 `SKILL.md` 包结构，所以同一个仓库 checkout 可以用 symlink 接入多个 agent runtime。

| Runtime | 个人 Skill 目录 | 项目 Skill 目录 | 说明 |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/skills/<skill-name>/` | `.claude/skills/<skill-name>/` | 个人 skill 对所有项目生效；项目 skill 跟随单个仓库。 |
| Codex / 兼容 Agent Skills 的工具 | `~/.agents/skills/<skill-name>/` | 取决于具体工具 | 适合作为多个工具共享的 Agent Skills 目录。有些 Codex 安装也会读取 `~/.codex/skills/`。 |
| OpenCode | `~/.config/opencode/skills/<skill-name>/` | `.opencode/skills/<skill-name>/` | OpenCode 也会发现 Claude 兼容的 `.claude/skills/` 和 agent 兼容的 `.agents/skills/` 位置。 |
| Hermes Agent | `~/.hermes/skills/<skill-name>/` | `skills/` 或配置的 external directories | Hermes 也可以通过 `skills.external_dirs` 扫描 `~/.agents/skills` 这类共享目录。 |

大多数 skill 的仓库目录名和 skill 名相同。比如全局安装到 Claude Code：

```bash
mkdir -p ~/.claude/skills
ln -s ~/locez-skills/gentoo-maintenance ~/.claude/skills/gentoo-maintenance
ln -s ~/locez-skills/locez-overlay-bump-workflow ~/.claude/skills/locez-overlay-bump-workflow
ln -s ~/locez-skills/repo-visual-analysis ~/.claude/skills/repo-visual-analysis
ln -s ~/locez-skills/workflow-skill-architect ~/.claude/skills/workflow-skill-architect
```

安装到 Codex 风格 runtime 常用的共享 Agent Skills 目录：

```bash
mkdir -p ~/.agents/skills
ln -s ~/locez-skills/gentoo-maintenance ~/.agents/skills/gentoo-maintenance
ln -s ~/locez-skills/locez-overlay-bump-workflow ~/.agents/skills/locez-overlay-bump-workflow
ln -s ~/locez-skills/repo-visual-analysis ~/.agents/skills/repo-visual-analysis
ln -s ~/locez-skills/workflow-skill-architect ~/.agents/skills/workflow-skill-architect
```

`locez-lens` 在仓库里使用更短的 `lens/` 目录：

```bash
ln -s ~/locez-skills/lens ~/.claude/skills/locez-lens
ln -s ~/locez-skills/lens ~/.agents/skills/locez-lens
```

OpenCode 示例：

```bash
mkdir -p ~/.config/opencode/skills
ln -s ~/locez-skills/gentoo-maintenance ~/.config/opencode/skills/gentoo-maintenance
ln -s ~/locez-skills/locez-overlay-bump-workflow ~/.config/opencode/skills/locez-overlay-bump-workflow
ln -s ~/locez-skills/repo-visual-analysis ~/.config/opencode/skills/repo-visual-analysis
ln -s ~/locez-skills/workflow-skill-architect ~/.config/opencode/skills/workflow-skill-architect
ln -s ~/locez-skills/lens ~/.config/opencode/skills/locez-lens
```

Hermes Agent 可以直接 symlink：

```bash
mkdir -p ~/.hermes/skills
ln -s ~/locez-skills/gentoo-maintenance ~/.hermes/skills/gentoo-maintenance
ln -s ~/locez-skills/locez-overlay-bump-workflow ~/.hermes/skills/locez-overlay-bump-workflow
ln -s ~/locez-skills/repo-visual-analysis ~/.hermes/skills/repo-visual-analysis
ln -s ~/locez-skills/workflow-skill-architect ~/.hermes/skills/workflow-skill-architect
ln -s ~/locez-skills/lens ~/.hermes/skills/locez-lens
```

也可以把共享 skills 统一放在 `~/.agents/skills`，然后在 `~/.hermes/config.yaml` 加 external directory：

```yaml
skills:
  external_dirs:
    - ~/.agents/skills
```

如果链接已经存在并且你想重建它：

```bash
RUNTIME_SKILL_DIR=~/.agents/skills
rm "$RUNTIME_SKILL_DIR/<skill-name>"
ln -s ~/locez-skills/<repo-directory> "$RUNTIME_SKILL_DIR/<skill-name>"
```

安装或更新 skill 后，如果你的 runtime 不支持热加载 skill 目录，就重启 agent 或开启一个新 session。

## 仓库结构

```text
<skill-name>/
  SKILL.md       # 触发条件、核心规则和资源导航
  references/    # 详细工作流规则、模板、合同、验证
  scripts/       # skill 使用的确定性辅助脚本
  agents/        # skill 列表里的 UI 元数据
  assets/        # 可选运行时资源

docs/
  specs/         # 设计历史和决策
  plans/         # 实施计划
```

不是每个 skill 都需要所有可选目录。Skill 目录应该专注运行时资源；仓库级文档放在 `README.md`、`README.zh-CN.md` 或 `docs/`。

## 仓库规则

- 不把私人机器状态写进仓库。
- 保持 `SKILL.md` 精简，把详细流程放到 `references/`。
- 重复且确定性的工作优先放到 `scripts/`，不要依赖模型临场记忆。
- 模板优先放到 `assets/`，不要复制 live system config。
- 设计历史放到 `docs/specs/`。
- 实施计划放到 `docs/plans/`。
- 有意义地修改 skill 后要做校验。
