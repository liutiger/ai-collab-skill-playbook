# Public Sharing Checklist

在把这套体系发到 GitHub 之前，建议至少检查下面这些项。

## 必查项

- [ ] 内网链接已替换成占位符或公开文档
- [ ] 私有仓库名、真实模块名、内部系统缩写已脱敏或泛化
- [ ] 个人用户名、绝对路径、本机命令历史已替换
- [ ] Token、密码、内网地址、Sonar 凭据等敏感信息不存在
- [ ] 任务示例、验收样例不包含真实业务单号、客户名、环境信息

## 方法层检查

- [ ] 章程、工作流、Skill、Prompt、Copilot 入口的层级关系写清楚
- [ ] 说明了为什么需要 `plan-gate`
- [ ] 说明了为什么需要 `evaluation-gate`
- [ ] 说明了为什么需要 `docs/tasks/` 和 `knowledge-base/`
- [ ] 说明了 GitNexus 优先导航的目的，不只是工具偏好

## 模板可用性检查

- [ ] `template/AGENTS.md` 已提示使用者必须重写项目上下文
- [ ] `template/docs/prompts/00-department-standards.md` 已改成占位式规范来源
- [ ] `template/docs/tasks/_templates/` 完整
- [ ] `template/docs/skills-src/tools/` 可运行
- [ ] `template/.github/` 和 `template/.claude/skills/` 可重新生成

## 发布前最后一轮自测

在 `template/` 目录下执行：

```bash
python3 docs/skills-src/tools/validate_skills.py
python3 docs/skills-src/tools/validate_copilot_assets.py
python3 docs/skills-src/tools/generate_claude_skills.py
python3 docs/skills-src/tools/generate_copilot_assets.py
python3 docs/skills-src/tools/acceptance_check.py
```

## 建议额外补的 GitHub 元信息

- 项目 License
- 一份简短的贡献说明
- 一张体系结构图
- 一组“先方案、后实现、再验收”的截图或对话样例
