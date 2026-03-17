---
description: "WMS 通用多角色自动开发总控：先经场景路由判主场景，再在满足条件时进入分析、实现、自检、评测门禁、落盘闭环"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/11-scene-router.md
#file:docs/prompts/07-auto-dev-orchestration.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 先通过 scene-router 判定主场景或标记为跨场景，并先说明采用的专项检查点
2. 若场景不清或命中章程高风险条件（边界不清 / 跨模块 / 跨服务 / 公共接口 / 核心链路 / 方案存在取舍），先停在方案阶段，待人工确认后再实现
3. 确认可以继续后，再按 Planner / Context Analyst / Solution Architect / Implementer / Reviewer & Tester / Evaluator / Gatekeeper / Documenter 分阶段执行
4. 结束前必须完成自检、评测门禁结论和 docs/tasks 沉淀；若门禁未通过，不得写完成标记
