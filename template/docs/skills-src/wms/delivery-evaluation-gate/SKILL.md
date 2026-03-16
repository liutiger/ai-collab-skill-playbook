---
name: delivery-evaluation-gate
description: "Use when a WMS task has changed code, SQL, or key configuration and now needs an explicit automated evaluation gate verdict before it can be treated as complete."
---

# Delivery Evaluation Gate

## When to Use

- 功能、修复、重构、数据库或配置改动已经完成
- 需要把“建议怎么测”升级为“实际评测结论”
- 需要决定本轮是否允许写完成标记

## Pair With

- `wms-task-governance`
- `auto-dev-orchestrator`
- `gitnexus-code-navigation`
- 对应场景薄 Skill

## Workflow

1. 先读 [workflow](references/workflow.md)
2. 先用 `assets/templates/eval-plan.md` 明确评测范围和门禁
3. 需要实际执行 Maven 门禁时，优先使用 `scripts/run_maven_eval_gate.sh`
4. 最终按 [output contract](references/output-contract.md) 输出 `eval-plan` 和 `eval-report`
5. 结束前执行 [checklists](references/checklists.md)

## Boundaries

- 不要把“建议执行命令”伪装成“评测已完成”
- 不要在关键门禁失败或未执行时写完成标记
- 不要跳过结构化评测结论，只写一句“测试通过”
