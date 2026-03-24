---
description: "WMS 模式入口：AOD（分析观察驱动），先补证、看日志、做链路和假设收敛，再决定是否修复"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/15-governance-lifecycle-contract.md
#file:docs/prompts/14-mode-catalog.md
#file:docs/prompts/19-aod-mode.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

共享治理生命周期合同：
1. 开始当前轮次前，先读取最新团队规范源、回查任务文档新增补充要求，并写入本轮 `规划任务:` 标记；若涉及命令执行，优先准备 tmux
2. 准备结束当前轮次前，必须执行共享结束协议：回查 README 与 artifacts、判断是否允许写完成标记，并显式确认“本文档中的任务是否已经处理完毕”；若平台不支持输入框，则默认按“需要继续检查文档”处理
3. 若本轮存在必须确认的 hard gate，必须一次性汇总所有 hard gate；用户在同一线程回复后，默认沿当前总控入口继续，不要求重新切换 prompt 或重开会话

本入口专项要求：
1. 把当前任务固定在 AOD 模式，优先做证据盘点、链路观察和假设收敛
2. 先明确已知证据、缺失证据、下一步验证动作和止血建议，不把猜测写成结论
3. 适合线上排障、数据不一致、链路不清或用户只给现象不给明确需求的任务
4. 若边界和方案已经收敛，可切到 ACD；若验收可测试且允许实现，可切到 TDD
