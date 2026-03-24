---
name: feature-dev-scene
description: "Use only when the task is approved feature implementation or capability change. Not for early planning, incident investigation, code review, database-only review, refactoring-only cleanup, or docs-only work."
---

# Feature Dev Scene

## When to Use

- 新增功能
- 扩展现有业务能力
- 新增接口、DTO、Feign、Query/Execute 路径

## Always Pair With

- `governance-orchestrator`
- `wms-task-governance`
- `gitnexus-code-navigation`
- `auto-dev-orchestrator`
- `delivery-evaluation-gate`
- 如需先卡方案：`plan-gate`

## Read Next

1. [workflow](references/workflow.md)
2. [output contract](references/output-contract.md)
3. [checklists](references/checklists.md)

## Boundaries

- 这是薄场景 Skill，不承载任务初始化和完整闭环
- 场景重点是功能设计与层次归属，不替代 Core Skill
