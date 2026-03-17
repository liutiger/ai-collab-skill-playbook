---
name: link-trace-and-curation
description: "Use only when the primary deliverable is an execution-chain trace with branches and side effects. Not for feature implementation, generic review, or post-change evaluation."
---

# Link Trace and Curation

## When to Use

- 功能改造前先确认真实链路
- 排障前先确认入口、主链路和关键副作用
- 跨模块改动前先确认影响面

## Pair With

- `wms-task-governance`
- `gitnexus-code-navigation`
- `plan-gate`：链路分析结果还要经过方案确认时

## Workflow

1. 先读 [workflow](references/workflow.md)
2. 需要落盘时，从 `assets/templates/link-trace.md` 起步
3. 输出前对照 [output contract](references/output-contract.md)
4. 结束前执行 [checklists](references/checklists.md)

## Boundaries

- 不要把“对象 set 了值”误判成“链路已完成”
- 不要只凭经验画流程，必须以真实代码顺序为准
- 不要只停留在聊天窗口，必须沉淀到 docs
