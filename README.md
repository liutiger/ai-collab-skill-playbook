# AI Collab Skill Playbook

一个面向真实研发协作的 Prompt → Skill → Copilot/Claude 适配示例仓库。

这个仓库整理的是一套可复用的方法，而不是某个业务系统的私有实现。它把 AI 协作拆成四层：

1. `章程`：定义定位、边界、风险控制和知识沉淀要求
2. `工作流`：把章程落成团队可执行的标准流程
3. `Skill`：把稳定工作方法封装成可复用能力
4. `工具入口`：把 Skill 适配到 GitHub Copilot、Claude 风格运行时和兼容 Prompt

## 适合谁

- 想把“几段 prompt”升级成“团队工作体系”的工程团队
- 想把 Copilot / Claude / Codex 入口统一到一套治理逻辑的人
- 想解决 AI 长链路任务容易跑偏、不会沉淀、不会验收的问题的人

## 仓库包含什么

- [`docs/`](./docs/)：这套方法怎么设计、怎么公开分享、怎么迁移
- [`template/`](./template/)：一个可直接复制到项目里的示例包
- [`template/docs/skills-src/`](./template/docs/skills-src/)：Skill 源码、生成脚本、校验脚本、验收样例
- [`template/docs/prompts/`](./template/docs/prompts/)：兼容 Prompt 入口
- `template/.github/`、`template/.claude/skills/`：由 Skill 源码生成的运行产物

## 模板结构

模板包当前保留了一个 “WMS 风格示例命名空间”，方便展示多模块业务项目里的典型做法：

- 核心 Skill：任务治理、代码导航、方案关卡、自动开发编排、链路确认、交付评测门禁
- 场景 Skill：新功能、排障、Code Review、数据库变更、重构、文档
- GitHub Copilot 入口：slash prompt + repository/path instructions
- Claude 风格运行时入口：`.claude/skills/`

如果你要迁移到自己的项目，通常只需要：

1. 改 `AGENTS.md` 项目上下文
2. 改 `docs/guides/AI协作研发章程.md`
3. 改 `docs/prompts/00-department-standards.md` 中的规范来源和目录约定
4. 改 `docs/skills-src/manifest.yaml` 里的命名空间、提示词描述和生成目标
5. 重新生成 `.github/` 和 `.claude/skills/`

## 快速开始

```bash
cd template

python3 docs/skills-src/tools/validate_skills.py
python3 docs/skills-src/tools/validate_copilot_assets.py
python3 docs/skills-src/tools/generate_claude_skills.py
python3 docs/skills-src/tools/generate_copilot_assets.py
python3 docs/skills-src/tools/acceptance_check.py
```

然后按下面顺序读：

1. [`template/docs/guides/AI协作试运行说明.md`](./template/docs/guides/AI协作试运行说明.md)
2. [`template/docs/guides/AI协作研发章程.md`](./template/docs/guides/AI协作研发章程.md)
3. [`template/docs/guides/ai-workflow.md`](./template/docs/guides/ai-workflow.md)
4. [`template/docs/skills-src/README.md`](./template/docs/skills-src/README.md)

## GitHub 发布前建议

- 先看 [`docs/public-sharing-checklist.md`](./docs/public-sharing-checklist.md)
- 再看 [`docs/repo-structure.md`](./docs/repo-structure.md)
- 真正准备推远端时，再看 [`docs/publish-to-github.md`](./docs/publish-to-github.md)
- 确认已经替换掉你的内网链接、真实模块名、内部系统缩写和敏感命令

## 当前定位

这是一个第一版的公开整理包，重点是：

- 让别人看懂这套体系为什么这样设计
- 让别人能把模板复制到自己的仓库试起来
- 让别人知道 Prompt、Skill、Copilot 入口和验收之间的关系

它不是一个通用 SaaS，也不是一个“一键自动接入所有仓库”的工具。
