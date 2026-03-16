---
name: refactoring-scene
description: "Use when a WMS task is safe refactoring, restructuring, or behavior-preserving cleanup. This is a thin scene skill that adds refactoring-specific checks on top of the core skills."
---

# Refactoring Scene

## When to Use

- 大方法拆分
- 去重复代码
- 策略化 / 模式化改造
- 保持行为不变的结构优化

## Always Pair With

- `wms-task-governance`
- `gitnexus-code-navigation`
- `auto-dev-orchestrator`

## Read Next

1. [workflow](references/workflow.md)
2. [output contract](references/output-contract.md)
3. [checklists](references/checklists.md)

## Boundaries

- 场景重点是风险分级、小步提交、行为不变
- 不要把局部重构扩展成无边界重写
