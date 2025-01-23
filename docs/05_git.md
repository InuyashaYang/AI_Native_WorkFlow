

1. **最小可使用的指令集**
2. **进阶指令集和详细指令列表**

---

## 1. 最小可使用的指令集

对于刚接触 Git 的用户，掌握以下基本指令即可进行基本的版本控制操作：

### 初始化仓库

- **`git init`**

  创建一个新的 Git 仓库。

  ```bash
  git init
  ```

### 克隆仓库

- **`git clone <repository>`**

  从远程仓库克隆一个本地副本。

  ```bash
  git clone https://github.com/username/repository.git
  ```

### 查看状态

- **`git status`**

  查看当前工作区和暂存区的状态。

  ```bash
  git status
  ```

### 添加更改

- **`git add <file>`**

  将指定文件的更改添加到暂存区。

  ```bash
  git add README.md
  ```

- **`git add .`**

  将当前目录下的所有更改添加到暂存区。

  ```bash
  git add .
  ```

### 提交更改

- **`git commit -m "提交说明"`**

  提交暂存区的更改，并添加提交说明。

  ```bash
  git commit -m "初始化项目结构"
  ```

### 查看提交历史

- **`git log`**

  显示提交历史记录。

  ```bash
  git log
  ```

### 推送更改

- **`git push`**

  将本地提交推送到远程仓库。

  ```bash
  git push origin main
  ```

### 拉取更改

- **`git pull`**

  从远程仓库拉取并合并更改到本地。

  ```bash
  git pull origin main
  ```

---

## 2. 进阶指令集和详细指令列表

掌握基本指令后，以下进阶指令能提升你的 Git 使用效率和管理能力：

### 分支管理

- **创建分支**

  ```bash
  git branch <branch-name>
  ```

- **切换分支**

  ```bash
  git checkout <branch-name>
  ```

  或使用新命令：

  ```bash
  git switch <branch-name>
  ```

- **创建并切换到新分支**

  ```bash
  git checkout -b <branch-name>
  ```

  或使用新命令：

  ```bash
  git switch -c <branch-name>
  ```

- **删除分支**

  ```bash
  git branch -d <branch-name>
  ```

### 合并与重放

- **合并分支**

  ```bash
  git merge <branch-name>
  ```

- **变基**

  ```bash
  git rebase <base-branch>
  ```

### 标签管理

- **创建标签**

  ```bash
  git tag <tag-name>
  ```

- **查看标签**

  ```bash
  git tag
  ```

- **推送标签**

  ```bash
  git push origin <tag-name>
  ```

### 远程仓库管理

- **添加远程仓库**

  ```bash
  git remote add <name> <url>
  ```

- **查看远程仓库**

  ```bash
  git remote -v
  ```

- **移除远程仓库**

  ```bash
  git remote remove <name>
  ```

### 暂存与恢复

- **暂存部分更改**

  ```bash
  git add -p
  ```

- **撤销未提交的更改**

  ```bash
  git checkout -- <file>
  ```

- **撤销已暂存的更改**

  ```bash
  git reset HEAD <file>
  ```

### 变更历史与比较

- **查看文件变化**

  ```bash
  git diff
  ```

- **查看某次提交的变化**

  ```bash
  git show <commit-id>
  ```

- **比较分支**

  ```bash
  git diff <branch1>..<branch2>
  ```

### 删除与清理

- **删除文件并提交**

  ```bash
  git rm <file>
  git commit -m "删除文件"
  ```

- **清理未跟踪文件**

  ```bash
  git clean -f
  ```

### 其他有用指令

- **查看别名**

  ```bash
  git config --list
  ```

- **设置别名**

  ```bash
  git config --global alias.st status
  ```

  之后可以使用 `git st` 代替 `git status`。

- **查看日志的图形化表示**

  ```bash
  git log --graph --oneline --all
  ```

### 高级功能

- **交互式变基**

  ```bash
  git rebase -i <base-branch>
  ```

- **解决冲突**

  当合并或变基时出现冲突，手动编辑冲突文件后，标记为已解决并继续操作。

  ```bash
  git add <file>
  git rebase --continue
  ```

- **别名与脚本**

  为常用操作创建 Git 别名或编写脚本以简化工作流程。

