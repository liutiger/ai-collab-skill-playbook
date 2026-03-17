# WMS Skill Source

> 这是公开仓库里的示例 Skill 源码包，保留了一个 WMS 风格命名空间，便于展示复杂业务项目的组织方式。

`docs/skills-src/` 是 `example-wms-project` 的 Skill 源码目录，也是唯一 Source of Truth。

但它不是治理总纲。治理关系固定为：

`AI协作研发章程 > AI协作试运行说明 > ai-workflow > docs/skills-src > .claude/skills/.github/prompts`

## 目录约定

```text
docs/skills-src/
├── manifest.yaml                 # Skill 清单与映射关系
├── tools/                        # 生成、校验、验收脚本
└── wms/                          # WMS 项目技能源码
```

运行产物固定生成到：

```text
.claude/skills/wms/
.github/copilot-instructions.md
.github/instructions/
.github/prompts/
```

## 运行时分层

这套模板现在明确区分两类 Skill：

- 主动运行 Skill：会生成到 `.claude/skills/wms/`，允许运行时自动触发
- 被动检查包：保留在 `docs/skills-src/`，用于手工引用、Prompt 兼容层、Copilot slash prompt 或维护时查阅

当前默认只保留以下主动运行 Skill：

- `plan-gate`
- `auto-dev-orchestrator`
- `delivery-evaluation-gate`
- `link-trace-and-curation`

以下内容不再作为主动运行 Skill 自动触发：

- `wms-task-governance`
- `gitnexus-code-navigation`
- `01~06` 对应场景 Skill

## 工作规则

- 只编辑 `docs/skills-src/`，不要直接手改 `.claude/skills/wms/`
- Copilot 运行产物也由 `docs/skills-src/` 生成，不要直接手改 `.github/copilot-instructions.md`、`.github/instructions/`、`.github/prompts/`
- `docs/prompts/00~10` 保留为兼容入口，不再作为唯一事实来源
- Core Skill 负责稳定工作方法，Scene Skill 只保留场景专项检查点
- 若 Skill / Copilot 适配与 `docs/guides/AI协作研发章程.md` 冲突，以章程为准

## 防串扰规则

- 默认只允许一个主导 Skill 自动触发，其他 Skill 尽量作为伴随 Skill
- 主动运行 Skill 的总数默认不应超过 5 个
- Scene Skill 的 frontmatter description 必须同时写清楚：
  - `Use only when`
  - `Not for`
- Scene Skill 默认只作为被动检查包保留在源码层，不进入 `.claude/skills/`
- 阶段型 Skill 必须写前后边界，例如：
  - `plan-gate` 只在实现前触发
  - `auto-dev-orchestrator` 只在方案确认后触发
  - `delivery-evaluation-gate` 只在改动已存在后触发
- 详细说明见 `docs/guides/skill-trigger-hygiene.md`

## 快速启动

任务目录初始化优先使用：

```bash
docs/skills-src/wms/wms-task-governance/scripts/create_task_dir.sh \
  --owner "your-name" \
  --module "example-service" \
  --plan-gate \
  --evaluation-gate \
  --link-trace \
  "inventory-batch-rule"
```

脚本会自动初始化：

- `README.md`
- `business-insights.md`
- `ai-conversations/01-任务启动.md` 或 `01-初步分析.md`
- `artifacts/plan-gate.md` / `artifacts/link-trace.md`（按参数启用）

## Copilot 快速使用

生成 Copilot 运行产物后，可在 VS Code Copilot Chat 中直接使用：

- `/wms-plan-gate`
- `/wms-feature-plan`
- `/wms-auto-dev`
- `/wms-feature-dev`
- `/wms-evaluation-gate`
- `/wms-issue-investigation`
- `/wms-code-review`
- `/wms-database-change`
- `/wms-refactoring`
- `/wms-documentation`
- `/wms-link-trace`

使用建议：

- 场景明确时，优先用对应场景型 slash prompt
- 场景不清或跨场景时，优先用 `/wms-plan-gate`
- 只有已满足章程中的人工确认要求后，再进入 `/wms-auto-dev`
- 涉及代码 / SQL / 配置改动时，完成前补用 `/wms-evaluation-gate`

## 第一版试运行默认策略

如果你是在给团队做第一版试运行，不要把 `docs/skills-src/` 当成一线同学的上手入口。

默认分层如下：

- 同事日常使用：先看 `docs/guides/AI协作试运行说明.md`
- 需要理解完整流程：再看 `docs/guides/ai-workflow.md`
- 维护 Prompt / Skill / Copilot 适配：再回到 `docs/skills-src/`

第一版最重要的不是“自动触发多聪明”，而是以下 3 件事稳定：

- 不清楚时先走 `/wms-plan-gate`
- 确认后再进入 `/wms-auto-dev` 或具体场景 prompt
- 代码改完后补跑 `/wms-evaluation-gate`
- 关键结论沉淀到 `docs/tasks/`

## 常用命令

```bash
python3 docs/skills-src/tools/validate_skills.py
python3 docs/skills-src/tools/validate_copilot_assets.py
python3 docs/skills-src/tools/generate_claude_skills.py --check
python3 docs/skills-src/tools/generate_claude_skills.py
python3 docs/skills-src/tools/generate_copilot_assets.py --check
python3 docs/skills-src/tools/generate_copilot_assets.py
python3 docs/skills-src/tools/acceptance_check.py
```

验收记录建议写入：

- `docs/reports/ai-skills/`

人工验收样例见：

- `docs/skills-src/acceptance-fixtures/`

## 核心约束

- 所有 Skill 目录必须包含 `SKILL.md`
- `SKILL.md` 必须包含 `name` 和 `description` frontmatter
- 场景薄 Skill 必须显式引用 Core Skill，不允许重复承载完整核心流程
- 新增或修改 Skill 后，必须重新执行校验、生成和验收
