# AI 协作提示词 Skill 化方案

> 版本：v1.0
> 目标：将现有 `docs/prompts/00~09` 从“可用的提示词体系”逐步演进为“可复用的 Skill 工作体系”

## 1. 文档定位

本文档回答的问题不是“某个 Prompt 怎么改”，而是：

1. 当前提示词体系为什么已经接近 Skill
2. 哪些内容应该继续保留为 Prompt
3. 哪些内容应该升级为 Skill
4. Skill 化后目录、职责、触发方式、脚本、落盘如何设计
5. 如何分阶段落地，而不是一次性重构整套体系

本文档是《AI 协作研发章程》的实施路线补充。

---

## 2. 现状判断

### 2.1 当前体系已经不是“几段提示词”

现有 `00~09` 已经包含了以下内容：

- 多角色分工
- 阶段输出协议
- GitNexus 导航顺序
- 任务目录与完成标记
- 场景切换
- 风险控制
- 文档沉淀

这说明当前体系本质上已经是一套工作方法，而不只是聊天提示。

### 2.2 当前体系的优势

- 能支撑复杂业务仓库的 AI 协作
- 能约束 AI 不随意跳过流程
- 能把任务过程沉淀到 `docs/`
- 能通过多场景区分不同类型任务

### 2.3 当前体系的瓶颈

- 共性规则分散在多个 Prompt 中，维护成本高
- Prompt 越来越多，边界容易模糊
- 同一套工作方法在多仓库复用时，迁移成本较高
- 稳定动作还停留在文本说明，没有充分脚本化
- “该做什么”和“怎么稳定地做”还没有彻底分层

---

## 3. Skill 化的目标

Skill 化不是为了追求形式升级，而是为了达成以下目标：

- 让通用工作方法从场景 Prompt 中抽离出来
- 让高频、脆弱、重复动作可以被稳定复用
- 让 Prompt 聚焦在“任务输入”和“场景切换”
- 让跨仓库迁移和版本管理更容易
- 让后续自动化和 Agent 编排有统一依托

---

## 4. 设计原则

### 4.1 Prompt 负责说清“这次做什么”

Prompt 应尽量聚焦：

- 本次任务目标
- 本次场景类型
- 本次验收标准
- 用户补充限制

### 4.2 Skill 负责说清“这类任务怎么稳定地做”

Skill 应承载：

- 稳定工作流程
- 工具使用协议
- 输出格式契约
- 必要脚本与模板
- 防跑偏规则

### 4.3 项目上下文仍留在 `AGENTS.md`

Skill 不应承担大量项目静态背景说明。  
项目架构、模块定位、反模式、技术栈等仍放在 `AGENTS.md`。

### 4.4 场景入口要变薄

未来的 `01~06` 不应继续膨胀成大型流程文档，而应更像：

- 场景入口
- 专项检查清单
- 产出物差异说明

---

## 5. 目标架构

Skill 化后的建议架构如下：

### Layer A: Project Context

- `AGENTS.md`
- `.github/copilot-instructions.md`

职责：

- 项目静态上下文
- 模块定位
- 架构约束
- 技术栈与反模式

### Layer B: Core Skills

职责：

- 承载通用工作方法
- 提供可复用流程和工具协议

### Layer C: Scene Prompts

职责：

- 说明这次是什么任务
- 触发相应 Skill
- 增加场景专项检查点

### Layer D: Scripts / Templates

职责：

- 脚本化稳定动作
- 提供模板化产出

### Layer E: Knowledge Sink

职责：

- 接收任务过程与结论
- 沉淀为长期知识资产

---

## 6. 核心 Skill 候选

### 6.1 `wms-task-governance`

来源：

- `00-department-standards.md`

职责：

- 任务初始化
- 任务目录创建
- 续做边界检查
- 完成标记写入
- 通用落盘规则

建议包含：

- `scripts/create_task_dir.sh`
- `scripts/append_completion_marker.py`
- `references/task-record-format.md`

### 6.2 `gitnexus-code-navigation`

来源：

- `00`
- `07`
- `08`
- `09`

职责：

- 统一 GitNexus 导航协议
- 定义 `query / context / impact / 回退` 的顺序
- 约束搜索退化行为

建议包含：

- `references/navigation-protocol.md`
- `references/anti-drift-search.md`
- `scripts/gitnexus_probe.sh`

### 6.3 `plan-gate`

来源：

- `09-plan-gate.md`

职责：

- 在实现前完成目标澄清、上下文定位、最小方案设计
- 卡住实施关口，等待人工确认

建议包含：

- `references/plan-output-contract.md`
- `assets/templates/plan-gate-template.md`

### 6.4 `auto-dev-orchestrator`

来源：

- `07-auto-dev-orchestration.md`

职责：

- 在确认后执行完整闭环
- 负责“分析 -> 实现 -> 自检 -> 落盘”

建议包含：

- `references/stage-output-contract.md`
- `references/review-checklist.md`

### 6.5 `link-trace-and-curation`

来源：

- `08-link-confirmation.md`

职责：

- 梳理真实链路
- 标记关键分支和副作用
- 沉淀到 docs

建议包含：

- `references/link-trace-format.md`
- `assets/templates/link-trace.md`

---

## 7. 哪些内容保留为 Prompt

以下内容适合继续保留为 Prompt，而不是 Skill：

- 当前任务描述
- 当前业务背景
- 当前范围和非目标
- 当前验收标准
- 当前用户补充要求
- 这次是新功能还是排障还是审查

也就是说：

- Prompt 负责“这次任务”
- Skill 负责“这类任务”

---

## 8. 哪些内容必须升级为 Skill

以下内容一旦反复出现，就不应继续散落在多个 Prompt 中：

- GitNexus 导航顺序
- 假设 -> 验证 -> 回退机制
- 阶段输出协议
- 高风险任务的方案确认关卡
- 文档落盘流程
- 完成标记规则
- 搜索退化防护规则

---

## 9. `00~09` 与 Skill 的映射建议

| 现有文件 | 当前职责 | 未来建议 |
|---|---|---|
| `00` | 部门规范、任务治理、落盘 | 升级为 `wms-task-governance` + 部分导航共性迁出 |
| `01` | 新功能开发场景 | 保留为薄场景 Prompt |
| `02` | 线上排障场景 | 保留为薄场景 Prompt |
| `03` | 代码审查场景 | 保留为薄场景 Prompt |
| `04` | 数据库变更场景 | 保留为薄场景 Prompt |
| `05` | 重构优化场景 | 保留为薄场景 Prompt |
| `06` | 文档编写场景 | 保留为薄场景 Prompt |
| `07` | 自动开发闭环 | 升级为 `auto-dev-orchestrator` |
| `08` | 链路确认和沉淀 | 升级为 `link-trace-and-curation` |
| `09` | 实施前方案核对 | 升级为 `plan-gate` |

---

## 10. 目录设计建议

建议把 Skill 的源码放在仓库中，便于版本化、代码审查和跨仓库复制：

```text
docs/skills-src/
├── wms-task-governance/
├── gitnexus-code-navigation/
├── plan-gate/
├── auto-dev-orchestrator/
└── link-trace-and-curation/
```

每个 Skill 目录建议结构：

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── output-contract.md
│   └── anti-patterns.md
├── scripts/
│   ├── stable-action-1.sh
│   └── stable-action-2.py
└── assets/
    └── templates/
```

---

## 11. 低成本落地顺序

不建议一次性把所有场景都 Skill 化。  
建议先做最能解决“腐化、跑偏、乱搜、跳过方案”的 3 个：

### Phase 1

- `gitnexus-code-navigation`
- `plan-gate`
- `auto-dev-orchestrator`

原因：

- 它们最直接决定 AI 是否稳定
- 它们能优先解决“搜索退化”和“直接越过方案阶段”的问题
- 这 3 个成功后，其他场景就能明显变薄

### Phase 2

- `wms-task-governance`
- `link-trace-and-curation`

原因：

- 它们决定闭环质量和知识沉淀质量
- 属于长期收益型能力

### Phase 3

- 视试运行结果，再决定 `01~06` 是否要进一步变成完整 Skill

---

## 12. 实施步骤

### Step 1: 盘点

对现有 `00~09` 做拆分标记：

- 哪些是项目上下文
- 哪些是通用流程
- 哪些是场景差异
- 哪些是稳定动作，适合脚本化

### Step 2: 抽共性

把 `00/07/08/09` 中重复出现的方法抽出来，形成核心 Skill 草案。

### Step 3: 建 Skill 骨架

先创建以下目录和空骨架：

- `docs/skills-src/gitnexus-code-navigation/`
- `docs/skills-src/plan-gate/`
- `docs/skills-src/auto-dev-orchestrator/`

### Step 4: 编写 `SKILL.md`

每个 Skill 的 `SKILL.md` 只写：

- 触发条件
- 工作目标
- 标准流程
- 边界
- 何时读 `references/`
- 何时调用 `scripts/`

### Step 5: 拆 `references/`

把大段格式、反模式、输出模板说明拆到 `references/`，避免 `SKILL.md` 过厚。

### Step 6: 脚本化稳定动作

优先脚本化这几类动作：

- 创建任务目录
- 初始化 README / business-insights
- 追加完成标记
- 生成 link trace 模板
- 执行 GitNexus 健康检查

### Step 7: 瘦身 `01~06`

把场景 Prompt 改成：

- 入口说明
- 场景特有关注点
- 产出物差异
- 场景专属完成检查

### Step 8: 试运行

至少用 3 类真实任务验证：

- 新功能开发
- 线上问题排查
- 链路确认

### Step 9: 评估

重点看以下指标：

- 是否减少大范围乱搜
- 是否更稳定停在方案确认阶段
- 是否更稳定完成文档沉淀
- 是否降低 Prompt 维护成本

---

## 13. 脚本化建议

以下动作建议优先落成脚本，而不是继续依赖 AI 即兴生成：

### 13.1 任务目录初始化

用途：

- 创建 `README.md`
- 创建 `business-insights.md`
- 创建 `ai-conversations/`
- 创建 `artifacts/`

### 13.2 完成标记追加

用途：

- 读取 `git user.name`
- 生成符合规范的完成标记
- 统一写入格式，避免手工漂移

### 13.3 Link Trace 模板生成

用途：

- 预生成 `artifacts/link-trace.md`
- 固定表头和关键字段

### 13.4 GitNexus 预检查

用途：

- 检查索引状态
- 未索引时提示 `analyze`
- 统一返回导航建议

---

## 14. 风险与取舍

### 14.1 不宜一次性做太重

如果一开始把所有 Prompt 都硬迁成 Skill，风险是：

- 体系过大
- 维护成本陡增
- 团队上手困难
- 新旧方式并存期会更混乱

### 14.2 不宜只做文本迁移

如果只是把 Prompt 原文复制进 Skill，而不抽职责、不拆 references、不补脚本，那只是“换壳”，不是 Skill 化。

### 14.3 不宜让 Skill 承担项目静态背景

项目上下文放太多进 Skill，会造成：

- Skill 触发成本高
- 复用性差
- 多仓库同步困难

---

## 15. 验收标准

Skill 化方案达成的标志包括：

- 共性方法从 `01~06` 中被明显抽离
- `01~06` 变薄但不失控
- AI 搜索退化行为显著减少
- 高风险任务能稳定停在方案关卡
- 任务沉淀更稳定、格式更统一
- 跨仓库迁移 Prompt 体系时，核心方法可以直接复用

---

## 16. 建议的近期行动

### 本周可做

1. 定稿本方案
2. 拆分 `00/07/08/09` 的共性内容
3. 先建 3 个 Skill 骨架

### 下周可做

1. 脚本化任务目录初始化和完成标记
2. 薄化 `01~06`
3. 用真实任务试跑

### 试运行后再决定

1. 是否继续把 `wms-task-governance` 和 `link-trace-and-curation` 做完整
2. 是否把 `01~06` 进一步变成完整 Skill
3. 是否进入自动化和定时任务层

---

## 17. 一句话总结

Skill 化不是把 Prompt 换个文件名，而是把本项目已经形成的 AI 协作工作方法，升级成：

**可安装、可触发、可复用、可演进、可审计的稳定能力单元。**
