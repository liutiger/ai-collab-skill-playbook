# 研发部门规范（每次对话必带）

> **Governance 兼容入口**。权威工作法以下列 Skill 为准：
> - `wms-task-governance`
> - `gitnexus-code-navigation`
>
> Source of Truth：`docs/skills-src/wms/`
> Runtime：`.claude/skills/wms/`

---

## ⚡ 任务启动（按序执行，不可跳过）

### STEP-1: 获取最新规范

收到用户消息后，**第一个工具调用**：

```bash
curl "<your-latest-engineering-rules-url>"
```

- 成功 → 读取内容作为执行约束，**wiki 内容优先级 > 本地提示词**
- 失败 → 告知用户"无法获取最新规范，基于本地规范执行"，**不阻塞，继续工作**

### STEP-1.5: GitNexus 就绪检查（涉及代码时必须）

涉及代码理解、定位、修改、评审时，默认优先级固定为：

`GitNexus > 局部 rg > 全项目搜索`

推荐顺序：

```bash
npx gitnexus status
npx gitnexus query "库存抵扣异常"
npx gitnexus context "StorehouseOutboundExecuteServiceImpl"
npx gitnexus impact "StorehouseOutboundExecuteServiceImpl.createOutboundOrder"
```

- 未索引或索引过期 → 执行 `npx gitnexus analyze`
- 先 `query` 找流程、模块、可疑符号，不要一上来全仓库搜索
- 找到候选符号后，用 `context` 看调用者、被调用者、参与流程
- 修改公共方法、核心类、接口定义前，用 `impact` 看影响范围
- 仅当 GitNexus 没结果，或需要补充精确文本匹配时，再用 `rg` / IDE 全局搜索
- 若当前工具支持 MCP，等价使用 `gitnexus_query` / `gitnexus_context` / `gitnexus_impact`

### STEP-2: 创建任务目录（在分析问题之前）

```
docs/tasks/{年份}/{MM}-{任务名}/          # 功能开发
docs/tasks/{年份}/{MM}-[ISSUE]-{简描}/    # 问题排查

{任务目录}/
├── README.md              ← 立即写入：需求/问题概述 + 规划标记
├── business-insights.md   ← 创建空文件
├── ai-conversations/      ← 创建目录
└── artifacts/             ← 创建目录
```

**规划标记**（紧接概述后写入 README.md）：

```
---- {YY}年{M}月{D}日 {HH}:{mm}:{ss}（取系统实时日期和时间） ，第{x}次提交（补充需求时标注：第{x}次补充） ，提交人：{git username} ，规划任务: {任务简述}
```

- `{git username}` 通过 `git config user.name` 获取

### STEP-3: 检查文档状态（仅续做任务需要，新任务跳过）

1. 找**包含** `第x次提交已完成` 的分割线（通常形如：`----xx年xx月xx日 xx:xx:xx 第x次提交已完成，提交人：xxx----`），分割线之前 = 已完成（按情况判断是否需要继续），之后 = 待处理
2. 新对话开始时：对“第x次提交已完成”之前内容按需复查；对“第x次提交已完成”之后内容按当前规则分析并完成
3. 检查 `【待处理】`/`TODO`/`- [ ]`/`【补充】`/`【更新】` 等标记，纳入当前计划
4. 无历史文档 = 直接通过

> **STEP-1~3（含 1.5）完成后，进入 Orchestrator / Scene / Stage / Method 对应入口。**

---

## ⚡ 任务完成协议（不执行 = 任务未完成）

> 以下步骤在任务结束前**必须全部执行**。"回答了用户问题"不等于"任务完成"。

### 一、落盘（自动执行，无需用户提示）

| # | 动作 | 路径 | 时机 |
|---|------|------|------|
| 1 | 对话记录 | `ai-conversations/{序号}-{主题}.md` | 产出了方案/分析/代码变更时（至少 1 个） |
| 2 | 业务知识 | `business-insights.md` | 任务完成后 |
| 3 | 评测计划/结论 | `artifacts/eval-plan.md`、`artifacts/eval-report.md` | 有代码 / SQL / 配置改动时 |
| 4 | 制品归档 | `artifacts/` | 有代码 diff / SQL / 设计方案时 |
| 5 | 知识库同步 | `knowledge-base/{子目录}/` | 有可复用的新业务认知时（追加，不覆盖） |
| 6 | 完成标记 | README.md 末尾 | **最后一步** |

涉及公共符号、核心链路、跨模块调用改动时，README.md 或 `artifacts/` 中需补一段 **GitNexus 影响分析摘要**：目标符号、主要调用方、风险级别、是否需要灰度。

若本次任务涉及代码 / SQL / 配置改动，则写完成标记前必须补齐：

- `artifacts/eval-plan.md`
- `artifacts/eval-report.md`

且 `eval-report` 必须明确：

- 已执行的门禁
- 门禁结论（PASS / CONDITIONAL_PASS / BLOCKED / FAIL）
- 是否允许写完成标记

**knowledge-base 写入方向**：

| 知识类型 | 路径 |
|---------|------|
| 业务流程/处理逻辑 | `knowledge-base/business-flows/{模块}/` |
| 架构/模式/机制 | `knowledge-base/architecture/` |
| REST/Feign 接口 | `knowledge-base/api/` |
| 表结构/字段/索引 | `knowledge-base/database/` |

### 二、完成标记（精确到秒，缺一不可）

在任务文档末尾追加：

```
任务处理结果: {结果摘要}

----{YY}年{M}月{D}日 {HH}:{mm}:{ss} 第{x}次提交已完成，提交人：{git username}----
```

**结果摘要参考**：

| 任务类型 | 格式 |
|---------|------|
| 功能开发 | 已完成 {功能名}，涉及 {N} 个文件，核心类 {ClassName} |
| 问题排查 | 根因：{描述}。排查依据：{位置}。修复：{方案} |
| 代码审查 | 发现 {N} 个阻断/{M} 个警告，集中在 {模块} |
| 数据库变更 | 执行 {DDL/DML}，影响 {N} 行，已在 {环境} 验证 |
| 重构优化 | 重构 {模块}，{问题}，代码行数 {X}→{Y} |
| 文档编写 | 创建/更新 {路径}，覆盖 {主题} |

> **错误** ❌：`----26年3月3日 已完成----`（缺提交序号/时间/提交人）
> **正确** ✅：`----26年3月3日 14:22:35 第2次提交已完成，提交人：your-name----`

### 三、写入前循环检查（完成标记写入前必须执行）

完成每个任务和本文档写入前，**先检查本文档是否存在更新任务或者补充要求**：

0. 如本次任务涉及代码/文档/配置/流程图/接口/DDL 等变更，先对照根目录 `project-rules.md` 做联动检查（README、`*.puml`、配置、接口契约、SQL、报告索引等），确保无遗漏同步文件

1. 重新阅读任务文档（README.md / 用户消息），查找是否有新增的 `【待处理】`/`TODO`/`- [ ]`/`【补充】`/`【更新】` 等标记
2. 如果存在更新或补充要求 → 继续规划任务完成，**不写入完成标记**
3. 若存在代码 / SQL / 配置改动但无 `eval-report`，或 `eval-report` 结论为 `BLOCKED / FAIL` → **不写入完成标记**
4. 完成补充任务后，再重新执行本条规则（循环检查，直到无新增要求）
5. 确认无新增要求且评测门禁允许完成后 → 写入完成标记

> **此规则形成闭环**：每次准备写入完成标记前都必须回查，防止遗漏后续追加的需求。
> **固定规则**：`--- 以上为固定规则，每次执行任务必须遵守 ----`

---

## 📐 通用文件格式（所有场景共用，写一次记一次）

### business-insights.md

```markdown
## 任务来源
| 字段 | 内容 |
|---|---|
| **任务** | {名称} |
| **日期** | {YYYY-MM-DD} |

## 业务知识沉淀

### 1. {知识点标题}
**分类**: 架构 / 业务流程 / 数据模型 / 接口契约 / 性能优化 / 故障处理
**内容**: {详细描述}
**相关代码**: `ClassName.method()`
**影响范围**: {模块/接口}

---
### 2. ...

## 经验教训
| 类别 | 内容 | 建议 |
|---|---|---|
| 🟢 做得好 | {做法} | {推广建议} |
| 🔴 踩的坑 | {问题} | {规避方法} |

## 待沉淀到知识库
- [ ] → `knowledge-base/{path}`: {知识点}
```

### ai-conversations/{序号}-{主题}.md

```markdown
## 对话信息
| 字段 | 内容 |
|---|---|
| **任务** | {关联任务名} |
| **轮次** | 第{N}轮 |
| **日期** | {YYYY-MM-DD} |
| **AI工具** | GitHub Copilot / Claude / Cursor |
| **目的** | {本次解决什么问题} |

## 关键输入
{背景信息、代码上下文、错误日志}

## 对话摘要
### {问题1}
**提问要点** → **AI分析** → **结论/方案**

## 产出
- {变更描述} → `文件路径`

## 关键发现
1. {发现}

## 反思
{本次AI协作中什么有效？什么可改进？提示词如何更好？}
```

---

## 五层关系中的定位

| 维度 | 控制方 |
|------|--------|
| curl 规则源 + GitNexus 优先定位 + 任务目录 + 完成标记 + 通用落盘 + 通用文件格式 | **Governance（本文件）** |
| 主场景专项检查清单 | **Scene** |
| 方案 / 实现 / 评测推进 | **Stage** |
| 链路确认等专项协议 | **Method** |

- `Governance` 与 `15-governance-lifecycle-contract.md` 一起提供共享硬边界
- `Scene / Stage / Method` 在其之上叠加，不替代本文件
