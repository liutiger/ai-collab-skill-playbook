---
name: database-change-scene
description: "Use only when schema change, SQL review, or data-fix planning is the main task. Not for generic feature work that merely touches persistence."
---

# Database Change Scene

## When to Use

- DDL 变更
- DML / 数据修复
- 字段、索引、表结构评审

## Always Pair With

- `wms-task-governance`
- `gitnexus-code-navigation`
- `auto-dev-orchestrator`

## Read Next

1. [workflow](references/workflow.md)
2. [output contract](references/output-contract.md)
3. [checklists](references/checklists.md)

## Boundaries

- 场景重点是联动影响、锁表风险、分批和回滚
- 不要只看 SQL，不看 Entity / Mapper / 同步链路
