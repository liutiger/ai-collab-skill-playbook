---
description: "WMS 单一总控入口：自动判定场景、执行模式、当前阶段和专项方法，默认在同一线程里先收敛、再实现、再验收"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/15-governance-lifecycle-contract.md
#file:docs/prompts/12-scene-catalog.md
#file:docs/prompts/13-method-catalog.md
#file:docs/prompts/14-mode-catalog.md
#file:docs/prompts/16-governance-orchestrator.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

共享治理生命周期合同：
1. 开始当前轮次前，先读取最新团队规范源、回查任务文档新增补充要求，并写入本轮 `规划任务:` 标记；若涉及命令执行，优先准备 tmux
2. 准备结束当前轮次前，必须执行共享结束协议：回查 README 与 artifacts、判断是否允许写完成标记，并显式确认“本文档中的任务是否已经处理完毕”；若平台不支持输入框，则默认按“需要继续检查文档”处理
3. 若本轮存在必须确认的 hard gate，必须一次性汇总所有 hard gate；用户在同一线程回复后，默认沿当前总控入口继续，不要求重新切换 prompt 或重开会话

本入口专项要求：
1. 默认先用统一场景目录判主场景，再结合模式目录选择 TDD / ACD / AOD 中最合适的执行模式
2. 高风险、跨模块、公共接口或方案存在取舍时，自动收敛到 ACD 风格的方案确认，不直接进入实现
3. 若任务以证据链、日志、链路、副作用为主，自动切到 AOD 风格的分析补证；若目标明确且验收可测试，优先采用 TDD 风格
4. 若存在必须确认的阻塞点，必须一次性汇总全部 hard gate；用户在同一线程答复后沿当前总控继续，不要求切换到别的 prompt
