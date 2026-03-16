# Workflow

## Phase 1: Evaluation Planner

- 明确改动类型：代码 / SQL / 配置 / 文档
- 明确影响模块和需要覆盖的 Maven 模块
- 区分必跑门禁和条件门禁
- 先写 `artifacts/eval-plan.md`

## Phase 2: Pipeline Runner

默认门禁按以下顺序考虑：

1. 编译门禁：`mvn -pl {模块列表} -am -DskipTests compile`
2. 测试门禁：`mvn -pl {模块列表} -am test`
3. 静态门禁（按风险启用）：`mvn -pl {模块列表} -am -DskipTests spotbugs:spotbugs`

补充规则：

- 文档任务默认无需进入本 Skill
- 纯文案或纯知识沉淀任务不强制跑 Maven 门禁
- 影响 `service` / `web` / 公共接口 / 核心链路时，优先考虑静态门禁
- 若环境、仓库历史债务或依赖问题阻塞执行，必须明确记录为 `BLOCKED`

## Phase 3: Gatekeeper

必须给出以下整体结论之一：

- `PASS`：关键门禁已通过，可进入完成流程
- `CONDITIONAL_PASS`：关键门禁已通过，但存在已说明的非阻断缺口，需要透明记录
- `BLOCKED`：关键门禁未能执行，不能写完成标记
- `FAIL`：关键门禁失败，不能写完成标记

## Exit Rules

- 已生成 `artifacts/eval-plan.md`
- 已生成 `artifacts/eval-report.md`
- 已明确是否允许写完成标记
