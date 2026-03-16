# Repo Structure

这个公开仓库建议保持“两层结构”：

## 1. 方法说明层

放在仓库根的 `docs/`，用于说明：

- 这套体系解决什么问题
- 为什么要从 Prompt 演进到 Skill
- 为什么要有章程、工作流、评测门禁和知识沉淀
- 发布前需要脱敏什么

这些文档主要给“看仓库的人”和“准备二次改造的人”。

## 2. 可复制模板层

放在 `template/`，用于承载一个可落地的示例包：

- `AGENTS.md`
- `docs/guides/`
- `docs/prompts/`
- `docs/skills-src/`
- `.github/`
- `.claude/skills/`

这层主要给“准备直接试跑的人”。

## 推荐目录

```text
ai-collab-skill-playbook/
├── README.md
├── docs/
│   ├── repo-structure.md
│   └── public-sharing-checklist.md
└── template/
    ├── AGENTS.md
    ├── docs/
    │   ├── guides/
    │   ├── prompts/
    │   ├── skills-src/
    │   ├── tasks/
    │   ├── knowledge-base/
    │   └── reports/
    ├── .github/
    └── .claude/
```

## 为什么不是直接把内部仓库原样公开

- 内部 Prompt 往往夹带私有模块名、内网链接和历史约定
- 直接公开会让外部读者很难判断哪些是方法，哪些是项目噪音
- 单个业务仓库的上下文过重，不利于别人迁移

更好的做法是：

1. 保留方法骨架
2. 泛化可复用规则
3. 保留少量示例味道
4. 明确哪些地方必须由使用者自己替换
