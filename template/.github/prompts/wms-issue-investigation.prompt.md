---
description: "WMS 线上问题排查：先时间线、止血、5W，再给根因和补偿建议"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/02-issue-investigation.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 先梳理时间线和影响范围
2. 优先给止血建议，不直接拍脑袋给根因
3. 按 5W 分析，并保留数据补偿视角
4. 将结论沉淀到 docs/tasks 对应问题目录
