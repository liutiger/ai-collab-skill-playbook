# Platform Confirmation Adapter

`Human Confirmation Contract` 是治理协议，不是某个平台工具名。

Skill 只需要声明：

- 这里必须发起确认
- 默认选项应为“需要继续检查文档”
- 未确认前不得进入完成态

具体如何发起确认，由平台适配层决定：

## 平台映射

- VS Code / 支持 `askQuestions` 的 IDE：
  - 由适配层调用 `askQuestions`
  - 默认选项设为“需要继续检查文档”
- GitHub Copilot Chat：
  - 显式发问
  - 若未收到确认，默认继续检查文档
- 其他无确认工具的平台：
  - 输出结构化待确认项
  - 在同一线程等待用户回复

## 适配原则

- 不要把 `askQuestions` 写死进治理本体
- 不要让 Skill 假设每个平台都有阻塞式输入框
- 平台能力不足时，退化为“显式发问 + 默认继续检查文档”
