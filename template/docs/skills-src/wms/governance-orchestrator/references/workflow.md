# Governance Orchestrator Workflow

## 1. 先判主场景

根据 `12-scene-catalog.md` 先判：

- 新功能开发
- 线上问题排查
- 代码审查
- 数据库变更
- 重构优化
- 文档编写

最多允许一个次场景。

## 2. 再判执行策略

根据 `14-mode-catalog.md` 选择最合适的执行策略：

- `tdd-mode`
- `acd-mode`
- `aod-mode`

优先依据任务的风险、边界清晰度、证据充足度和验收可测试性来决定。

## 3. 再判当前三态

- `DISCOVER`：边界不清 / 高风险 / 多方案 / 线上异常 / 需要证据链
- `DELIVER`：目标清晰且允许继续，可以进入实现
- `VERIFY`：已存在改动，优先评测门禁

## 4. 决定是否叠加专项方法

根据 `13-method-catalog.md` 判断是否需要：

- `link-trace-and-curation`

## 5. 统一确认协议

若存在必须人工确认的 hard gate：

- 一次性列出全部 hard gate
- 区分必须确认与可带假设继续
- 若平台支持 `askQuestions` / 确认框，由适配层承接确认
- 用户在同一线程回复后，默认沿当前总控继续

## 6. 委派协议

若需要分给 subagent：

- 先继承共享治理合同
- 使用 `delegation payload` 传递控制文档路径、本轮规划、非目标和完成标准
- 不允许只丢一个“去看下”式的自由任务

## 7. 收尾协议

- 回查 README 与 artifacts 是否有新增补充要求
- 若未明确确认任务可结束，默认继续检查文档
- 若存在代码 / SQL / 配置改动，默认补评测门禁
