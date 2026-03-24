---
name: refactoring-scene
description: "Use only when the main task is behavior-preserving cleanup or structural refactoring. Not for new features, incidents, or schema-led changes."
---

# Refactoring Scene

## When to Use

- 大方法拆分
- 去重复代码
- 策略化 / 模式化改造
- 保持行为不变的结构优化

## Always Pair With

- `governance-orchestrator`
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
