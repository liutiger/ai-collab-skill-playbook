# AI 协作开发工作流指南

> 本指南定义公开模板使用 AI 协作时的标准工作流程。

## 阅读顺序

1. `docs/guides/AI协作试运行说明.md`
2. `docs/guides/AI协作研发章程.md`
3. 本文档
4. `docs/prompts/README.md`
5. `docs/skills-src/README.md`

## 默认工作流

### 阶段一：任务初始化

```bash
./docs/skills-src/wms/wms-task-governance/scripts/create_task_dir.sh \
  --owner "{姓名}" \
  --module "{模块}" \
  --plan-gate \
  --evaluation-gate \
  "{任务名}"
```

### 阶段二：总控推进

默认先进入：

- `/wms-orchestrator`

总控会依次完成：

1. 先判场景
2. 再选执行模式（TDD / ACD / AOD）
3. 再决定当前阶段
4. 必要时叠加专项方法
5. 遇到 hard gate 时一次性汇总确认项

### 阶段三：专项方法与评测

- 链路确认：`/wms-link-trace`
- 交付评测：`/wms-evaluation-gate`

## 五层架构

1. `Governance`
2. `Orchestrator`
3. `Scene`
4. `Stage`
5. `Method`

> `TDD / ACD / AOD` 是 Orchestrator 之下的执行模式，不是第六层。
