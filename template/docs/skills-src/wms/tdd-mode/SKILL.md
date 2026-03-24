---
name: tdd-mode
description: "Use when the task has clear, testable acceptance criteria and the best path is to define failing checks first, then implement the smallest change. Not for evidence-first incident triage or architecture trade-off work."
---

# TDD Mode

## When to Use

- 验收标准明确
- 可以先定义测试点、断言或回归点
- 希望先红后绿、再最小实现

## Pair With

- `governance-orchestrator`
- `feature-dev-scene`
- `delivery-evaluation-gate`

## Workflow

1. 读 [workflow](references/workflow.md)
2. 输出时遵守 [output contract](references/output-contract.md)
3. 最后执行 [checklists](references/checklists.md)

## Boundaries

- 不要在验收标准还不清楚时强行进入 TDD
- 不要先写实现、后补测试
- 若出现明显架构取舍，切到 `acd-mode`
- 若证据不足，切到 `aod-mode`
