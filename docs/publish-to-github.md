# Publish To GitHub

如果你准备把这个整理包独立发布成一个 GitHub 仓库，建议按下面顺序做。

## 1. 先定三个东西

- 仓库名
- License
- README 开头的一句话定位

建议仓库名风格：

- `ai-collab-skill-playbook`
- `prompt-to-skill-playbook`
- `ai-dev-governance-template`

## 2. 本地再检查一轮

```bash
cd ai-collab-skill-playbook/template

python3 docs/skills-src/tools/validate_skills.py
python3 docs/skills-src/tools/validate_copilot_assets.py
python3 docs/skills-src/tools/generate_claude_skills.py --check
python3 docs/skills-src/tools/generate_copilot_assets.py --check
python3 docs/skills-src/tools/acceptance_check.py
```

## 3. 初始化独立仓库

如果你打算把这个目录作为单独仓库：

```bash
cd /Users/xiaowang/Documents/Playground/ai-collab-skill-playbook
git init
git add .
git commit -m "chore: bootstrap public skill playbook"
```

如果你使用 GitHub CLI：

```bash
gh repo create <your-repo-name> --public --source=. --remote=origin --push
```

## 4. 发布说明里建议强调

- 这是一个“方法模板 + 示例包”
- `template/` 需要按接入方项目重写
- `AGENTS.md`、章程和 00 号 Prompt 一定要本地化
- `.github/` 和 `.claude/skills/` 由 `docs/skills-src/` 生成

## 5. 第一版不要追求完美

第一版公开最重要的是：

- 结构清楚
- 脱敏完成
- 能跑通生成和验收
- 别人 clone 后知道从哪里开始看
