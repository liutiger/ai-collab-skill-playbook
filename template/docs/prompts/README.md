# 五层治理骨架 + 单一总控 Skill 兼容体系（Public V2）

> 本目录是公开模板中的 Prompt 兼容入口。默认工作法以下方 Skill 源码与生成产物为准。

## 原则

- **章程层（总纲）**：`docs/guides/AI协作研发章程.md`
- **Governance**：`00-department-standards.md` + `15-governance-lifecycle-contract.md`
- **Orchestrator**：`16-governance-orchestrator.md`
- **Scene**：`12-scene-catalog.md`，`01~06` 仅保留兼容入口
- **Stage**：`07/09/10` 等兼容阶段入口
- **Method**：`13-method-catalog.md`，`08` 是显式专项方法入口
- **Skill 实现层**：`docs/skills-src/` 为源码，`.claude/skills/wms/` 为运行产物
- **Copilot 适配层**：`.github/copilot-instructions.md`、`.github/instructions/`、`.github/prompts/` 由 `docs/skills-src/` 自动生成

> `TDD / ACD / AOD` 是 **Orchestrator 之下的执行模式**，不是第六层架构。它们通过 `14-mode-catalog.md` 和 `17~19` 模式入口参与总控决策。

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

## Copilot 默认入口

如果你在 VS Code 中使用 GitHub Copilot Chat，默认优先使用这些 slash prompt：

- `/wms-orchestrator`
- `/wms-tdd`
- `/wms-acd`
- `/wms-aod`
- `/wms-link-trace`
- `/wms-evaluation-gate`

使用建议：

- 日常绝大多数任务先用 `/wms-orchestrator`
- 只有当你明确知道当前任务必须固定在某种模式时，才直接进 `/wms-tdd`、`/wms-acd`、`/wms-aod`
- 只有当你明确只想做链路确认时，才显式用 `/wms-link-trace`
- 涉及代码 / SQL / 配置改动时，完成前补跑 `/wms-evaluation-gate`

## 用法

每次新对话，默认这样开场：

```text
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/15-governance-lifecycle-contract.md
#file:docs/prompts/12-scene-catalog.md
#file:docs/prompts/13-method-catalog.md
#file:docs/prompts/14-mode-catalog.md
#file:docs/prompts/16-governance-orchestrator.md

[任务描述]
```

### 模式入口

当你明确要固定某种执行模式时，可直接进入：

- `00 + 15 + 14 + 17`：TDD
- `00 + 15 + 14 + 18`：ACD
- `00 + 15 + 14 + 19`：AOD

### 评测门禁 / 交付验收模式

在你希望 AI 对已完成改动执行自动评测、输出结构化结论，并决定是否允许写完成标记时，使用：

```text
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/15-governance-lifecycle-contract.md
#file:docs/prompts/10-evaluation-gate.md

[按已实现结果执行评测门禁并输出结论]
```

### 专项方法模式

当你明确知道这轮只做链路确认时，可直接进入：

- 链路确认：`00 + 15 + 13 + 08`

## 场景与兼容入口

| 任务类型 | 引用 |
|---------|------|
| 新功能开发兼容入口 | `01-feature-dev.md` |
| 线上问题排查兼容入口 | `02-issue-investigation.md` |
| 代码审查兼容入口 | `03-code-review.md` |
| 数据库变更兼容入口 | `04-database-change.md` |
| 重构优化兼容入口 | `05-refactoring.md` |
| 文档编写兼容入口 | `06-documentation.md` |
| 多角色自动开发编排（兼容阶段入口） | `07-auto-dev-orchestration.md` |
| 链路确认 / 知识沉淀 | `08-link-confirmation.md` |
| 方案核对 / 实施前确认（兼容阶段入口） | `09-plan-gate.md` |
| 自动评测 / 交付验收 | `10-evaluation-gate.md` |
| 场景路由兼容入口 | `11-scene-router.md` |
| 统一场景目录 | `12-scene-catalog.md` |
| 统一专项方法目录 | `13-method-catalog.md` |
| 统一执行模式目录 | `14-mode-catalog.md` |
| 共享治理生命周期合同 | `15-governance-lifecycle-contract.md` |
| 治理总控默认入口 | `16-governance-orchestrator.md` |
| TDD 模式 | `17-tdd-mode.md` |
| ACD 模式 | `18-acd-mode.md` |
| AOD 模式 | `19-aod-mode.md` |
