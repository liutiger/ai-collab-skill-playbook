# Workflow

## 启动

1. 获取最新规范
2. 如涉及代码，先确认 GitNexus 是否可用
3. 检查是否已有任务目录
4. 若无任务目录，优先使用 `scripts/create_task_dir.sh`
5. 需要方案确认时，加 `--plan-gate`
6. 需要链路沉淀时，加 `--link-trace`
7. 需要交付评测门禁时，加 `--evaluation-gate`
8. 启动后至少应具备：
   - `README.md`
   - `business-insights.md`
   - `ai-conversations/01-任务启动.md` 或 `01-初步分析.md`
   - `artifacts/plan-gate.md` / `artifacts/link-trace.md` / `artifacts/eval-plan.md` / `artifacts/eval-report.md`（如适用）

## 续做

1. 先找 `第x次提交已完成` 分割线
2. 已完成分割线之前的内容只按需复查
3. 分割线之后的 `TODO`、`【待处理】`、`- [ ]` 纳入本轮计划

## 结束

1. 写入对话记录
2. 写入 `business-insights.md`
3. 写入 `artifacts/`
4. 如有复用价值，追加到 `knowledge-base/`
5. 涉及代码 / SQL / 配置改动时，先确认 `eval-report` 允许完成
6. 最后追加完成标记
