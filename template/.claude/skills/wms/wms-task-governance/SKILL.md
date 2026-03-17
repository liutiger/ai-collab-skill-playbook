---
name: wms-task-governance
description: "Use only when task lifecycle management itself is needed: creating, resuming, or closing docs/tasks records, completion markers, or sink artifacts. Not for ordinary coding, review, tracing, or planning questions."
---

# WMS Task Governance

## When to Use

- 开始一个新的 WMS AI 任务
- 续做已有任务，需要先检查完成边界和待处理项
- 准备结束任务，需要补齐落盘和完成标记

## Pair With

- `gitnexus-code-navigation`：涉及代码理解、定位、影响评估时
- `auto-dev-orchestrator`：需求已确认，要进入完整开发闭环时
- `delivery-evaluation-gate`：涉及代码 / SQL / 配置改动，需要交付门禁时
- `plan-gate`：高风险任务需要先卡在方案确认阶段时

## Workflow

1. 先读 [workflow](references/workflow.md)
2. 缺少任务目录时，用 `scripts/create_task_dir.sh`
3. 写任务文档前，对照 [output contract](references/output-contract.md)
4. 准备结束任务前，逐项执行 [checklists](references/checklists.md)

## Boundaries

- 本 Skill 负责任务生命周期治理，不替代场景专项检查
- 不要把“已经回答问题”误判成“任务已完成”
- 不要跳过完成标记和知识沉淀
- 不要在评测门禁未过时写完成标记
