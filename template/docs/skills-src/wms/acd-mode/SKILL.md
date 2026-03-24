---
name: acd-mode
description: "Use when the task needs architecture or contract confirmation before coding, especially for cross-module, public-interface, schema, or trade-off-heavy work. Not for routine low-risk changes or evidence-first incident triage."
---

# ACD Mode

## When to Use

- 跨模块 / 跨服务 / 公共接口
- 数据库结构调整
- 方案取舍明显
- 需要先确认边界与回滚

## Pair With

- `governance-orchestrator`
- `feature-dev-scene`
- `database-change-scene`
- `refactoring-scene`

## Workflow

1. 读 [workflow](references/workflow.md)
2. 输出时遵守 [output contract](references/output-contract.md)
3. 最后执行 [checklists](references/checklists.md)

## Boundaries

- 人工确认前，不要进入实现
- 不要把多种取舍压成一句模糊建议
- 若验收已清楚且可以测试，切到 `tdd-mode`
- 若证据不足，切到 `aod-mode`
