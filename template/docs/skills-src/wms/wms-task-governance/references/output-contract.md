# Output Contract

## 必须落盘的产物

| 产物 | 位置 |
|---|---|
| 任务主记录 | `docs/tasks/{年份}/{MM}-{任务名}/README.md` |
| 对话记录 | `ai-conversations/{序号}-{主题}.md` |
| 业务沉淀 | `business-insights.md` |
| 制品说明 | `artifacts/` |
| 长期知识 | `docs/knowledge-base/`（按需） |

## 推荐启动产物

- 默认生成：
  - `ai-conversations/01-任务启动.md` 或 `01-初步分析.md`
- 按需生成：
  - `artifacts/plan-gate.md`
  - `artifacts/link-trace.md`
  - `artifacts/eval-plan.md`
  - `artifacts/eval-report.md`

## README 最低要求

- 任务背景或问题概述
- 当前状态
- 本轮分析/方案/结果
- 若有代码改动，补 GitNexus 影响摘要
- 若有代码 / SQL / 配置改动，补评测门禁结论
- 末尾完成标记

## 完成标记格式

```text
任务处理结果: {结果摘要}

----{YY}年{M}月{D}日 {HH}:{mm}:{ss} 第{x}次提交已完成，提交人：{git username}----
```
