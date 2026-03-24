---
description: "WMS 模式入口：ACD（架构确认驱动），先收敛边界、方案与接口，再决定是否进入实现"
---

#file:docs/prompts/00-department-standards.md
#file:docs/prompts/15-governance-lifecycle-contract.md
#file:docs/prompts/14-mode-catalog.md
#file:docs/prompts/18-acd-mode.md

任务：
${input:task:描述本次任务、异常或改动目标}

补充信息：
${input:extra:补充验收标准、日志、范围、风险点或可留空}

共享治理生命周期合同：
1. 开始当前轮次前，先读取最新团队规范源、回查任务文档新增补充要求，并写入本轮 `规划任务:` 标记；若涉及命令执行，优先准备 tmux
2. 准备结束当前轮次前，必须执行共享结束协议：回查 README 与 artifacts、判断是否允许写完成标记，并显式确认“本文档中的任务是否已经处理完毕”；若平台不支持输入框，则默认按“需要继续检查文档”处理
3. 若本轮存在必须确认的 hard gate，必须一次性汇总所有 hard gate；用户在同一线程回复后，默认沿当前总控入口继续，不要求重新切换 prompt 或重开会话

本入口专项要求：
1. 把当前任务固定在 ACD 模式，不直接进入实现闭环
2. 先明确边界、约束、候选方案、取舍理由和回滚思路
3. 涉及公共接口、数据库结构、跨模块或跨服务联动时，优先按 ACD 收敛
4. 若方案已清楚且测试路径明确，可转入 TDD；若证据还不够，先补 AOD 式分析
