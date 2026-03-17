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
- 先判断任务属于哪个场景，再进入对应阶段工作流
- 涉及代码定位、调用链分析、影响评估时，默认顺序：`GitNexus > 局部 rg > 全项目搜索`
- 高风险需求、边界不清改动、跨模块功能，默认先停在 `plan-gate`
- 涉及代码 / SQL / 配置改动时，完成前默认补一次 `evaluation-gate`
- 每次任务尽量落到 `docs/tasks/{年份}/{MM}-{任务名}/`
- 有复用价值的结论继续沉淀到 `docs/knowledge-base/`

## 第一版试运行默认策略

- 默认先进入 `/wms-scene-router` 做场景归类，再决定下一步阶段入口
- 用户表达不清、边界不清、跨模块、跨服务、涉及公共接口或核心链路时，默认先进入 `/wms-plan-gate`
- 只有在目标、范围、方案和风险已明确后，才进入 `/wms-auto-dev`
- 代码 / SQL / 配置改动完成后，默认进入 `/wms-evaluation-gate` 再决定是否允许完成
- 默认把“会不会稳定使用”放在“会不会自动化很多”之前，不主动追求过度自动执行

## 架构约束

### 分层规则

`Controller -> Service Impl -> Service Interface -> Datasource (Entity/Mapper)`

- Web 层禁止直接调用 Mapper / DAO
- 公共接口先在 `*-interface` 模块定义，再在 `*-service` 实现
- 微服务间禁止直连数据库，必须通过 Feign

### Query / Execute 分离

- `*QueryService`：只读查询，不写数据
- `*ExecuteService`：写操作 / 命令，不承担无关查询
- 新建服务必须遵守此约定

### 抵扣引擎高风险点

- 修改抵扣逻辑前，先确认 `SkuSerialProcessor` 串行约束
- 修改规则分发前，先看 `StoreHouseInventoryDeductionRuleFactory` 影响范围

## 任务自动路由

当用户没有显式使用 slash prompt 时，请按下面的信号优先匹配工作流：

{{ROUTING_TABLE}}

如果同时命中多个场景：

- 优先满足风险更高的工作流
- 先用 `/wms-scene-router` 定一个主场景，再进入对应阶段入口
- 若用户表达了“先出方案、确认后再做”，优先进入 `plan-gate` 风格
- 若用户表达了“确认链路、有没有真正落盘/发消息”，优先进入 `link-trace` 风格
- 若仍然不明确，先问最少的澄清问题，或先按 `plan-gate` 收敛

## 推荐 slash prompts

这些 prompt file 由 `docs/skills-src` 自动生成，适合在 VS Code Copilot Chat 中直接使用：

{{PROMPT_TABLE}}

使用原则：

- 默认先用 `/wms-scene-router` 定场景
- 场景不清或跨场景：优先用 `/wms-plan-gate`
- 只有在满足章程中的人工确认要求后，才直接进入 `/wms-auto-dev`

## 路径级说明

这些 path instructions 也由 `docs/skills-src` 自动生成：

{{PATH_INSTRUCTION_TABLE}}

## 兼容入口

如果当前环境没有出现 slash prompt，仍可在聊天内容中显式引用：

```text
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/0x-xxx.md

[任务描述]
```

其中：

- `00-department-standards.md` 是每次都应带的兼容入口
- `11-scene-router.md` 用于先判场景，再选阶段
- `07-auto-dev-orchestration.md` 用于完整开发闭环
- `08-link-confirmation.md` 用于链路确认与知识沉淀
- `09-plan-gate.md` 用于先方案后实现
