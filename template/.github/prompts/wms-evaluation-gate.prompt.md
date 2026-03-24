---
description: "WMS 自动评测与交付验收门禁：确定评测范围、执行必要门禁、输出结构化评测结论，并决定是否允许完成"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/15-governance-lifecycle-contract.md
#file:docs/prompts/10-evaluation-gate.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

共享治理生命周期合同：
1. 开始当前轮次前，先读取最新团队规范源、回查任务文档新增补充要求，并写入本轮 `规划任务:` 标记；若涉及命令执行，优先准备 tmux
2. 准备结束当前轮次前，必须执行共享结束协议：回查 README 与 artifacts、判断是否允许写完成标记，并显式确认“本文档中的任务是否已经处理完毕”；若平台不支持输入框，则默认按“需要继续检查文档”处理
3. 若本轮存在必须确认的 hard gate，必须一次性汇总所有 hard gate；用户在同一线程回复后，默认沿当前总控入口继续，不要求重新切换 prompt 或重开会话

本入口专项要求：
1. 先判断本次改动的影响模块、改动类型和必须执行的评测门禁
2. 先写出评测计划，再执行编译、测试和按风险需要补充的静态检查门禁
3. 必须输出结构化评测结果，明确 PASS / CONDITIONAL_PASS / BLOCKED / FAIL 结论
4. 若关键门禁失败或未执行，不得写完成标记，必须明确下一步补救动作
