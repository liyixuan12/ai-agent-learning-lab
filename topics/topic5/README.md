# Topic 5 — Version Control & GitHub 实战

> 范围：本目录用于 Topic 5 的实操。目标是把你当前 `financial-ai-coding-study` 项目变成一个结构清晰、可复现、可展示的 GitHub 学习作品集。
>
> 重点不是“会敲命令”，而是建立一套你之后长期会复用的协作习惯：小步提交、清晰信息、分支开发、可读 README。

---

## 1. 学完这一节你应具备的能力

- 理解 Git 与 GitHub 的分工（本地版本管理 vs 远程协作与展示）。
- 能在本地初始化仓库并完成标准提交流程：`add -> commit -> log`。
- 能创建并切换分支，独立完成一个小功能后合并回主分支。
- 能将代码推送到 GitHub，并设置清晰的仓库首页说明。
- 能写出有“项目可读性”的 README（目标、结构、运行方式、截图、免责声明）。

---

## 2. 本节产出（完成后你会得到什么）

```text
1) 一个已初始化并有提交历史的本地 Git 仓库
2) 一个远程 GitHub 仓库（同名或你自定义名字）
3) 一份可用于求职展示的 README
4) 至少 8 条语义清晰的提交记录（覆盖 Topic 1~4 与 Topic 5）
```

---

## 3. 快速心智模型（先记住这张图）

```text
工作区(Working Directory)
        |
   git add
        v
暂存区(Staging Area)
        |
 git commit
        v
本地仓库(Local Repository)
        |
   git push
        v
远程仓库(Remote / GitHub)
```

一句话：`add` 是“选中要提交的改动”，`commit` 是“生成一次快照”，`push` 是“把快照同步到 GitHub”。

---

## 4. 实操步骤（按顺序执行）

> 以下命令均在仓库根目录执行：`financial-ai-coding-study/`

### 4.1 初始化与首个提交

```bash
git init
git status
git add .
git commit -m "Initialize Financial AI coding study workspace"
```

检查提交历史：

```bash
git log --oneline --decorate -n 5
```

### 4.2 配置主分支名称并连接远程

```bash
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

示例远程地址：

```text
https://github.com/<your-username>/financial-ai-coding-study.git
```

### 4.3 创建分支做一次独立改动

```bash
git checkout -b docs/topic5-readme-polish
```

在该分支上修改任意文档后提交：

```bash
git add .
git commit -m "Improve Topic 5 learning documentation"
git push -u origin docs/topic5-readme-polish
```

然后在 GitHub 发起 PR（Pull Request）并合并到 `main`。

---

## 5. 提交信息模板（可直接复用）

建议格式（英文祈使句）：

```text
<Type>: <What changed in one sentence>
```

常见 Type：

- `Add`：新增文件或功能
- `Update`：增强已有内容
- `Fix`：修复错误
- `Refactor`：重构（不改变外部行为）
- `Docs`：文档更新

示例：

```text
Add Topic 1 company risk analyzer notes
Update FastAPI endpoint docs and examples
Fix RAG demo argument parsing for dry-run mode
Docs: polish project README structure
```

---

## 6. README 最小模板（建议你在根目录 README 使用）

```markdown
# Financial AI Coding Study

## Project Goal
Build a practical portfolio from coding basics to a mini financial AI demo.

## Topics Covered
- Topic 1: Python basics
- Topic 2: FastAPI and architecture
- Topic 3: LLM and prompt engineering
- Topic 4: RAG basics
- Topic 5: Version control and GitHub workflow

## Project Structure
... (tree)

## Quick Start
1. Create virtual environment
2. Install dependencies
3. Run topic scripts

## Screenshots
... (optional)

## Disclaimer
This project is for educational purposes and is not financial advice.
```

---

## 7. 自测检查表

- [ ] 我能解释 `git add`、`git commit`、`git push` 的区别
- [ ] 我完成了至少 1 次分支开发并通过 PR 合并
- [ ] 我的提交信息可以让他人看懂“为什么改”
- [ ] 我的 GitHub 仓库首页能让陌生人 3 分钟内理解项目
- [ ] 我在 README 中包含了免责声明（非投资建议）

---

## 8. 今天就做（45~60 分钟）

1. `git init` 并做首个提交。  
2. 新建 GitHub 仓库并 `push` 到 `main`。  
3. 用分支 `docs/topic5-readme-polish` 改一处文档并提一个 PR。  
4. 在根目录 README 增加 “Project Goal / Structure / Disclaimer” 三节。  
5. 截图保存到 `screenshots/`（仓库首页 + 提交历史 + PR 页面）。

完成后你就达成 Topic 5 的最小闭环。

---

## 9. 反思模板

```text
What I learned:
我学到了：

What was difficult:
我觉得困难的是：

How this helps my job application:
这对我的求职有什么帮助：

Next improvement:
下一步改进：
```
