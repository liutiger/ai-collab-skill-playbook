---
description: "WMS 代码审查：按严重度优先输出问题，并覆盖正确性、并发和安全"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/03-code-review.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 输出以 findings 为主，不要先写总结
2. 按严重度排序问题，并给出代码位置
3. 优先检查正确性、并发、事务、安全和可维护性
4. 必要时结合 GitNexus 看影响范围
