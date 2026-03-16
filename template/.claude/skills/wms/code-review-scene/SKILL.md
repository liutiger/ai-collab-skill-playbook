---
name: code-review-scene
description: "Use when a WMS task is code review or diff review. This is a thin scene skill that adds review-specific checks on top of the core skills."
---

# Code Review Scene

## When to Use

- PR Review
- 变更评审
- Diff 风险判断

## Always Pair With

- `wms-task-governance`
- `gitnexus-code-navigation`
- `auto-dev-orchestrator`

## Read Next

1. [workflow](references/workflow.md)
2. [output contract](references/output-contract.md)
3. [checklists](references/checklists.md)

## Boundaries

- 场景重点是按严重度输出问题
- 不要用“总体不错”代替问题列表
