# 提示词 01 — 新功能场景检查包

> 对话开头可引用 `#file:docs/prompts/01-feature-dev.md`。
> 更推荐先走 `#file:docs/prompts/11-scene-router.md` 判定场景，再叠加 `09-plan-gate.md` 或 `07-auto-dev-orchestration.md`。
>
> **兼容入口**：本场景的权威工作法以 `feature-dev-scene` 为准。
> 这是场景检查包，不承担完整共性流程。

---

## 何时使用

- 目标是新增能力、扩展接口、补一个明确的新业务分支
- 需要判断层次归属、接口边界、读写分离和联动影响
- 已知这是“功能交付”而不是排障、Review、数据库专项或纯文档任务

## 不用于

- 只做方案核对：先走 `09-plan-gate.md`
- 真实链路确认：改走 `08-link-confirmation.md`
- 只做交付验收：改走 `10-evaluation-gate.md`

---

## 场景判定信号

- 常见用户表达：`新增功能`、`补一个能力`、`支持一种新规则`、`确认后再实现`
- 常见产出：接口、实现类、DTO、Mapper、测试、任务文档

---

## 专项检查重点

### 1. 层次归属

- Controller、Interface、Service Impl、Mapper 各落在哪个模块
- 公共能力先定义 Interface，再实现 Service
- 不让 Web 层直连 Mapper / DAO

### 2. Query / Execute 边界

- 只读查询进入 `*QueryService`
- 写操作进入 `*ExecuteService`
- 不混合“查 + 改 + 外部联动”到一个模糊 Service

### 3. 外部依赖与数据面

- 是否新增或修改 DTO、Feign、消息体、枚举、事件
- 是否触发库存、抵扣、状态流转、同步链路
- 若改公共符号或核心链路，必须先确认影响面

### 4. 交付闭环

- 大于单文件的小改动，默认先过方案关卡
- 改完后进入评测门禁，不把“代码写完”视作“任务完成”

---

## 默认产出物

- `artifacts/plan-gate.md`
- `artifacts/eval-plan.md`
- `artifacts/eval-report.md`
- `docs/tasks/.../README.md`
- `business-insights.md`

---

## 推荐组合

- 方案未确认：`00 + 11 + 09 + 01`
- 已确认并开始实现：`00 + 11 + 07 + 01`
- 实现完成后验收：`00 + 10`

---

## 场景自检

1. [ ] 已确认这真的是“功能交付”，不是排障 / Review / 链路确认
2. [ ] 已回答层次归属、Query / Execute、DTO / Feign / 库存影响
3. [ ] 涉及公共接口、跨模块、核心链路时，已先经过方案关卡
4. [ ] 涉及代码 / SQL / 配置改动时，后续会进入 `delivery-evaluation-gate`
5. [ ] 关键结论会沉淀到 `docs/tasks/`
