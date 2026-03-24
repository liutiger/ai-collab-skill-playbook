# WMS Skill Source

> 这是公开模板的 Skill 源码目录，也是当前模板 Prompt / Skill / Copilot 适配的唯一事实来源。

`docs/skills-src/` 是唯一 Source of Truth，但它不是治理总纲。治理关系固定为：

`AI协作研发章程 > AI协作试运行说明 > ai-workflow > docs/skills-src > .claude/skills/.github/prompts`

> 公开模板不包含 `docs/ai-runtime/` 这类维护者运行时目录；默认只演示纯 Skill / Copilot 路径。

## 当前默认架构

这套模板按 **双轴五构件** 组织：

### Governance Axis

- `charter`：总纲与边界
- `governance contract`：共享开始 / 结束合同

### Execution Axis

- `orchestrator`：单一总控 Skill
- `capability packs`：Scene / Strategy / Method / Gate / Policy
- `adapters & tools`：生成器、Copilot 适配和任务脚本

> `TDD / ACD / AOD` 属于 **Capability Packs 里的 Strategy Packs**，不是默认外显入口。

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
  "inventory-batch-rule"
```

脚本会自动初始化：

- `README.md`
- `business-insights.md`
- `ai-conversations/01-任务启动.md` 或 `01-初步分析.md`
- `artifacts/link-trace.md` / `artifacts/eval-plan.md` / `artifacts/eval-report.md`（按参数启用）
- 新任务的第 1 次 `规划任务:` 标记

默认不需要再手动拼 `plan-gate`/`auto-dev` 之类的阶段组合；日常由 `/wms-orchestrator` 自动判断当前三态和策略。

## Copilot 快速使用

生成 Copilot 运行产物后，可在 VS Code Copilot Chat 中直接使用：

- `/wms-orchestrator`
- `/wms-link-trace`
- `/wms-evaluation-gate`

使用建议：

- 日常默认先用 `/wms-orchestrator`
- 由 `/wms-orchestrator` 自动选择最合适的 Strategy Pack
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
