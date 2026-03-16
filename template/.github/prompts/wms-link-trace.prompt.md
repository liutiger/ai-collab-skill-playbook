---
description: "WMS 链路确认：确认真实执行链路、分支和副作用，并沉淀到 docs"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/08-link-confirmation.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 先界定起点、终点和范围
2. 以真实代码顺序列出主链路和关键分支
3. 区分 DB 写入、MQ、Feign 等副作用
4. 把结果写入 docs/tasks 对应任务目录的 artifacts/link-trace.md
