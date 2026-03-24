# Delegation Payload

当总控需要委派给 subagent 时，最少应携带以下载荷：

## 必填项

- 当前控制文档路径
- 当前轮次规划摘要
- 本轮目标
- 本轮非目标 / 禁止事项
- 完成标准
- 回写位置（README / artifacts / business-insights）

## 推荐模板

```markdown
## Delegation Payload
- 控制文档：
- 本轮规划：
- 本轮目标：
- 本轮不做什么：
- 完成标准：
- 回写位置：
```

## 原则

- subagent 拿到的是受控任务，不是自由发挥任务
- 若控制文档发生新增补充，主控应先回查，再决定是否重发 payload
- 若平台不支持 subagent，此模板仍可作为“我准备怎么委派”的显式自检清单
