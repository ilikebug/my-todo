# my-todo

个人 GTD 待办页面，单个 HTML 文件，数据存在浏览器的 localStorage 里。

- `todo.html`：页面本体，直接用浏览器打开
- `todo-sync.js`：Claude 的 sync-todo skill 生成的项目进度，页面打开时合并
- `skill/sync-todo/`：sync-todo skill 的副本（实际使用的在 `~/.claude/skills/sync-todo/`）
- `backups/page/`：页面旧版本
- `backups/data/`：页面「导出」得到的数据备份
- `design/`：布局改版时两份设计方案、互评和 demo
