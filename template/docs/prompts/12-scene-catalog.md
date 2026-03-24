# 提示词 12 — 统一场景目录

> 本文件是 `01~06` 场景专项检查的唯一事实来源。
> `11-scene-router.md` 负责判定主场景，`16-governance-orchestrator.md` 负责推进三态，本文件负责提供每个场景的专项检查点、默认产出物和三态切换建议。

---

## 总规则

1. 每轮只允许一个主场景，必要时最多一个次场景
2. 先判场景，再判三态
3. 高风险、边界不清、跨模块、跨服务、公共接口、数据库结构变更，默认先走 `09-plan-gate.md`
4. 涉及代码 / SQL / 配置改动，落地后默认走 `10-evaluation-gate.md`
5. 真实链路、副作用、有没有真正落盘等问题，优先走 `08-link-confirmation.md`

---

## Scene 1：新功能开发

> 对应 Skill：`feature-dev-scene`

### 适用信号

- 新增能力、扩展接口、补业务分支、支持新规则

### 必答问题

- 层次归属在哪个模块
- Query / Execute 如何分离
- DTO / Feign / 消息 / 枚举会不会受影响
- 是否触发库存、抵扣、状态流转、同步链路

### 专项检查重点

- 公共能力先定义 Interface，再实现 Service
- 不让 Web 层直连 Mapper / DAO
- 改公共符号或核心链路前先看影响面
- 改完后必须进评测门禁，不把“代码写完”视作“任务完成”

### 默认产出物

- `artifacts/plan-gate.md`
- `artifacts/eval-plan.md`
- `artifacts/eval-report.md`
- `docs/tasks/.../README.md`
- `business-insights.md`

### 默认三态切换

- 方案不稳：`09`
- 方案已确认：`07`
- 实施完成：`10`

---

## Scene 2：线上问题排查

> 对应 Skill：`issue-investigation-scene`

### 适用信号

- 线上异常、日志报错、数据不一致、链路中断、补偿排查

### 必答问题

- 故障时间和影响范围是什么
- 是否需要止血
- 根因证据链是否完整
- 是否需要 SQL / 重放 / 补单 / hotfix

### 专项检查重点

- 先时间线，再根因
- 即使“不需要止血”，也要写依据
- 5W 分析要区分直接现象、上层原因、根因和漏检原因
- 热修和根治方案分开讲

### 默认产出物

- `artifacts/hotfix-changes.md`
- `artifacts/data-fix-*.sql`
- `docs/tasks/.../README.md`
- `business-insights.md`

### 默认三态切换

- 先收敛与评估：`09`
- 先确认真实链路：`08`
- 方案确认后修复：`07`
- 修复完成：`10`

---

## Scene 3：代码审查

> 对应 Skill：`code-review-scene`

### 适用信号

- Review PR、审 diff、查风险、找回归点

### 必答问题

- 阻断问题有哪些
- 正确性、事务、幂等、并发、安全有没有问题
- 缺了哪些测试
- 哪些问题只是建议，不该和阻断级混在一起

### 专项检查重点

- findings 优先，先问题后总结
- 按严重度排序
- 尽量给类 / 方法 / 位置
- 关注正确性、并发、事务、安全、可维护性

### 默认产出物

- `docs/reports/code-review/...-review.md`
- 关联任务的 `README.md`
- 必要时更新 `knowledge-base/architecture/`

### 默认三态切换

- 直接审查：停在当前场景
- 若决定修改：转 `09` 或 `07`

---

## Scene 4：数据库变更

> 对应 Skill：`database-change-scene`

### 适用信号

- DDL、DML、字段调整、索引调整、表结构变更、数据修复

### 必答问题

- 会影响哪些 Entity / Mapper / DTO / Service / 同步链路
- 执行窗口、分批、锁表和兼容风险是什么
- 验证 SQL 和回滚方案是什么
- 应用侧需要同步改哪些地方

### 专项检查重点

- 先看应用联动，再看 SQL 本身
- 先 SELECT 再 UPDATE
- 高风险 DDL 默认先走方案关卡
- 变更后仍要给出应用侧验证和评测结论

### 默认产出物

- `artifacts/ddl-*.sql`
- `artifacts/dml-data-fix-*.sql`
- `artifacts/eval-report.md`
- `knowledge-base/database/*.md`

### 默认三态切换

- 默认先 `09`
- 确认后 `07`
- 落地后 `10`

---

## Scene 5：重构优化

> 对应 Skill：`refactoring-scene`

### 适用信号

- 重构、拆分、抽象、简化结构、行为不变优化

### 必答问题

- 风险等级是什么
- 哪些行为绝对不能变
- 提交如何切分
- 出问题如何回滚

### 专项检查重点

- 不借重构顺手改业务
- 高风险核心链路先做 blast radius
- 默认拆成可回滚的小步
- 需要说明行为验证点

### 默认产出物

- `artifacts/refactoring-analysis.md`
- `artifacts/eval-report.md`
- `knowledge-base/architecture/`

### 默认三态切换

- 先 `09`
- 再 `07`
- 完成后 `10`

---

## Scene 6：文档编写

> 对应 Skill：`documentation-scene`

### 适用信号

- 写指南、补说明、沉淀知识、整理流程、输出复盘

### 必答问题

- 写给谁看
- 文档类型是什么
- 内容证据来自哪里
- 应该落到哪个目录

### 专项检查重点

- 先确定读者、目标和写入位置
- 关键流程与结论必须来自真实代码 / 接口 / 表 / 配置
- 流程类文档优先带 Mermaid / PlantUML
- 已有内容默认更新或追加，不盲目覆盖

### 默认产出物

- 目标文档本身
- 关联任务 `README.md`
- `docs/guides/` 或 `docs/knowledge-base/` 中的更新内容

### 默认三态切换

- 先 `09`
- 再 `07`
- 如需链路确认，可叠加 `08`
