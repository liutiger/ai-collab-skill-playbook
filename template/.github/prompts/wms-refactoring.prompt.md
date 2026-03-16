---
description: "WMS 重构优化：先分级风险，再按行为不变原则拆步落地"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/05-refactoring.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 先划分风险级别和边界
2. 默认保持行为不变，不顺手改无关逻辑
3. 给出分步改造与回滚思路
4. 必要时将方案先沉淀到 docs/tasks 再实施
