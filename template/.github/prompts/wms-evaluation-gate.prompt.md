---
description: "WMS 自动评测与交付验收门禁：确定评测范围、执行必要门禁、输出结构化评测结论，并决定是否允许完成"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/10-evaluation-gate.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 先判断本次改动的影响模块、改动类型和必须执行的评测门禁
2. 先写出评测计划，再执行编译、测试和按风险需要补充的静态检查门禁
3. 必须输出结构化评测结果，明确 PASS / CONDITIONAL_PASS / BLOCKED / FAIL 结论
4. 若关键门禁失败或未执行，不得写完成标记，必须明确下一步补救动作
