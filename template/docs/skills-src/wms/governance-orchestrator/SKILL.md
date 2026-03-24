---
name: governance-orchestrator
description: "Use as the default WMS skill entry. It should classify scene, choose execution strategy, drive the DISCOVER / DELIVER / VERIFY states, overlay specialized methods, batch hard-gate confirmations, and continue in the same thread without asking the user to switch prompts."
---

# Governance Orchestrator

## When to Use

- 默认 WMS 任务入口
- 用户只说目标、异常、Review、DDL、重构或文档需求，没有明确指定阶段
- 希望在同一线程里自动完成“场景判定 -> 策略选择 -> 三态推进 -> 待确认汇总 -> 继续执行”

## Pair With

- `wms-task-governance`
- `gitnexus-code-navigation`
- `feature-dev-scene`
- `issue-investigation-scene`
- `code-review-scene`
- `database-change-scene`
- `refactoring-scene`
- `documentation-scene`
- `tdd-mode`
- `acd-mode`
- `aod-mode`
- `link-trace-and-curation`
- `delivery-evaluation-gate`

## Workflow

1. 先执行共享开始合同：[start contract](../wms-task-governance/references/start-contract.md)
2. 读 [workflow](references/workflow.md)
3. 输出时遵守 [output contract](references/output-contract.md)
4. 准备结束当前轮次前，先执行共享结束合同：[finish contract](../wms-task-governance/references/finish-contract.md)
5. 最后执行 [checklists](references/checklists.md)

## Boundaries

- 不要要求用户在同一条任务链里频繁切换 prompt
- 不要把多个 hard gate 拆成多轮零碎追问
- 不要在高风险、边界不清或存在方案取舍时直接离开 DISCOVER
- 不要在未过评测门禁时默认任务可以完成
