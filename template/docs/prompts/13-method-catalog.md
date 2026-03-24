# 提示词 13 — 统一专项方法目录

> 本文件是“专项方法”的唯一事实来源。
> 默认由 `16-governance-orchestrator.md` 决定是否叠加某种专项方法；策略与场景都不直接替代方法。

---

## 总规则

1. 专项方法不是主场景，也不是默认入口，而是叠加在场景与三态之上的专用协议
2. 每轮默认最多启用 2 个专项方法，避免方法之间再次互相干扰
3. 基础方法默认隐式启用：`wms-task-governance`、`gitnexus-code-navigation`
4. 专项方法必须说明：
   - 为什么需要它
   - 它补充了什么额外证据 / 约束 / 产出物
   - 执行后下一步回到哪个三态

---

## 基础方法（默认隐式启用）

### Method 0：任务治理

- 对应 Skill：`wms-task-governance`
- 作用：最新规则、任务目录、规划标记、完成标记、文档闭环、多轮确认
- 默认状态：每次任务都启用，不单独作为 slash prompt

### Method 0.5：GitNexus 导航

- 对应 Skill：`gitnexus-code-navigation`
- 作用：`GitNexus > 局部 rg > 全项目搜索`
- 默认状态：涉及代码理解、链路定位、影响评估时隐式启用，不单独作为 slash prompt

---

## 显式专项方法

## Method 1：链路确认

- 对应入口：`/wms-link-trace`
- 对应 Prompt：`08-link-confirmation.md`
- 对应 Skill：`link-trace-and-curation`

### 适用信号

- 确认真实执行顺序
- 有没有真正落盘 / 发 MQ / 调 Feign
- 想梳理副作用点、关键分支、幂等和事务边界

### 额外价值

- 它补充的是“真实代码链路和副作用证据”，不是普通场景检查
- 常叠加在新功能、线上排障、数据库变更、文档沉淀前

### 默认产出物

- `artifacts/link-trace.md`
- README 中的链路摘要

### 下一步建议

- 默认继续由 `16-governance-orchestrator.md` 统一推进
- 仍需方案确认：回到 ACD 风格收敛
- 链路已清楚且允许落地：进入 TDD / 实现闭环
- 只做知识沉淀：停在当前方法并写 docs

---

## 输出协议

若本轮需要叠加专项方法，输出中至少包含：

```markdown
## 专项方法
- 启用的方法：
- 触发原因：
- 额外证据来源：
- 默认产出物：
- 完成该方法后回到哪个三态：
```
