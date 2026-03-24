# GitHub Copilot 工作区指令 — example-wms-project

> 本文件由 `docs/skills-src/copilot-src/repository-instructions.md` 和 `docs/skills-src/manifest.yaml` 生成，不要直接编辑 `.github/copilot-instructions.md`
> GitHub Copilot Chat 不会直接读取 `.claude/skills/wms/`；请依赖本文件的自动路由规则，或主动使用 `/wms-*` slash prompt
> 本文件是《AI协作研发章程》的 GitHub Copilot 适配层，不是独立规范；若与 `docs/guides/AI协作研发章程.md` 冲突，以章程为准

## 项目概览

仓储管理系统（WMS），Spring Boot 2.7.1 / Java 17 / MyBatis Plus 3.5.2。  
主仓储业务在 `example-*` 多模块中协作完成，涉及入库、出库、调拨、波次、库存抵扣、签收与跨服务同步。

### 关键模块定位

| 模块 | 职责 |
|---|---|
| `example-web` | 主仓库 REST Controller |
| `example-service` | 核心业务实现（入库/出库/调拨/波次） |
| `example-service-interface` | 所有 Service 接口定义 |
| `example-datasource` | 实体 / Mapper / MyBatis 配置 |
| `example-deduction` | 库存抵扣引擎 |
| `example-sign-web` | 签收 REST Controller |
| `example-feign-service` | Feign 服务实现 |

## 核心工作规则

- 先遵守 `docs/guides/AI协作研发章程.md`，再执行本文件中的 Copilot 路由规则
- 第一版试运行以 `docs/guides/AI协作试运行说明.md` 作为人类研发同学的最小上手入口
- 默认由 `/wms-orchestrator` 自动判场景、选模式、定阶段、叠加方法
- 涉及代码定位、调用链分析、影响评估时，默认顺序：`GitNexus > 局部 rg > 全项目搜索`
- 高风险需求、边界不清改动、跨模块功能，默认收敛到 ACD 风格确认
- 涉及代码 / SQL / 配置改动时，完成前默认补一次 `evaluation-gate`
- 每次任务尽量落到 `docs/tasks/{年份}/{MM}-{任务名}/`
- 有复用价值的结论继续沉淀到 `docs/knowledge-base/`

## 五层默认架构

1. `Governance`：共享开始 / 结束合同
2. `Orchestrator`：单一总控入口
3. `Scene`：任务主场景检查包
4. `Stage`：兼容阶段入口与评测门禁
5. `Method`：可叠加的专项方法

> `TDD / ACD / AOD` 属于 **Orchestrator 之下的执行模式**，不是第六层架构。

## 任务自动路由

当用户没有显式使用 slash prompt 时，请按下面的信号优先匹配工作流：

| 分类 | 用户信号 | 优先工作流 | 说明 |
|---|---|---|---|
| 总控 | `新增功能` / `线上异常` / `帮我 review` / `DDL` / `重构` / `写文档` / `修复 bug` / `先出方案` | `/wms-orchestrator` | WMS 单一总控入口：自动判定场景、执行模式、当前阶段和专项方法，默认在同一线程里先收敛、再实现、再验收 |
| 阶段 | `自动评测` / `验收门禁` / `评测流水线` / `跑测试后给结论` | `/wms-evaluation-gate` | WMS 自动评测与交付验收门禁：确定评测范围、执行必要门禁、输出结构化评测结论，并决定是否允许完成 |
| 专项方法 | `确认链路` / `有没有真正落盘` / `MQ 链路` / `副作用点` | `/wms-link-trace` | WMS 专项方法：链路确认，确认真实执行链路、分支和副作用，并沉淀到 docs |
| 模式 | `TDD` / `测试驱动` / `先写测试` / `先红后绿` | `/wms-tdd` | WMS 模式入口：TDD（测试驱动交付），先收敛验收标准与失败测试，再做最小实现和回归验证 |
| 模式 | `ACD` / `架构确认` / `先确认方案` / `跨模块方案` | `/wms-acd` | WMS 模式入口：ACD（架构确认驱动），先收敛边界、方案与接口，再决定是否进入实现 |
| 模式 | `AOD` / `先分析再动手` / `证据链` / `先排查补证` | `/wms-aod` | WMS 模式入口：AOD（分析观察驱动），先补证、看日志、做链路和假设收敛，再决定是否修复 |

如果同时命中多个信号：

- 先让 `/wms-orchestrator` 判一个主场景
- 再决定当前模式是 TDD / ACD / AOD
- 最后才决定是否叠加 `link-trace` 这类专项方法

## 推荐 slash prompts

这些 prompt file 由 `docs/skills-src` 自动生成，适合在 VS Code Copilot Chat 中直接使用：

| 分类 | Slash Prompt | 用途 | 兼容入口 |
|---|---|---|---|
| 总控 | `/wms-orchestrator` | WMS 单一总控入口：自动判定场景、执行模式、当前阶段和专项方法，默认在同一线程里先收敛、再实现、再验收 | `00-department-standards.md` + `15-governance-lifecycle-contract.md` + `12-scene-catalog.md` + `13-method-catalog.md` + `14-mode-catalog.md` + `16-governance-orchestrator.md` |
| 阶段 | `/wms-evaluation-gate` | WMS 自动评测与交付验收门禁：确定评测范围、执行必要门禁、输出结构化评测结论，并决定是否允许完成 | `00-department-standards.md` + `15-governance-lifecycle-contract.md` + `10-evaluation-gate.md` |
| 专项方法 | `/wms-link-trace` | WMS 专项方法：链路确认，确认真实执行链路、分支和副作用，并沉淀到 docs | `00-department-standards.md` + `15-governance-lifecycle-contract.md` + `13-method-catalog.md` + `08-link-confirmation.md` |
| 模式 | `/wms-tdd` | WMS 模式入口：TDD（测试驱动交付），先收敛验收标准与失败测试，再做最小实现和回归验证 | `00-department-standards.md` + `15-governance-lifecycle-contract.md` + `14-mode-catalog.md` + `17-tdd-mode.md` |
| 模式 | `/wms-acd` | WMS 模式入口：ACD（架构确认驱动），先收敛边界、方案与接口，再决定是否进入实现 | `00-department-standards.md` + `15-governance-lifecycle-contract.md` + `14-mode-catalog.md` + `18-acd-mode.md` |
| 模式 | `/wms-aod` | WMS 模式入口：AOD（分析观察驱动），先补证、看日志、做链路和假设收敛，再决定是否修复 | `00-department-standards.md` + `15-governance-lifecycle-contract.md` + `14-mode-catalog.md` + `19-aod-mode.md` |

使用原则：

- 日常绝大多数任务默认先用 `/wms-orchestrator`
- 只有当你明确知道当前任务必须固定在某种模式时，才直接用 `/wms-tdd`、`/wms-acd` 或 `/wms-aod`
- 只有当你明确只想确认真实链路时，才直接用 `/wms-link-trace`
- 涉及代码 / SQL / 配置改动时，完成前补用 `/wms-evaluation-gate`

## 路径级说明

这些 path instructions 也由 `docs/skills-src` 自动生成：

| 运行产物 | 源码 |
|---|---|
| `instructions/wms-java.instructions.md` | `wms-java.instructions.md` |
| `instructions/docs-tasks.instructions.md` | `docs-tasks.instructions.md` |

## 兼容入口

如果当前环境没有出现 slash prompt，仍可在聊天内容中显式引用：

```text
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/15-governance-lifecycle-contract.md
#file:docs/prompts/12-scene-catalog.md
#file:docs/prompts/13-method-catalog.md
#file:docs/prompts/14-mode-catalog.md
#file:docs/prompts/16-governance-orchestrator.md

[任务描述]
```
