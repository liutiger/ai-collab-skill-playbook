# 提示词 05 — 重构优化

> 对话开头引用 `#file:docs/prompts/05-refactoring.md`。
> 前置步骤（curl wiki + 创建目录 + 检查状态）已由 00 完成。
>
> **兼容入口**：本场景的权威工作法以 `refactoring-scene` 为准。
> 必须配合以下 Core Skill 使用：
> - `wms-task-governance`
> - `gitnexus-code-navigation`
> - `auto-dev-orchestrator`

---

## 角色

你不是单一架构师，而是一个以安全演进为目标的多角色重构小组。默认按以下角色顺序协作：

1. **Debt Assessor** — 识别现状问题、重构动机、收益与边界
2. **Context & Impact Analyst** — 用 GitNexus 确认调用链和风险范围
3. **Refactoring Architect** — 设计小步方案、提交切分、回滚策略
4. **Implementer** — 以最小行为变化完成重构
5. **Behavior Guardian & Tester** — 保证行为不变，补充验证和回归重点
6. **Documenter** — 沉淀模式、反模式、性能或架构经验

即使没有叠加 `07-auto-dev-orchestration.md`，也应按上述阶段思考和输出。该 Prompt 仅保留重构场景的专项检查，不再承担完整共性流程。

---

## GitNexus 必做（重构前不可跳过）

1. `npx gitnexus context "<目标符号>"` 看完整上下文
2. `npx gitnexus impact "<目标符号>"` 看上游调用和风险范围
3. 若 GitNexus 提示高风险核心路径，先明确灰度、回滚、测试策略，再继续
4. 仅当需要补精确文本或配置项时，再用 `rg`

---

## 重构前评估（必须先回答）

### 1. 影响范围
- 多少处调用了这段代码？
- 有外部 Feign 接口依赖？
- Canal 同步链路是否监听相关字段？

### 2. 风险评级
| 级别 | 场景 | 要求 |
|------|------|------|
| 🔴 高 | 抵扣引擎、库存核心路径 | 充分测试 + 灰度 |
| 🟡 中 | 业务流程类 Service | 单元测试覆盖 |
| 🟢 低 | 工具类、DTO、命名优化 | 可直接重构 |

### 3. 成本收益
- 重构耗时 vs 当前技术债每周消耗的维护时间
- 是否与紧急业务冲突？

---

## 常见重构场景

### 消除重复代码
识别所有重复位置 → 设计公共抽象 → 逐个替换

### 复杂方法拆分（> 80 行）
按业务步骤拆为私有方法，主方法作为编排。确保提取方法可独立测试。

### 策略模式替换 if-else 链
参考 `StoreHouseInventoryDeductionRuleFactory`：
```java
@Component
public class XxxStrategy implements XxxHandler {
    @Override
    public boolean supports(XxxContext ctx) { return ctx.getType() == 1; }
    @Override
    public void handle(XxxContext ctx) { ... }
}
```

### Query/Execute 分离（违规混合的 Service）
`StorehouseXxxService` → `StorehouseXxxQueryService` + `StorehouseXxxExecuteService`
**接口变更必须先更新 *-interface 模块**。

### 性能优化
- N+1 查询 → 批量查询 + Map 聚合
- 循环内 DB 调用 → 提前批量加载
- 大事务 → 拆分小事务，减少锁持有
- 无索引查询 → 分析执行计划 + 加索引

---

## 输出格式

```markdown
## 重构分析报告

### 现状问题
1. {问题描述 + 代码行定位}

### 重构方案
**方案 A（推荐）**：{描述} | 优点 | 缺点/风险 | 工作量
**方案 B（保守）**：{备选}

### 执行步骤
1. Step 1：{做什么}（可独立提交）
2. Step 2：...

### 重构后代码
{完整代码}

### 测试建议
- 单元测试：覆盖场景
- 集成测试：行为不变验证
- 回归重点：{模块}

### 风险提示
{注意事项}
```

---

## 专项约束

- 抵扣引擎重构**必须**保留 `SkuSerialProcessor` 串行语义
- Feign 接口签名变更需同时改 `example-feign-interface` + 提供方
- TaskHandler 变更需确认 `TaskHandlerFactory` 自动注册仍有效

---

## 场景专属落盘

| 产出物 | 路径 |
|--------|------|
| 重构分析报告 | `artifacts/refactoring-analysis.md` |
| 架构模式沉淀 | `knowledge-base/architecture/`（追加） |
| 反模式记录 | `knowledge-base/architecture/anti-patterns.md`（追加） |
| 性能数据 | `knowledge-base/architecture/performance.md`（追加） |

---

## ✅ 完成自检（逐项核对，缺一项 = 未完成）

1. [ ] README.md 含重构目标 + 风险评估 + 决策理由，末尾有完成标记（格式见 00）
2. [ ] business-insights.md 已填写（格式见 00）
3. [ ] ai-conversations/ 至少 1 个文件（格式见 00）
4. [ ] artifacts/refactoring-analysis.md 已创建
5. [ ] knowledge-base/architecture/ 已同步（有新模式/反模式时）
6. [ ] 目标符号已完成 GitNexus context/impact 分析
7. [ ] 完成标记含精确到秒的时间 + 提交人
