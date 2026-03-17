---
name: plan-gate
description: "Use only before implementation, when the task must stop at goal clarification, context locating, and minimum-change planning. Not for already-approved execution or post-change evaluation."
---

# Plan Gate

## When to Use

- 需求边界还不稳
- 改动风险高，必须先核对方案
- 历史链路复杂，先确认入口、主编排和影响面

## Pair With

- `wms-task-governance`
- `gitnexus-code-navigation`
- 对应场景薄 Skill

## Workflow

1. 读 [workflow](references/workflow.md)
2. 如需结构化输出，从 `assets/templates/plan-gate.md` 起步
3. 输出时遵守 [output contract](references/output-contract.md)
4. 结束前执行 [checklists](references/checklists.md)

## Boundaries

- 未确认前禁止进入实现
- 不要把多个猜测方案一起抛给用户
- 信息不足时停在“待确认”，不要越过关卡
