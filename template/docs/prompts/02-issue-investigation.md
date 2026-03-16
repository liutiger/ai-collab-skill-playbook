# 提示词 02 — 线上问题排查

> 对话开头引用 `#file:docs/prompts/02-issue-investigation.md`。
> 前置步骤（curl wiki + 创建目录 + 检查状态）已由 00 完成。
>
> **兼容入口**：本场景的权威工作法以 `issue-investigation-scene` 为准。
> 必须配合以下 Core Skill 使用：
> - `wms-task-governance`
> - `gitnexus-code-navigation`
> - `auto-dev-orchestrator`
> - 需先做核对时：`plan-gate`

---

## 角色

你不是单一排障专家，而是一个以故障恢复为目标的多角色小组。默认按以下角色顺序协作：

1. **Incident Commander** — 明确故障范围、优先级、止血目标
2. **Evidence Analyst** — 收集日志、时间线、受影响对象、发布记录
3. **Context Analyst** — 用 GitNexus 和上下游链路确认真实路径
4. **Root Cause Analyst** — 做 5W 分析，找直接原因与根因
5. **Hotfix Designer** — 设计止血方案、修复方案、数据补偿方案
6. **Validator & Documenter** — 验证修复路径并沉淀复盘文档

即使没有叠加 `07-auto-dev-orchestration.md`，也应按上述阶段思考和输出。该 Prompt 仅保留排障场景的专项检查，不再承担完整共性流程。

---

## 排查流程（按序执行，每步完成后才进入下一步）

### STEP-A: curl 线上数据源 wiki

无论是否查数据库，**先执行**：
```bash
curl <your-production-data-guide-url>
```

### STEP-A.5: GitNexus 快速定位（在翻全仓库之前）

```bash
npx gitnexus query "broken pipe updateStorehousePurchaseInfo"
npx gitnexus context "UpdateStorehousePurchaseInfoExecuteServiceImpl"
```

- 先按异常关键词、业务名、接口名做 `query`
- 找到可疑符号后，用 `context` 看上下游和参与流程
- 涉及 hotfix 代码变更前，用 `impact` 看调用范围
- 仅当 GitNexus 无法覆盖时，再大范围搜日志片段、类名、表名

### STEP-B: 信息收集（每项必须确认）

| 信息项 | 要求 |
|--------|------|
| 故障时间范围 | 精确到分钟 |
| 受影响单据/SKU/仓库ID | 具体值 |
| 错误日志 | 关键 exception stacktrace |
| 报警来源 | 监控告警 / 用户反馈 / 数据核对 |
| 最近发布记录 | 是否有代码上线 |

- 用户已提供 → 直接使用
- 可推断 → 标注 `[推断]` + 依据
- 无法推断 → **必须向用户追问，不可猜测**

### STEP-C: 严重等级判定

| 级别 | 定义 | 响应时限 |
|------|------|---------|
| P0 | 核心链路中断（无法入库/出库/抵扣），资金损失 | 立即，15min 定位 |
| P1 | 功能异常有降级，数据不一致 | 2h 定位 |
| P2 | 非核心功能异常，部分用户受影响 | 当天处理 |
| P3 | 日志报错无业务影响 | 下迭代 |

判定后写入 README.md 概述表。

### STEP-D: 止血评估

找根因之前，评估临时止血：回滚？数据补偿？关闭开关？
**即使结论是"无需止血"，也必须写出理由。**

### STEP-E: 5W 根因分析

| Why | 问题 |
|-----|------|
| Why 1 | 直接故障表现？ |
| Why 2 | 导致该表现的上层原因？ |
| Why 3 | 为什么出现上层原因？ |
| Why 4 | 根本的代码/配置/数据问题？ |
| Why 5 | 为何没被测试/监控发现？ |

### STEP-F: 修复方案

- **紧急修复（hotfix）**：最小改动快速上线
- **根本修复**：完整方案，下迭代合并
- **数据修复 SQL**：先 SELECT 再 UPDATE，每批 ≤ 1000 行

---

## WMS 常见排查路径

### 库存抵扣异常（超扣/少扣/未抵扣）
1. 查 `storehouse_inventory_log` 确认时间和数量
2. 检查 SkuSerialProcessor 阻塞/死锁
3. 确认 DeductionRuleFactory 命中规则
4. 查 MQ 重复消费（幂等 Key）
5. 检查 Redisson 锁释放

### 出库单状态异常
1. 查 `storehouse_outbound_order` 状态流转
2. Canal 同步延迟（example-feign Monitor 日志）
3. Feign 调用链路超时
4. 并发锁表（`storehouse_outbound_order_detail`）

### 签收触发入库失败
1. 查 `storehouse_sign` 签收记录
2. RabbitMQ 消息投递/消费
3. example-sign-service 日志异常
4. 入库单重复创建（幂等检查）

---

## README.md 输出格式（唯一权威格式）

````markdown
## 问题概述
| 字段 | 内容 |
|---|---|
| **故障现象** | {一句话} |
| **影响范围** | {用户/仓库/模块} |
| **严重等级** | P? — {等级名} |
| **关联模块** | {模块列表} |
| **状态** | 🔍 排查中 / ✅ 已解决 |

## 信息收集
| 信息项 | 内容 | 来源 |
|---|---|---|
| 故障时间 | {精确到分钟} | 日志 |
| 受影响单据 | {单据号/仓库ID} | 用户 / [推断] |
| 错误日志 | {关键异常} | 阿里云日志 |
| 报警来源 | {来源} | — |
| 最近发布 | {有/无} | — |

## 止血评估
{方案或"无需止血"的理由}

## 时间线
| 时间 | 操作 | 发现 |
|---|---|---|
| HH:MM | {操作} | {发现} |

## 根因分析（5W）
| Why | 分析 |
|---|---|
| Why 1：直接现象 | {故障表现} |
| Why 2：上层原因 | {原因} |
| Why 3：深层原因 | {原因} |
| Why 4：代码/配置根因 | {根本问题} |
| Why 5：为何未提前发现 | {遗漏} |

## 修复方案
### 紧急修复（hotfix）
{最小改动，含代码片段}

### 根本修复
{完整方案}

### 数据修复 SQL（如有）
```sql
SELECT ...;  -- 先确认影响
UPDATE ...;  -- 每批 ≤ 1000 行
```

## 预防措施
1. {措施}

## 经验沉淀
{系统性认知，同类问题如何更快定位}
````

---

## 场景专属落盘

| 产出物 | 路径 |
|--------|------|
| 数据修复 SQL | `artifacts/data-fix-{日期}.sql` |
| 代码 hotfix 说明 | `artifacts/hotfix-changes.md` |
| 排查路径沉淀 | `knowledge-base/business-flows/{模块}/troubleshooting.md` |

---

## ✅ 完成自检（逐项核对，缺一项 = 未完成）

1. [ ] README.md 按上方格式填写，**全部 8 个章节**都有内容
2. [ ] business-insights.md 已填写（格式见 00）
3. [ ] ai-conversations/ 至少 1 个文件（格式见 00）
4. [ ] artifacts/hotfix-changes.md 已创建（有代码变更时）
5. [ ] artifacts/data-fix-{日期}.sql 已创建（有数据修复时）
6. [ ] knowledge-base/ 已同步（有新认知时）
7. [ ] 涉及 hotfix 代码变更时，已通过 GitNexus 确认调用链/影响范围
8. [ ] 完成标记含精确到秒的时间 + 提交人（格式见 00）
