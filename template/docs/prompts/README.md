# 三层提示词 + Skill 兼容体系（V4）

> 本目录是公开模板中的兼容入口示例。权威工作法以下方 Skill 源码为准。

## 原则

- **章程层（总纲）**：`docs/guides/AI协作研发章程.md`
- **Layer 1**（自动注入）：项目级上下文。不同工具下通常来自 `AGENTS.md` 或 `.github/copilot-instructions.md`
- **Layer 2**（兼容入口）：`00-department-standards.md`，每次**必须**手动引用
- **Layer 3**（兼容场景入口）：根据任务类型选择一个 Prompt
- **Skill 层（权威工作法）**：`docs/skills-src/` 为源码，`.claude/skills/wms/` 为运行产物
- **Copilot 适配层**：`.github/copilot-instructions.md`、`.github/instructions/`、`.github/prompts/` 由 `docs/skills-src/` 自动生成
- **编排层（推荐）**：复杂任务或自动开发时，追加 `07-auto-dev-orchestration.md`

> 说明：`AI协作研发章程` 是总纲，`Skill` 是工作法，`Prompt / Copilot slash prompt` 是工具入口。Prompt 现在承担“任务入口”和“场景切换”的职责；稳定工作方法以下列 Skill 为准：`wms-task-governance`、`gitnexus-code-navigation`、`auto-dev-orchestrator`、`delivery-evaluation-gate`、`link-trace-and-curation`、`plan-gate`。

> 当前模板的根本收敛策略是：**阶段型 Skill 主动运行，场景型 Prompt / Scene Skill 被动补充**。也就是说，`01~06` 主要负责场景专项检查，不再推荐把它们都做成自动触发入口。

## Source Of Truth

- Skill 源码：`docs/skills-src/`
- 运行产物：`.claude/skills/wms/`
- Copilot 运行产物：`.github/copilot-instructions.md`、`.github/instructions/`、`.github/prompts/`
- Prompt：兼容入口，供不支持 Skill 的工具继续使用

常用命令：

```bash
python3 docs/skills-src/tools/validate_skills.py
python3 docs/skills-src/tools/validate_copilot_assets.py
python3 docs/skills-src/tools/generate_claude_skills.py
python3 docs/skills-src/tools/generate_copilot_assets.py
python3 docs/skills-src/tools/acceptance_check.py
```

如果你在 VS Code 中使用 GitHub Copilot Chat，优先使用这些 slash prompt：

- `/wms-plan-gate`
- `/wms-feature-plan`
- `/wms-auto-dev`
- `/wms-feature-dev`
- `/wms-evaluation-gate`
- `/wms-issue-investigation`
- `/wms-code-review`
- `/wms-database-change`
- `/wms-refactoring`
- `/wms-documentation`
- `/wms-link-trace`

使用建议：

- 场景明确时，优先用对应场景型 slash prompt
- 场景不清或跨场景时，优先用 `/wms-plan-gate`
- 只有已满足章程中的人工确认要求后，再进入 `/wms-auto-dev`
- 涉及代码 / SQL / 配置改动时，完成前补跑 `/wms-evaluation-gate`

## GitNexus 优先原则

- 涉及代码定位、调用链分析、影响评估时，默认顺序是：`GitNexus > 局部 rg > 全项目搜索`
- 先用 `query` 找流程和模块，再用 `context` 看符号上下文，修改公共符号前用 `impact` 看影响面
- 只有 GitNexus 无法覆盖，或需要补充精确文本/配置项时，再做大范围搜索
- CLI 示例：`npx gitnexus status`、`npx gitnexus query "<关键词>"`、`npx gitnexus context "<符号名>"`、`npx gitnexus impact "<符号名>"`
- MCP 示例：`gitnexus_query(...)`、`gitnexus_context(...)`、`gitnexus_impact(...)`

## 用法

每次新对话，消息开头写：

```
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/01-feature-dev.md

[任务描述]
```

### 自动开发 / 多角色编排模式（推荐）

复杂任务、跨模块任务、需要自动走完分析→实现→自检→文档闭环时，使用：

```
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/07-auto-dev-orchestration.md
#file:docs/prompts/01-feature-dev.md

[任务描述]
```

> 第三行按任务类型替换为 `01~08` 中的任意一个场景文件；涉及交付验收时，再追加 `10` 或在实现后单独进入评测门禁。

### 方案核对 / 实施前确认模式

在你希望 AI 先做目标澄清、GitNexus 定位、最小方案设计，等人工核对后再继续实现时，使用：

```
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/09-plan-gate.md
#file:docs/prompts/01-feature-dev.md

[任务描述]
```

> 第三行按任务类型替换为 `01~08` 中的任意一个场景文件。确认方案后，推荐切换到 `00 + 07 + 对应场景` 继续落地；涉及代码 / SQL / 配置改动时，完成前再补 `00 + 10`。

### 评测门禁 / 交付验收模式

在你希望 AI 对已完成改动执行自动评测、输出结构化结论，并决定是否允许写完成标记时，使用：

```
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/10-evaluation-gate.md

[按已实现结果执行评测门禁并输出结论]
```

## 场景选择

| 任务类型 | 引用 |
|---------|------|
| 新功能开发 | `01-feature-dev.md` |
| 线上问题排查 | `02-issue-investigation.md` |
| 代码审查 | `03-code-review.md` |
| 数据库变更 | `04-database-change.md` |
| 重构优化 | `05-refactoring.md` |
| 文档编写 | `06-documentation.md` |
| 多角色自动开发编排 | `07-auto-dev-orchestration.md` |
| 链路确认 / 知识沉淀 | `08-link-confirmation.md` |
| 方案核对 / 实施前确认 | `09-plan-gate.md` |
| 自动评测 / 交付验收 | `10-evaluation-gate.md` |

## Prompt -> Skill 映射

| Prompt | 对应 Skill |
|---|---|
| `00-department-standards.md` | `wms-task-governance` + `gitnexus-code-navigation` |
| `01-feature-dev.md` | `feature-dev-scene` |
| `02-issue-investigation.md` | `issue-investigation-scene` |
| `03-code-review.md` | `code-review-scene` |
| `04-database-change.md` | `database-change-scene` |
| `05-refactoring.md` | `refactoring-scene` |
| `06-documentation.md` | `documentation-scene` |
| `07-auto-dev-orchestration.md` | `auto-dev-orchestrator` |
| `08-link-confirmation.md` | `link-trace-and-curation` |
| `09-plan-gate.md` | `plan-gate` |
| `10-evaluation-gate.md` | `delivery-evaluation-gate` |

## 关键要求

- **00 必须每次都带**，不可只带 Layer 3
- `01~10` 可单独使用，但默认也应按多角色阶段执行，不再按单一身份思考
- 复杂任务推荐叠加 `07`，但 `07` 不是 `00` 的替代品
- 想先核对理解、上下文和实施方案时，优先使用 `09`，确认后再进入实现
- 涉及代码 / SQL / 配置改动时，完成前优先使用 `10` 做评测门禁
- Skill 是权威工作法，Prompt 是兼容入口
- curl wiki 获取最新规范，wiki 内容 > 本地提示词
- 任务完成标记格式：`----{YY}年{M}月{D}日 {HH}:{mm}:{ss} 第{x}次提交已完成，提交人：{git username}----`
