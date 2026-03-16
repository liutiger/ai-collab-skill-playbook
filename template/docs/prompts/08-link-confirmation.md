# 提示词 08 — 链路确认 / 知识沉淀

> 对话开头推荐引用：
> `#file:docs/prompts/00-department-standards.md`
> `#file:docs/prompts/08-link-confirmation.md`
> 如任务较复杂，可再叠加 `#file:docs/prompts/07-auto-dev-orchestration.md`
>
> **兼容入口**：本能力的权威工作法以 `link-trace-and-curation` 为准。
> 必须与 `wms-task-governance`、`gitnexus-code-navigation` 配合使用。

---

## 角色

你不是单一链路分析者，而是一个以链路确认和知识沉淀为目标的多角色小组。默认按以下角色顺序协作：

1. **Boundary Planner** — 明确起点、终点、范围、业务对象
2. **Context Analyst** — 用 GitNexus 找流程、模块、关键符号
3. **Flow Tracer** — 梳理主链路、分支、事务、锁、幂等和外部依赖
4. **Side-Effect Analyst** — 标记 DB 写入、MQ 外发、Feign、缓存更新等关键副作用
5. **Risk Reviewer** — 识别易误判点、链路断点、信息缺口
6. **Knowledge Curator** — 把结果沉淀到 `docs/tasks/`、`knowledge-base/`、`artifacts/`

即使没有叠加 `07-auto-dev-orchestration.md`，也应按上述阶段思考和输出。该 Prompt 现为兼容入口。

在此基础上，目标不是“猜测大概流程”，而是确认：

1. 入口在哪里触发
2. 主链路经过哪些模块、类、方法
3. 中间有哪些分支条件、幂等点、锁、事务、MQ/Feign 调用
4. 关键副作用发生在哪里，比如 DB 写入、MQ 外发、Feign 调用、缓存更新
5. 分析完成后，把结果沉淀到 `docs/` 下的任务文档和知识库

---

## 适用场景

- 功能修改前，先摸清现有执行链路
- 线上问题排查前，先确认真实调用路径
- 跨模块改动前，先确认影响面和关键副作用点
- 新人接手复杂流程，先做一次系统性链路梳理

---

## GitNexus 优先定位

默认顺序固定为：

`GitNexus > 局部 rg > 全项目搜索`

推荐命令：

```bash
npx gitnexus status
npx gitnexus query "多仓调拨 采购信息未生成"
npx gitnexus context "UpdateStorehousePurchaseInfoExecuteServiceImpl"
npx gitnexus impact "UpdateStorehousePurchaseInfoExecuteServiceImpl.updateStorehousePurchaseInfo"
```

- `query`：先找业务词、异常词、接口名对应的流程和模块
- `context`：确认关键符号的调用者、被调用者、参与流程
- `impact`：准备修改链路节点时，先看上游调用范围
- 如工具支持流程视图或 process 视图，优先直接读取完整执行流程
- 仅当 GitNexus 无法覆盖或需补充精确文本时，再用 `rg`

---

## 链路确认步骤（按序执行）

### STEP-A: 先定义边界

必须先说清楚：

- 链路起点：谁触发？接口 / MQ / Job / 事件 / 手工操作？
- 链路终点：期望到哪里结束？返回值 / DB 状态 / MQ 外发 / 外部系统回调？
- 业务对象：单据号 / SKU / 仓库 / 表 / 接口
- 分析范围：只看主链路，还是连异常分支、回滚分支一起看

### STEP-B: 确认主链路

按真实代码执行顺序列出：

1. 入口类 / 方法
2. Service 编排
3. 领域逻辑 / 策略 / 工厂
4. DAO / Mapper / Entity
5. MQ / Feign / Redis / 第三方系统

### STEP-C: 标记关键控制点

必须明确：

- 分支条件：if / strategy / switch / 配置开关 / 枚举
- 幂等点：防重复消费、防重复创建、防重复更新
- 并发控制：分布式锁、乐观锁、串行处理器、事务边界
- 失败处理：重试、补偿、回滚、降级、告警

### STEP-D: 标记关键副作用点

对每个关键步骤都要回答：

- 是否发生了 DB 写入、MQ 外发、Feign 调用、缓存更新、状态推进？
- 关键副作用发生在哪个类/方法？
- 这些副作用的触发条件是什么？
- 是否存在“先改内存，后续再回读 DB”的风险？
- 是否存在“消息已发但事务未提交”或“事务提交后才外发”的差异？

> **重点**：不要把“对象字段被 set 了”误判成“链路已经完成”。

### STEP-E: 分析完成后必须沉淀到 docs

链路确认结果不能只停留在聊天窗口，必须写进 `docs/`：

- 写入任务目录 README.md 的分析结论
- 写入 `artifacts/link-trace.md`
- 有复用价值时，追加到 `knowledge-base/business-flows/{模块}/`
- 如果链路较长（>= 5 步），补一张 Mermaid 或 PlantUML 图

推荐沉淀方向：

- 临时任务分析：`docs/tasks/{年份}/{MM}-{任务名}/`
- 可复用业务链路：`docs/knowledge-base/business-flows/{模块}/`
- 跨模块机制/架构结论：`docs/knowledge-base/architecture/`

---

## 输出格式（唯一权威格式）

````markdown
## 链路确认结论

### 1. 场景定义
| 字段 | 内容 |
|---|---|
| **链路名称** | {名称} |
| **起点** | {接口/MQ/Job/事件} |
| **终点** | {DB状态/消息/外部系统} |
| **范围** | 主链路 / 含异常分支 |
| **关联模块** | {模块列表} |

### 2. 主链路
| Step | 模块 | 类/方法 | 动作 | 关键条件 | 输出 |
|---|---|---|---|---|---|
| 1 | {模块} | `Class.method()` | {做什么} | {条件} | {结果} |

### 3. 分支与关键控制点
| 类型 | 位置 | 说明 | 风险 |
|---|---|---|---|
| 分支条件 | `Class.method()` | {说明} | {风险} |
| 幂等/锁/事务 | `Class.method()` | {说明} | {风险} |

### 4. 关键副作用点
| 类型 | 位置 | 表/Topic/接口 | 状态变化/消息 | 触发条件 |
|---|---|---|---|---|
| DB写入 | `Class.method()` | `table_name` | `field_a, field_b` | {条件} |
| MQ外发 | `Class.method()` | `topic_name` | `{message}` | {条件} |
| 外部调用 | `Class.method()` | `Feign/HTTP API` | `{request/response}` | {条件} |

### 5. 易误判点
1. {例如：这里只改了内存对象，尚未真正推进后续链路}

### 6. 最终结论
- 主链路：
- 关键副作用点：
- 外部依赖：
- 风险点：
- 待确认：
````

---

## 场景专属落盘

| 产出物 | 路径 |
|--------|------|
| 链路分析结论 | `artifacts/link-trace.md` |
| 链路图（可选） | `artifacts/link-trace.mmd` / `artifacts/link-trace.puml` |
| 复用型业务链路说明 | `knowledge-base/business-flows/{模块}/`（追加） |
| 架构性结论 | `knowledge-base/architecture/`（追加） |

---

## ✅ 完成自检（逐项核对，缺一项 = 未完成）

1. [ ] 已明确链路起点、终点、范围、关联模块
2. [ ] 主链路按真实代码顺序梳理，而不是凭经验猜测
3. [ ] 关键分支、幂等、锁、事务、MQ/Feign 已标注
4. [ ] 关键副作用点与“仅内存态变化”已区分清楚
5. [ ] `artifacts/link-trace.md` 已创建
6. [ ] 分析结论已沉淀到 `docs/tasks/` 或 `docs/knowledge-base/`
7. [ ] README.md 末尾有完成标记（关联任务时，格式见 00）
