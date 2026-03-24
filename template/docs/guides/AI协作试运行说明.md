# AI 协作试运行说明

> 版本：v3.0
> 适用对象：直接在 VS Code + GitHub Copilot Chat 里使用公开模板的研发同学

## 1. 先记住 4 条规则

### 规则一：默认只用一个入口

绝大多数任务先用：

- `/wms-orchestrator`

它会在同一线程里自动做这几件事：

- 先走共享治理骨架
- 自动判主场景
- 自动选策略（TDD / ACD / AOD）
- 自动推进到 `DISCOVER / DELIVER / VERIFY`
- 必要时自动叠加专项方法

### 规则二：确认时直接在同一线程回复

如果 AI 提出了待确认点，不要重新换 prompt，也不用自己再组织一轮完整上下文。

### 规则三：涉及代码 / SQL / 配置改动，收尾前必须补评测门禁

- `/wms-evaluation-gate`

## 2. 最小使用路径

### 第一步：先建任务目录

```bash
./docs/skills-src/wms/wms-task-governance/scripts/create_task_dir.sh \
  --owner "{你的名字}" \
  --module "{模块名}" \
  "{任务名}"
```

如果你已经明确这轮只做链路确认或要预创建评测产物，再按需追加：

- `--link-trace`
- `--evaluation-gate`

### 第二步：默认入口

推荐优先级：

1. 日常默认总控：`/wms-orchestrator`
2. 只做链路确认：`/wms-link-trace`
3. 改动已存在，要决定能不能完成：`/wms-evaluation-gate`

### 第三步：把任务说清楚

```text
/wms-orchestrator

目标：新增库存批量操作类型能力
范围：example-service、同步链路
验收：能新增类型且不影响现有库存扣减
限制：请按总控先判主场景、策略和当前三态，高风险先停在 DISCOVER，不要直接写代码
```

### 第四步：待确认时不要换入口

直接在当前线程回复确认项，例如：

```text
确认：
1. 采用最小改动方案
2. 这轮不改公共接口
3. 可以继续实现
```

### 第五步：代码改完后补评测门禁

如果本轮有代码 / SQL / 配置改动，再进入：

- `/wms-evaluation-gate`

## 3. 一句话记忆

**默认先走 `/wms-orchestrator`，让总控自动判场景、选策略并推进 `DISCOVER / DELIVER / VERIFY`；确认时直接在同一线程回复，改动收尾前补 `/wms-evaluation-gate`。**
