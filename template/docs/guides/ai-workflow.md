# 📖 AI 协作开发工作流指南

> 本指南定义了团队使用 AI 进行开发时的标准工作流程

## 核心理念

**每一次 AI 对话都是知识资产**。我们需要：
1. **记录** — 保留 AI 对话的关键内容
2. **沉淀** — 从对话中提取业务知识
3. **复用** — 让团队成员能从历史对话中受益

补充总纲文档：

- 试运行最小上手路径：`docs/guides/AI协作试运行说明.md`
- 协作原则与边界：`docs/guides/AI协作研发章程.md`
- Prompt 向 Skill 演进方案：`docs/guides/AI协作提示词Skill化方案.md`
- Skill 源码与生成规范：`docs/skills-src/README.md`
- GitHub Copilot 运行入口：`.github/copilot-instructions.md`、`.github/prompts/`

## 先看哪里

如果你是第一批试运行同学，不要从 Skill 源码开始看。

推荐阅读顺序：

1. `docs/guides/AI协作试运行说明.md`
2. `docs/guides/AI协作研发章程.md`
3. 本文档

如果你只是日常使用 GitHub Copilot Chat，优先使用 `.github/prompts/` 下的 slash prompt；`docs/skills-src/` 是维护者视角的实现目录。

## 工作流程

### 阶段一：任务初始化

```bash
./docs/skills-src/wms/wms-task-governance/scripts/create_task_dir.sh \
  --owner "{姓名}" \
  --module "{模块}" \
  --plan-gate \
  --evaluation-gate \
  "{任务名}"
```

填写 README.md 中的背景、目标、范围。若本轮没有代码 / SQL / 配置改动，可去掉 `--evaluation-gate`。

### 阶段二：AI 协作开发

每轮有价值的 AI 对话后：

1. **创建对话记录**
   - 优先在任务目录现有模板基础上续写
   - 如需新增记录，再从 `docs/tasks/_templates/AI_CONVERSATION.md` 复制

2. **记录关键内容**（不需要逐字记录，重点是）
   - 提了什么问题
   - AI 给了什么关键分析
   - 最终采纳了什么方案
   - 发现了什么之前不知道的知识

3. **保存产出物**
   - 代码变更的 diff 或说明 → `artifacts/`
   - SQL 变更 → `artifacts/`
   - 配置变更 → `artifacts/`

### 阶段二点五：评测与验收门禁

如果本轮涉及代码 / SQL / 配置改动，不要直接结束，先进入评测门禁：

1. 生成 `artifacts/eval-plan.md`
2. 生成 `artifacts/eval-report.md`
3. 至少覆盖编译门禁和测试门禁
4. 明确 `PASS / CONDITIONAL_PASS / BLOCKED / FAIL`
5. 只有门禁允许完成后，才进入最终完成标记

### 阶段三：业务沉淀

任务完成（或阶段性完成）时：

1. **更新 `business-insights.md`**
   - 提炼知识点
   - 记录经验教训
   - 标注哪些知识需要沉淀到 knowledge-base

2. **同步到 knowledge-base**
   - 成熟的业务知识 → `knowledge-base/business-flows/{模块}/`
   - 架构知识 → `knowledge-base/architecture/`
   - 接口知识 → `knowledge-base/api/`

3. **更新任务状态**
   - 更新 `README.md` 状态为已完成
   - 更新 `tasks/README.md` 任务索引

## AI 提示词体系

提示词分为**三层**，每次对话叠加使用：

### Layer 1 — 全局上下文（自动注入，无需操作）

按工具不同，通常由 `AGENTS.md` 或 `.github/copilot-instructions.md` 自动注入，包含：
- 项目基础上下文（模块定位、架构约定）
- 核心反模式（禁止事项）
- 数据流向

### Layer 2 — 研发部门规范（每次对话必须引用）

`#file:docs/prompts/00-department-standards.md`

每次对话**必须带上**，包含：
- 任务开始前 curl wiki 获取最新开发规范
- 代码理解与修改优先走 GitNexus，不先全项目搜索
- 新对话检查文档中“第x次提交已完成”分割线，继续处理未完成项
- 任务完成后在文档末尾写入完成标记（`----26年X月X日 HH:mm:ss 第x次提交已完成，提交人：xxx----`）
- 文档写入前的三步检查规则

### Layer 3 — 任务专属提示词（按任务类型选一个）

| 任务类型 | 引用命令 |
|---------|---------|
| 场景路由入口 | `#file:docs/prompts/11-scene-router.md` |
| 新功能开发检查包 | `#file:docs/prompts/01-feature-dev.md` |
| 线上问题排查检查包 | `#file:docs/prompts/02-issue-investigation.md` |
| 代码审查检查包 | `#file:docs/prompts/03-code-review.md` |
| 数据库变更检查包 | `#file:docs/prompts/04-database-change.md` |
| 重构优化检查包 | `#file:docs/prompts/05-refactoring.md` |
| 文档编写检查包 | `#file:docs/prompts/06-documentation.md` |
| 多角色自动开发编排 | `#file:docs/prompts/07-auto-dev-orchestration.md` |
| 链路确认 / 知识沉淀 | `#file:docs/prompts/08-link-confirmation.md` |
| 方案核对 / 实施前确认 | `#file:docs/prompts/09-plan-gate.md` |
| 自动评测 / 交付验收 | `#file:docs/prompts/10-evaluation-gate.md` |

> `11` 先负责场景路由；`01~06` 已瘦身为场景检查包；`07` 用于把分析、实现、验证、落盘进一步收紧成完整闭环；`09` 用于在实施前增加方案确认关卡；`10` 用于把“建议怎么测”升级为“实际交付门禁”。

### Skill 层 — 权威工作方法

Skill 体系是 Prompt 兼容层之上的权威工作方法：

- 源码：`docs/skills-src/`
- 运行产物：`.claude/skills/wms/`
- Copilot 运行产物：`.github/copilot-instructions.md`、`.github/instructions/`、`.github/prompts/`
- Prompt：兼容入口，负责任务入口和场景切换

请按下面的方式理解：

- `AI协作研发章程 = 总纲`
- `AI 工作流 = 章程落地流程`
- `Prompt = 入口`
- `Skill = 工作法`
- `Copilot slash prompt = GitHub Copilot 的直接触发入口`

不要把 Copilot slash prompt 或某个 Prompt 误认为总规则；它们只是工具入口，仍受《AI协作研发章程》约束。

### GitNexus 优先策略

涉及代码理解、调用链分析、影响评估时，固定顺序为：

1. `npx gitnexus status`
2. `npx gitnexus query "<业务词/异常/接口名>"`
3. `npx gitnexus context "<候选符号>"`
4. 修改公共符号前：`npx gitnexus impact "<符号名>"`
5. GitNexus 无法覆盖时，再用 `rg` 或 IDE 搜索补充

> 目标不是禁用搜索，而是先用知识图谱缩小范围，避免一上来全项目扫。

### 每次对话的标准开场格式

```
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/11-scene-router.md

[任务描述]
```

复杂任务推荐：

```
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/11-scene-router.md
#file:docs/prompts/07-auto-dev-orchestration.md
#file:docs/prompts/01-feature-dev.md

[任务描述]
```

> 标准模式只换第二行；自动开发模式增加 `07` 作为编排层。详见 `docs/prompts/README.md`

需要先核对目标、上下文和实施方案时，推荐：

```
#file:docs/prompts/00-department-standards.md
#file:docs/prompts/11-scene-router.md
#file:docs/prompts/09-plan-gate.md
#file:docs/prompts/01-feature-dev.md

[任务描述]
```

当你需要理解“为什么要这样设计 Prompt / Skill / 文档闭环”时，优先阅读：

- `docs/guides/AI协作研发章程.md`
- `docs/guides/AI协作提示词Skill化方案.md`

### GitHub Copilot Chat 直接用法

如果你在 VS Code 中使用 GitHub Copilot Chat，可直接使用：

- `/wms-scene-router`
- `/wms-plan-gate`
- `/wms-auto-dev`
- `/wms-evaluation-gate`
- `/wms-link-trace`

这些 slash prompt 由 `docs/skills-src/` 自动生成到 `.github/prompts/`。

使用建议：

- 先用 `/wms-scene-router` 分场景，再进入阶段入口
- 场景不清、跨场景或高风险任务，先用 `/wms-plan-gate`
- 只有满足章程中的人工确认要求后，再进入 `/wms-auto-dev`
- 涉及代码 / SQL / 配置改动时，完成前补用 `/wms-evaluation-gate`

## Skill 生成与验收

每次修改 Skill 源码后，固定执行：

```bash
python3 docs/skills-src/tools/validate_skills.py
python3 docs/skills-src/tools/validate_copilot_assets.py
python3 docs/skills-src/tools/generate_claude_skills.py --check
python3 docs/skills-src/tools/generate_claude_skills.py
python3 docs/skills-src/tools/generate_copilot_assets.py --check
python3 docs/skills-src/tools/generate_copilot_assets.py
python3 docs/skills-src/tools/generate_claude_skills.py --check
python3 docs/skills-src/tools/generate_copilot_assets.py --check
python3 docs/skills-src/tools/acceptance_check.py
```

通过标准：

- 所有命令退出码为 `0`
- 第二次 `--check` 不再报未同步
- `.claude/skills/wms/` 与 `docs/skills-src/` 保持一致
- `.github/copilot-instructions.md`、`.github/instructions/`、`.github/prompts/` 与 `docs/skills-src/` 保持一致

## AGENTS.md 的维护

当任务沉淀出重要的项目级知识时，应同步更新 `AGENTS.md`：

- 新模块/新架构 → 更新 STRUCTURE 和 WHERE TO LOOK
- 新的开发规范 → 更新 CONVENTIONS
- 新的反模式 → 更新 ANTI-PATTERNS
- 新的技术栈 → 更新 TECH STACK

## 目录规范

```
tasks/{年份}/{MM}-{任务名}/              ← 功能开发
tasks/{年份}/{MM}-[ISSUE]-{问题简描}/   ← 线上问题排查
├── README.md                  任务/问题卡片 (必须)
├── ai-conversations/          AI 对话记录
│   ├── 01-需求分析.md          功能开发: 需求分析
│   ├── 01-初步分析.md          问题排查: 根据日志初步定位
│   ├── 02-根因定位.md          问题排查: 深入代码分析
│   └── 03-修复方案.md
├── business-insights.md       业务沉淀 (必须)
└── artifacts/                 产出物 (按需)
    ├── fix-changes.diff        代码变更
    ├── data-fix.sql            数据修复 SQL
    ├── eval-plan.md            评测计划
    ├── eval-report.md          评测结论
    └── ...
```

## 线上问题排查工作流

问题发生时快速建立排查记录：

```bash
./docs/skills-src/wms/wms-task-governance/scripts/create_task_dir.sh \
  --issue \
  --owner "{姓名}" \
  --module "{模块}" \
  --link-trace \
  --evaluation-gate \
  "{问题简描}"
```

排查过程中同步记录：
1. **立即填写** — 问题现象、影响范围、时间线
2. **AI辅助分析** — 贴日志/代码让 AI 协助定位，记录到 `ai-conversations/`
3. **修复完成** — 更新根因、临时止损、根本修复
4. **复盘沉淀** — 填写经验教训，提炼到 `business-insights.md`

> 排查中的 AI 对话尤为宝贵，同类问题再次出现时直接查历史记录
