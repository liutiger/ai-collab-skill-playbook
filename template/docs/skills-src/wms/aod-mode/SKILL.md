---
name: aod-mode
description: "Use when the task is evidence-heavy or ambiguous and the right next step is to analyze, observe, and narrow hypotheses before fixing anything. Not for clear testable feature work."
---

# AOD Mode

## When to Use

- 线上异常或数据不一致
- 证据不足、现象复杂
- 需要时间线、日志、链路、副作用观察

## Pair With

- `governance-orchestrator`
- `issue-investigation-scene`
- `link-trace-and-curation`

## Workflow

1. 读 [workflow](references/workflow.md)
2. 输出时遵守 [output contract](references/output-contract.md)
3. 最后执行 [checklists](references/checklists.md)

## Boundaries

- 不要一上来直接写代码
- 不要把猜测写成结论
- 证据足够讨论方案时，切到 `acd-mode`
- 修复目标已清楚且验收可测试时，切到 `tdd-mode`
