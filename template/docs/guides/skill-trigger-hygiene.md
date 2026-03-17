# Skill Trigger Hygiene

这个文档专门解决一个常见问题：

**Skill 集成到 VS Code 后，聊天过程中很容易多个 Skill 同时触发，彼此抢活、重复输出、互相打断。**

## 1. 为什么会发生

最常见的根因不是“模型太笨”，而是 Skill 元数据写得太宽：

- 描述词太泛，多个 Skill 都像是在说“我也能做”
- 场景 Skill 和核心 Skill 都试图做主导
- 阶段边界不清，计划、实现、验收都在抢同一条输入
- Scene Skill 没写排除条件，只写了“什么时候能用”

## 2. 设计原则

### 原则一：一个请求只该有一个主导 Skill

默认应该是：

- 一个主导 Skill
- 零到两个伴随 Skill

如果一个输入同时能触发 4 个以上 Skill，基本就说明描述太宽了。

### 原则二：Scene Skill 必须写正向触发词和排除词

坏例子：

- `Use when a task is feature development`

好例子：

- `Use only when the task is approved feature implementation... Not for early planning, incident investigation, code review...`

也就是：

- 既要说“什么时候该触发”
- 也要说“什么时候不要触发”

### 原则三：阶段型 Skill 必须写前后边界

例如：

- `plan-gate` 只能在实现前触发
- `auto-dev-orchestrator` 只能在方案已确认后触发
- `delivery-evaluation-gate` 只能在改动已存在后触发

如果不写这些边界，模型就会在任意阶段把它们都拉进来。

### 原则四：导航型 Skill 更适合作为伴随 Skill

像 `gitnexus-code-navigation` 这种 Skill，应该更多承担：

- 代码定位
- 调用链导航
- 影响面分析

而不是抢“主任务身份”。

## 3. 这套模板里的约束

从当前版本开始，Scene Skill 的描述必须显式包含：

- `Use only when`
- `Not for`

校验器会检查这两点，防止后面又慢慢腐化。

另外，这套模板还做了一个更根本的收敛：

- 主动运行 Skill 只保留少数几个阶段型 Skill
- 场景 Skill 降级为源码层的被动检查包，不再默认进入 `.claude/skills/`

也就是把“阶段”与“场景”拆开：

- 阶段：谁来主导这轮工作
- 场景：这一轮需要补什么专项检查点

这样能大幅减少多个 Skill 同时抢入口。

## 4. VS Code 实操建议

### 推荐输入方式

- 先明确阶段：`先做方案` / `现在开始实现` / `现在做验收`
- 再明确场景：`这是 Code Review` / `这是问题排查` / `这是链路确认`

例如：

- `先做方案，不要实现，这是跨模块新功能`
- `方案已确认，现在进入实现闭环`
- `代码已改完，现在只做 evaluation gate`

### 不推荐输入方式

- `你帮我全都做了`
- `顺便看一下有没有问题`
- `帮我分析下然后改一下再测一下`

这类输入会让多个 Skill 都觉得“像是自己该上”。

## 5. 维护建议

每次新增 Skill 时，至少检查这 4 件事：

1. 它是不是主导 Skill 还是伴随 Skill
2. 它的 description 有没有写 `Use only when`
3. 它的 description 有没有写 `Not for`
4. 它会不会和现有 Skill 抢同一类请求

如果会，就先收窄，而不是继续加说明文档。
