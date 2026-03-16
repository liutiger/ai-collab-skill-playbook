# Project Context (Example)

这是一个公开模板里的示例 `AGENTS.md`，目的是告诉使用者：项目上下文必须和 Skill / Prompt 分层。

## 你应该在自己的项目里替换什么

- 项目定位与技术栈
- 模块结构
- 关键链路
- 禁止修改的边界
- 推荐的本地验证命令
- GitNexus 或其他代码导航工具的使用方式

## 示例项目形态

- 多模块 Java 服务
- 典型模块：
  - `example-web`
  - `example-service`
  - `example-service-interface`
  - `example-datasource`
  - `example-deduction`
  - `example-feign-service`
- 典型任务：
  - 新功能开发
  - 线上问题排查
  - Code Review
  - 数据库变更
  - 重构优化
  - 文档沉淀
  - 链路确认
  - 自动评测与交付验收

## 设计原则

- 项目上下文放在 `AGENTS.md`
- 协作规则放在 `docs/guides/AI协作研发章程.md`
- 工作方法放在 `docs/skills-src/`
- 兼容入口放在 `docs/prompts/`
- GitHub Copilot 入口放在 `.github/`
- Claude 风格运行时入口放在 `.claude/skills/`
