---
description: "WMS 新功能方案确认：先定位上下文、给最小改动方案并停在待确认"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/09-plan-gate.md
#file:docs/prompts/01-feature-dev.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 先按 Planner / Context Analyst / Solution Architect 输出
2. 优先 GitNexus，不要直接全项目搜索
3. 停在“待确认”，不要进入实现
4. 结果写入 docs/tasks 对应任务目录的 artifacts/plan-gate.md
