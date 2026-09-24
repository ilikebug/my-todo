# Proposal B: "IDE for your day"

## 1. Read and core idea
**Design read:** a personal command center for one backend engineer who lives in JetBrains and terminals. It should feel like a dense, calm, keyboard-first tool, the way an IDE feels, not like a to-do app.

**Core idea:** use an IDE layout. The queue on the left works like a project tree, anything you open becomes a tab in the center editor, the right tool window is a shared timeline of everything that happened, and a status bar holds the ambient stuff (weather, sync, backup).

Why this differs from the obvious redesign (sidebar + list + detail panel): it has no drawer, no separate 工作台 page and no widgets in a sidebar. Projects, tasks and docs all open the same way, as tabs. The "how is everything going" question gets its own screen, a matrix, instead of a stack of cards.

## 2. Layout

### ~1440px
```
+--------------------------------------------------------------------------------------------+
| [v] 我的待办   [ ⌘K  搜索 / 新建 / 跳转 …                    ]            9月24日 周四       |  40
+----------------------+---------------------------------------------------+-----------------+
| QUEUE          260px | [全部项目] [Exception 需求开发 x] [发版流程.md x]  | TIMELINE  320px |
| 22 23[24]25 26 27 28 |---------------------------------------------------|  [记一条… ⏎ ]   |
|  .     .  ..         |  Exception 需求开发                  P0  处理中     |  为: Exception  |
| v 今天            2  |  AI Anomaly Prediction · 同步于 16:15               | --- 今天 ------ |
|   ! Bunning 逾期7天  |  技术方案 v21 已过 Gate 1，正在第二轮 review        | 16:07 Exception |
|   * 黑五稳定性 P0    |  +-----------------------------------------------+ |  第二轮 review: |
| v 处理中          3  |  | -> 下一步  修第二轮 review 的 4 个 P1          | |  4 个 P1 …      |
|   ~ Exception  3/14  |  +-----------------------------------------------+ | 15:54 Exception |
|     黑五稳定性   P0  |  需要我动手 ---------------  盯着就行 ------------- |  v21 过 Gate 1  |
|     Bunning      P2  |  待修 5                      等别人 3              | --- 昨天 ------ |
| > 等待中          0  |  [ ] P1 规则改名 …1265       - Leo：事件量级 …     | 18:40 黑五稳定性|
| > 收集箱          1  |  [ ] P1 backfill… :431       - 理松/Eason #432     |  发版计划初稿   |
| > 将来也许        0  |  我要做 4                    上线后 1              |                 |
| > 已完成         12  |  [ ] 自己 review PR …        - 存量合并脚本        |                 |
| ---- 文档 ---------- |  上线前 4                    ------------------    |                 |
|   发布上线流程       |  [ ] search 接口字段 …       我的备注              |                 |
|                      |                              [ textarea          ] |                 |
+----------------------+---------------------------------------------------+-----------------+
| ⟳ 1 个来源 · 16:15  |  备份 9 天前 [导出]  |  上海 23° 多云  |  j/k 移动  ⏎ 打开  ⌘K 命令  |  28
+--------------------------------------------------------------------------------------------+
```
Center pane default tab **全部项目**, one row per synced project with the group counts as columns (numbers in mono):
```
项目                    阶段 / 下一步                 待修 我要做 等别人 上线前  进度    更新
Exception 需求开发 P0   修第二轮 review 的 4 个 P1      5     4     3     4   3/14  16:15
```
Plain tasks open in the same editor: title, controls row (清单 / 优先级 / 情境 / 截止), 下一步, 备注. Their log lives in the timeline, filtered to the task.

### ~768px
Two panes: queue (240) and editor. The timeline turns into a right tool window toggled with `⌘J` or a status-bar button, overlaying the editor. Tabs scroll horizontally. The status bar stays but drops the weather text and keeps only the icon plus temperature.

### ~390px
One pane at a time, with a bottom tab bar: **队列 / 项目 / 时间线 / 文档**. Opening an item pushes a full-screen editor with a back chevron. The project matrix turns into stacked rows (name, next step, a counts line). The ⌘K bar becomes a search icon in the header, and quick add becomes a fixed input above the tab bar. Status-bar items (sync, backup, weather) move to a "状态" sheet reached from the header.

## 3. Where each feature lives
| Feature | Location |
|---|---|
| 收集箱 / 处理中 / 等待中 / 将来也许 / 已完成 | Queue sections, collapsible, with counts. 已完成 is collapsed by default |
| 今天 | Pinned top queue section: due today plus overdue, overdue rows first and marked in red |
| Calendar filter | A 7-day strip at the top of the queue with due-count ticks. Click a day to filter, click the month label to open a month popover |
| Quick add (P0/P1/P2, @情境, due) | ⌘K bar: typing plain text creates a task, and inline tokens `p0 @电脑 ^周五` are parsed into pills. A "新建" button is the mouse path |
| Detail: 下一步, 备注, controls | Editor tab |
| 进展记录 | Timeline: the input at the top writes to the focused item, and the full per-task history appears when the timeline is filtered |
| Global search | ⌘K: task and doc results in one grouped list |
| 流程文档 | Queue section "文档". Opens as an editor tab with an edit/preview toggle |
| Weather | Status bar |
| Export/import, backup reminder | Status bar: the backup age turns amber when overdue and shows [导出]. Import is in the ⌘K commands |
| Sync status | Status bar, with a per-source tooltip |

## 4. Synced projects
- **Queue row:** a synced task gets a small sync glyph and a `3/14` fraction, so you can tell it apart from plain tasks in place.
- **Overview (全部项目 tab):** a matrix you can scan in 3 seconds. Red is used only for 待修 counts above 0. Click a count cell to open that project scrolled to that group.
- **Project tab:** the stage line, then a 下一步 bar, then groups split by **ownership** instead of the source order. "需要我动手" (待修, 我要做, 上线前) are tickable and sit on the left. "盯着就行" (等别人, 上线后) are read-only bullets on the right with my own notes below them. Unknown group names fall into the column that matches `groupIcon`, or into "其他".
- **Switching between my tasks and project progress** is a key press, not a page change: `g p` opens the overview, `g q` focuses the queue, `⌘1–9` switches tabs. Open tabs persist in localStorage.
- **The timeline merges every task's and project's log** (synced entries tagged with the source), which answers "what moved today" across all work streams.

## 5. Visual language
Keep the teal accent (it carries over from the favicon and there's no reason to change it), but use it only for focus, selection, progress and the primary action. Hierarchy comes from structure: panes are separated by 1px hairlines, with no cards and no shadows except on floating layers.

| Token | Light | Dark |
|---|---|---|
| --chrome (bars) | #eef0f2 | #0e1012 |
| --pane | #fbfbfc | #15181b |
| --pane-2 (headers, hover) | #f2f4f6 | #1b1f23 |
| --line / --line-2 | #e2e5e8 / #d1d6db | #262a2f / #343a40 |
| --ink / --ink-2 / --muted | #16181b / #3a3f46 / #6a717a | #e6e8eb / #c0c5cb / #8f97a0 |
| --accent / --accent-soft | #0f766e / #e1efed | #3cb3a4 / #14302c |
| --p0 / --p1 / --p2 | #c43d3d / #a8701c / #7b8490 | #e06a6a / #d4a045 / #8a939e |

- **Type:** Geist + PingFang SC, with Geist Mono for all times, counts, dates, P-levels and file:line references. Scale: 11 mono meta, 12 labels, 13 rows (base), 14 editor body, 16 pane titles, 20 editor title (600, -0.02em). The base drops from 14 to 13 to get the density.
- **Radius:** panes 0 (split edges), floating layers (⌘K, popovers) 8, controls 6, tags and checkboxes 4. No pills.
- **Density:** 30px queue rows, 28px checklist rows, 12/16 pane padding. A 1440px screen shows about 25 queue rows.
- **Motion:** 120ms for hover and selection, 160ms opacity-only tab swaps, a 150ms tick, and the ⌘K palette fades and scales from 0.98. No sliding drawers. Reduced-motion is respected.
- **Icons:** Phosphor Regular only, one weight.

## 6. Risks and trade-offs
1. **Busy with little data.** Three panes plus a status bar is a lot of frame for 4 tasks and 1 project. Mitigations: the timeline and matrix need real empty states, and the timeline can be collapsed and stay collapsed.
2. **The IDE metaphor adds state and a learning curve.** Tabs, focus zones and shortcuts must never be the only path. Every action needs a visible mouse target, and tab persistence must not resurrect deleted items.
3. **Regrouping by ownership reinterprets Claude's markdown.** If a sync uses new group names, the split can misplace items. Risk of "why did my section move." Mitigation: a toggle for "按原文顺序", and the raw syncNote is always one click away in the project tab.
