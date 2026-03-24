---
description: "WMS 模式入口：TDD（测试驱动交付），先收敛验收标准与失败测试，再做最小实现和回归验证"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/15-governance-lifecycle-contract.md
#file:docs/prompts/14-mode-catalog.md
#file:docs/prompts/17-tdd-mode.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

共享治理生命周期合同：
1. 开始当前轮次前，先读取最新团队规范源、回查任务文档新增补充要求，并写入本轮 `规划任务:` 标记；若涉及命令执行，优先准备 tmux
2. 准备结束当前轮次前，必须执行共享结束协议：回查 README 与 artifacts、判断是否允许写完成标记，并显式确认“本文档中的任务是否已经处理完毕”；若平台不支持输入框，则默认按“需要继续检查文档”处理
3. 若本轮存在必须确认的 hard gate，必须一次性汇总所有 hard gate；用户在同一线程回复后，默认沿当前总控入口继续，不要求重新切换 prompt 或重开会话

本入口专项要求：
1. 把当前任务固定在 TDD 模式，不再重新猜测模式
2. 先把验收标准转成可验证的测试或断言，再决定最小改动范围
3. 优先列出要新增或修改的测试点、失败信号和最小实现路径
4. 若中途出现高风险架构取舍，回退到 ACD 风格确认；若证据不足，补充 AOD 式分析后再继续
