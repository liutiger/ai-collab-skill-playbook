# WMS Skill Source

> 这是公开模板的 Skill 源码目录，也是当前模板 Prompt / Skill / Copilot 适配的唯一事实来源。

`docs/skills-src/` 是唯一 Source of Truth，但它不是治理总纲。治理关系固定为：

`AI协作研发章程 > AI协作试运行说明 > ai-workflow > docs/skills-src > .claude/skills/.github/prompts`

## 当前默认架构

这套模板现在明确区分五层：

- `governance`：共享开始 / 结束合同
- `orchestrator`：单一总控 Skill
- `scene`：任务主场景检查包
- `stage`：兼容阶段入口
- `method`：可叠加的专项方法

> `TDD / ACD / AOD` 属于 **Orchestrator 之下的执行模式**，不是新增架构层。

当前默认只保留以下主动运行 Skill：

- `governance-orchestrator`

以下内容保留在源码层，但不再作为默认主动运行 Skill：

- `wms-task-governance`
- `gitnexus-code-navigation`
- `01~06` 对应场景 Skill
- `plan-gate`
- `auto-dev-orchestrator`
- `delivery-evaluation-gate`
- `link-trace-and-curation`
- `tdd-mode`
- `acd-mode`
- `aod-mode`

## 快速启动

任务目录初始化优先使用：

```bash
docs/skills-src/wms/wms-task-governance/scripts/create_task_dir.sh \
  --owner "your-name" \
  --module "example-service" \
  --plan-gate \
  --evaluation-gate \
  "inventory-batch-rule"
```

脚本会自动初始化：

- `README.md`
- `business-insights.md`
- `ai-conversations/01-任务启动.md` 或 `01-初步分析.md`
- `artifacts/plan-gate.md` / `artifacts/link-trace.md`（按参数启用）
- 新任务的第 1 次 `规划任务:` 标记

## Copilot 快速使用

生成 Copilot 运行产物后，可在 VS Code Copilot Chat 中直接使用：

- `/wms-orchestrator`
- `/wms-tdd`
- `/wms-acd`
- `/wms-aod`
- `/wms-link-trace`
- `/wms-evaluation-gate`

使用建议：

- 日常默认先用 `/wms-orchestrator`
- 只有当你明确要固定执行模式时，再用 `/wms-tdd`、`/wms-acd`、`/wms-aod`
- 只有当你明确只想做专项方法时，再用 `/wms-link-trace`
- 涉及代码 / SQL / 配置改动时，完成前补用 `/wms-evaluation-gate`

## 常用命令

```bash
python3 docs/skills-src/tools/validate_skills.py
python3 docs/skills-src/tools/validate_copilot_assets.py
python3 docs/skills-src/tools/generate_claude_skills.py --check
python3 docs/skills-src/tools/generate_claude_skills.py
python3 docs/skills-src/tools/generate_copilot_assets.py --check
python3 docs/skills-src/tools/generate_copilot_assets.py --clean-stale
python3 docs/skills-src/tools/acceptance_check.py
```
