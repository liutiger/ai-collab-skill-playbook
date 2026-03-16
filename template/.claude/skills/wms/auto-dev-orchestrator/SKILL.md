---
name: auto-dev-orchestrator
description: "Use when a WMS task should run as a full multi-role delivery loop: understand, locate, design, implement, review, verify, and sink results into docs."
---

# Auto Dev Orchestrator

## When to Use

- 复杂任务需要 AI 走完整闭环
- 跨模块需求不能只停在分析阶段
- 需要把实现、自检和落盘收紧在同一次协作中

## Pair With

- `wms-task-governance`
- `gitnexus-code-navigation`
- `delivery-evaluation-gate`
- 对应场景薄 Skill：`feature-dev-scene`、`issue-investigation-scene`、`code-review-scene`、`database-change-scene`、`refactoring-scene`、`documentation-scene`

## Workflow

1. 读 [workflow](references/workflow.md)
2. 按 [output contract](references/output-contract.md) 输出阶段结果
3. 实施完成后，逐项核对 [checklists](references/checklists.md)

## Boundaries

- 不要跳过 Planner / Context / Architect 阶段直冲实现
- 不要忽略场景薄 Skill 的专项检查
- 不要把“已改代码”当成“已完成闭环”
- 不要在未经过评测门禁时默认任务已完成
