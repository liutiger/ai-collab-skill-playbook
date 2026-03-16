---
description: "WMS 新功能实现闭环：分析、实现、自检、测试和文档沉淀"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/07-auto-dev-orchestration.md
#file:docs/prompts/01-feature-dev.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

执行要求：
1. 若命中章程高风险条件（边界不清 / 跨模块 / 跨服务 / 公共接口 / 核心链路 / 方案存在取舍），先切到 plan-gate 风格，停在待确认
2. 若任务目录不存在，先初始化 docs/tasks 目录
3. 先更新任务文档，再进入代码实现
4. 改完后必须做自检和测试，并补齐评测门禁结论
5. 把结果继续沉淀到 docs/tasks 和 business-insights.md；无 eval-report 时不得视为完成
