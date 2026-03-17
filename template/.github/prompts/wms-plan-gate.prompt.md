---
description: "WMS 通用方案确认总控：先经场景路由判主场景，再澄清目标、定位上下文、给最小方案并停在待确认"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/11-scene-router.md
#file:docs/prompts/09-plan-gate.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 先通过 scene-router 判定主场景；若无法明确，停在待确认
2. 明确该主场景的专项检查重点、风险控制和产出物要求
3. 再按 Planner / Context Analyst / Solution Architect 输出
4. 若命中章程高风险条件（边界不清 / 跨模块 / 跨服务 / 公共接口 / 核心链路 / 方案存在取舍），必须停在“待确认”，不要进入实现
