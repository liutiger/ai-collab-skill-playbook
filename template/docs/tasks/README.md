# 📋 任务管理中心

> 所有任务按 `{年份}/{MM}-{任务名}/` 组织，任务目录保存 AI 协作过程、关键结论和交付验收结果。

## 目录结构

```text
docs/tasks/
├── _templates/
│   ├── TASK_RECORD.md
│   ├── ISSUE_INVESTIGATION.md
│   ├── AI_CONVERSATION.md
│   └── BUSINESS_INSIGHT.md
└── {年份}/
    ├── {MM}-{任务名}/
    └── {MM}-[ISSUE]-{问题简描}/
```

## 命名规范

| 类型 | 目录命名 | 模板 |
|---|---|---|
| 功能开发 / 需求 | `{MM}-{任务名}` | `TASK_RECORD.md` |
| 线上问题排查 | `{MM}-[ISSUE]-{问题简描}` | `ISSUE_INVESTIGATION.md` |

## 创建新任务

```bash
./docs/skills-src/wms/wms-task-governance/scripts/create_task_dir.sh \
  --owner "{姓名}" \
  --module "{模块}" \
  "{任务名}"
```

排障任务可以使用：

```bash
./docs/skills-src/wms/wms-task-governance/scripts/create_task_dir.sh \
  --issue \
  --owner "{姓名}" \
  --module "{模块}" \
  --link-trace \
  "{问题简描}"
```

## 使用建议

- `create_task_dir.sh` 是推荐入口，会自动初始化 `README.md`、`business-insights.md`、`ai-conversations/`、`artifacts/`
- 涉及代码 / SQL / 配置改动时，建议按需带上 `--evaluation-gate`
- 只想预创建链路沉淀文件时，可带 `--link-trace`
- `_templates/` 保留为底层模板，不建议再手工 `mkdir + cp`
- 关键结论优先沉淀到任务目录，再视情况提炼到 `docs/knowledge-base/`
