---
name: gitnexus-code-navigation
description: "Use when understanding WMS code, tracing a chain, or assessing change safety. This skill enforces the GitNexus-first navigation protocol and anti-degeneration rules before any broad search."
---

# GitNexus Code Navigation

## When to Use

- 理解陌生代码或业务链路
- 在改动前确认调用链和影响面
- 排障、链路确认、重构或评审时缩小范围

## Pair With

- 外部 GitNexus Skill：`gitnexus-guide`、`gitnexus-exploring`、`gitnexus-debugging`、`gitnexus-impact-analysis`
- `plan-gate`：需要先完成上下文定位和方案核对时
- `auto-dev-orchestrator`：进入完整实现闭环时

## Workflow

1. 先读 [workflow](references/workflow.md)
2. 先执行 `scripts/gitnexus_probe.sh` 或等价的 `status`
3. 输出前对照 [output contract](references/output-contract.md)
4. 修改前复核 [checklists](references/checklists.md)

## Boundaries

- 禁止一上来全仓库搜索
- 禁止把多个猜测动作词混成一条长正则
- 两轮定位失败后必须回退重写假设，不继续扩大关键词
