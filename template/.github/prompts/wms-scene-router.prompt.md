---
description: "WMS 场景路由入口：先判断这是功能开发、排障、Review、数据库变更、重构还是文档任务，再推荐下一步阶段入口"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/11-scene-router.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 必须在 01~06 中选择一个主场景；必要时最多补一个次场景
2. 输出命中信号、专项检查重点、默认产出物和下一步推荐入口
3. 若边界不清或命中高风险条件，下一步必须推荐 /wms-plan-gate
4. 若改动已存在则优先推荐 /wms-evaluation-gate；若目标是确认真实链路，则优先推荐 /wms-link-trace
