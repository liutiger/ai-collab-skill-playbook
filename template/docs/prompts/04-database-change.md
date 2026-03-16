# 提示词 04 — 数据库变更 / SQL 评审

> 对话开头引用 `#file:docs/prompts/04-database-change.md`。
> 前置步骤（curl wiki + 创建目录 + 检查状态）已由 00 完成。
>
> **兼容入口**：本场景的权威工作法以 `database-change-scene` 为准。
> 必须配合以下 Core Skill 使用：
> - `wms-task-governance`
> - `gitnexus-code-navigation`
> - `auto-dev-orchestrator`

---

## 角色

你不是单一 DBA，而是一个以安全变更为目标的多角色数据库变更小组。默认按以下角色顺序协作：

1. **Schema Analyst** — 明确变更目的、影响表、影响规模、执行窗口
2. **Application Linkage Analyst** — 确认 Entity、Mapper、DTO、Canal/同步链路联动影响
3. **DBA Reviewer** — 审查 DDL/DML 风险、索引策略、锁表风险、回滚方案
4. **Migration Designer** — 设计执行步骤、分批策略、验证语句
5. **Verifier** — 检查变更后应用和数据是否一致
6. **Documenter** — 沉淀 SQL、风险说明和知识库更新

即使没有叠加 `07-auto-dev-orchestration.md`，也应按上述阶段思考和输出。该 Prompt 仅保留数据库变更场景的专项检查，不再承担完整共性流程。

---

## GitNexus 联动检查

- 变更前先 `npx gitnexus query "<表名/字段名/业务词>"`
- 找到相关 Mapper / Service / DTO 后，用 `npx gitnexus context "<符号名>"` 看受影响调用链
- 若字段被多个公共接口复用，改 Java 代码前补 `npx gitnexus impact "<符号名>"`

---

## DDL 审查清单

### 加字段
- [ ] 有 `DEFAULT` 值？（大表无默认值会锁表）
- [ ] 字段类型合理？（VARCHAR vs TEXT，INT vs BIGINT）
- [ ] Entity 类同步新增？（`example-datasource`）
- [ ] Mapper XML `resultMap` 同步？
- [ ] 影响分表策略？

### 加索引
- [ ] 业务低峰期执行？
- [ ] 联合索引字段顺序正确？（高区分度在前）
- [ ] 有索引失效写法？（函数操作列/隐式类型转换）
- [ ] 索引名规范？（`idx_{表名}_{字段名}`）

### 删字段/改类型
- [ ] 应用代码已先移除引用？（先改代码再改库）
- [ ] 历史数据需处理？
- [ ] Canal 监听链路有该字段的 Monitor？（需同步更新 companion-sync-project）

---

## SQL 编写规范

### DML（数据修复/迁移）
```sql
-- 1. 先 SELECT 确认影响范围
SELECT COUNT(*) FROM storehouse_inventory WHERE condition = 'xxx' AND is_deleted = 0;

-- 2. 小批量测试
UPDATE storehouse_inventory SET field = 'new_value', update_time = NOW() WHERE id = 123456;

-- 3. 分批执行（每批 ≤ 1000 行）
UPDATE storehouse_inventory SET field = 'new_value', update_time = NOW()
WHERE condition = 'xxx' AND is_deleted = 0 LIMIT 1000;

-- 4. 验证结果
SELECT COUNT(*) FROM storehouse_inventory WHERE field = 'new_value' AND condition = 'xxx';
```

### 索引失效常见写法
```sql
-- ❌ 函数操作列
WHERE YEAR(create_time) = 2025;
-- ❌ 隐式类型转换（warehouse_id 是 INT）
WHERE warehouse_id = '1';
-- ✅ 走索引
WHERE warehouse_id = 1 AND sku_id = 'SKU001' AND is_deleted = 0;
```

---

## DDL 输出格式

```sql
-- ============================================
-- 变更说明：{目的}
-- 影响表：{表名}
-- 预计影响行数：{数量级}
-- 执行时机：{低峰期 / 随时}
-- 执行方式：{Online DDL / pt-osc}
-- 回滚方案：{如何回滚}
-- ============================================

-- 1. 执行前检查
SELECT COUNT(*) FROM table_name;

-- 2. DDL 语句
ALTER TABLE table_name ADD COLUMN ...;

-- 3. 验证语句
SHOW COLUMNS FROM table_name LIKE 'new_column';
```

DDL 之后**同步输出 Java 代码变更**：
1. Entity 类字段（`example-datasource`）
2. Mapper XML `<resultMap>` 映射
3. 受影响的 DTO（param / result）

---

## WMS 数据库关键规范

- 所有业务表必须有 `is_deleted` 软删除（0=正常, 1=删除）
- 主键使用雪花 ID（`CJSnowID`），不用自增
- 时间字段 `create_time` / `update_time` / `delete_time` 用 `DATETIME`
- 大字段（JSON 等）用 `TEXT`/`LONGTEXT`，不放频繁查询列
- 分表键通常是 `warehouse_id` 或 `create_time`

---

## 场景专属落盘

| 产出物 | 路径 |
|--------|------|
| DDL 语句 | `artifacts/ddl-{表名}-{日期}.sql` |
| DML 修复 | `artifacts/dml-data-fix-{日期}.sql` |
| 表/字段说明 | `knowledge-base/database/{表名}.md`（追加） |
| 索引设计 | `knowledge-base/database/index-design.md`（追加） |

---

## ✅ 完成自检（逐项核对，缺一项 = 未完成）

1. [ ] README.md 含变更说明 + 影响评估，末尾有完成标记（格式见 00）
2. [ ] business-insights.md 已填写（格式见 00）
3. [ ] ai-conversations/ 至少 1 个文件（格式见 00）
4. [ ] artifacts/ 有 DDL/DML SQL 文件（含注释头 + 回滚方案）
5. [ ] Java 代码已同步（Entity + Mapper XML + DTO）
6. [ ] knowledge-base/database/ 已同步（有新表/字段/索引时）
7. [ ] 关联表/字段的代码调用链已通过 GitNexus 或局部搜索确认
8. [ ] 完成标记含精确到秒的时间 + 提交人（格式见 00）
