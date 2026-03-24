# Shared Start Contract

每次进入活跃入口前，都先执行：

1. 读取最新团队规范源，例如：`curl "<your-latest-engineering-rules-url>"`
2. 回查任务目录与 `README.md` 是否已有新增补充要求
3. 写入新的 `规划任务:` 标记；若是补充需求，则写成 `第x次补充`
4. 如涉及 shell / 构建 / 测试命令，优先准备 `tmux`
5. 进入具体场景 / 阶段 / 方法前，先确认这轮边界与默认产物
