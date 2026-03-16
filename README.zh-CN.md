# AI 协作 Skill Playbook

这是一个把零散 Prompt 升级成“可治理 AI 研发协作体系”的公开模板仓库。

## 它解决什么问题

- Prompt 越写越多，但 AI 还是会跑偏
- 还没确认方案，AI 就开始直接改代码
- 代码搜索逐渐退化成全仓库乱搜
- 关键结论只停留在聊天框里，没有沉淀
- 改完代码就算完成，缺少自动评测和交付门禁

## 这套仓库的回答

```text
章程 -> 工作流 -> Skill -> 工具入口 -> 任务交付 -> 评测门禁 -> 文档沉淀
```

## 主要内容

- `章程`：定义 AI 的定位、边界、控制规则
- `工作流`：把章程落成可执行的团队流程
- `Skill`：把稳定工作方法封装成可复用能力
- `运行产物`：生成给 GitHub Copilot 和 Claude 风格运行时使用
- `知识沉淀`：把过程和结论写入 `docs/tasks/` 和 `docs/knowledge-base/`

## 核心交付路径

```text
plan-gate -> auto-dev -> evaluation-gate -> docs sink
```

## 建议阅读顺序

1. [`template/docs/guides/AI协作试运行说明.md`](./template/docs/guides/AI协作试运行说明.md)
2. [`template/docs/guides/AI协作研发章程.md`](./template/docs/guides/AI协作研发章程.md)
3. [`template/docs/guides/ai-workflow.md`](./template/docs/guides/ai-workflow.md)
4. [`template/docs/prompts/README.md`](./template/docs/prompts/README.md)
5. [`template/docs/skills-src/README.md`](./template/docs/skills-src/README.md)

## 模板结构

- `template/docs/skills-src/`：唯一事实来源
- `template/.claude/skills/`：生成后的 Claude 风格 Skill
- `template/.github/`：生成后的 Copilot 指令和 slash prompt
- `template/docs/prompts/`：兼容 Prompt 入口
- `template/docs/tasks/`：任务沉淀目录和模板

## 如果你要迁移到自己的项目

优先改这几个地方：

- `template/AGENTS.md`
- `template/docs/guides/AI协作研发章程.md`
- `template/docs/prompts/00-department-standards.md`
- `template/docs/skills-src/manifest.yaml`

然后重新生成：

```bash
cd template
python3 docs/skills-src/tools/generate_claude_skills.py
python3 docs/skills-src/tools/generate_copilot_assets.py
```

## 发布前建议

- [仓库结构说明](./docs/repo-structure.md)
- [公开分享检查单](./docs/public-sharing-checklist.md)
- [发布到 GitHub 的步骤](./docs/publish-to-github.md)
