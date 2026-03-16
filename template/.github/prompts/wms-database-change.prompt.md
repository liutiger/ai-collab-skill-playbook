---
description: "WMS 数据库变更评审：关注联动影响、DDL/DML 风险和回滚路径"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/04-database-change.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 确认表结构改动影响的 Mapper、Service、同步链路
2. 评估锁表、分批、回滚和兼容性风险
3. 不要只看 SQL 语句本身，要看调用链和数据面
4. 需要时把方案或评审结论写入 docs/tasks
