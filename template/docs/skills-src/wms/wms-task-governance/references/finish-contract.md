# Shared Finish Contract

准备结束当前轮次前，都先执行：

1. 回查 `README.md` 与 `artifacts/` 是否存在新增补充要求或未落盘结论
2. 该沉淀的内容先写入 `docs/tasks/`、`artifacts/`、`business-insights.md`
3. 涉及代码 / SQL / 配置改动时，先经过评测门禁；未通过不得写完成标记
4. 显式询问用户：`本文档中的任务是否已经处理完毕`
5. 若当前平台不支持真正的确认框，则默认按“需要继续检查文档”处理
6. 若存在 hard gate，必须一次性汇总全部必须确认项；用户回复后沿当前线程继续
