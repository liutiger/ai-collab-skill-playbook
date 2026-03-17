# 提示词 04 — 数据库变更场景检查包

> 对话开头可引用 `#file:docs/prompts/04-database-change.md`。
> 更推荐先走 `#file:docs/prompts/11-scene-router.md` 判定场景，再叠加 `09-plan-gate.md` 或 `07-auto-dev-orchestration.md`。
>
> **兼容入口**：本场景的权威工作法以 `database-change-scene` 为准。
> 这是场景检查包，不承担完整共性流程。

---

## 何时使用

- 涉及 DDL、DML、索引、字段、表结构或数据修复
- 需要评估 SQL 本身之外的 Mapper、DTO、同步链路和回滚风险
- 目标是做安全数据库变更，不是普通功能补充

## 不用于

- 只改 Java 代码、不碰数据面：优先别用本包
- 只是链路确认：改走 `08-link-confirmation.md`
- 只是交付验收：改走 `10-evaluation-gate.md`

---

## 场景判定信号

- 常见用户表达：`加字段`、`改索引`、`补 SQL`、`数据修复`
- 常见产出：DDL、DML、回滚方案、验证 SQL、联动代码清单

---

## 专项检查重点

### 1. 联动影响

- Entity、Mapper XML、DTO、Service、同步链路是否受影响
- 改字段前先确认代码引用是否已经移除或兼容

### 2. DDL / DML 风险

- 锁表、分批、执行窗口、默认值、索引策略
- 数据量级、回填方式、是否支持在线变更

### 3. 回滚与验证

- 先 SELECT 再 UPDATE
- 每批次控制影响范围
- 变更后有明确校验 SQL 和回滚路径

### 4. 交付门禁

- 数据库变更通常属于高风险，默认先过方案关卡
- 实施后仍要进入评测门禁，至少给出应用侧验证结论

---

## 默认产出物

- `artifacts/ddl-*.sql`
- `artifacts/dml-data-fix-*.sql`
- `artifacts/eval-report.md`
- `knowledge-base/database/*.md`

---

## 推荐组合

- 先评审方案：`00 + 11 + 09 + 04`
- 方案确认后执行：`00 + 11 + 07 + 04`
- 变更后验收：`00 + 10`

---

## 场景自检

1. [ ] 已同时看 SQL 风险和应用联动风险
2. [ ] 已准备执行验证与回滚方案
3. [ ] 高风险 DDL / 跨模块联动已先走方案关卡
4. [ ] 变更完成后会进入评测门禁，不直接写完成标记
5. [ ] SQL 与知识沉淀会写入 `artifacts/` 或 `knowledge-base/database/`
