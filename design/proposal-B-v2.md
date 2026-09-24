# Proposal B v2: "IDE for your day", tightened

## 1. Read and core idea (unchanged)
**Design read:** a dense, calm, keyboard-friendly command center for a backend engineer who lives in an IDE.

**Core idea:** the queue on the left is the project tree, and anything you open (a task, a project or a doc) becomes a tab in the center editor. The default tab, **总览**, answers "where is every work stream" in one glance.

What changed from v1: the permanent third pane is gone, the ownership regrouping is dropped, and the shortcuts are cut down to a set that doesn't clash with the browser. From A, I've taken the signal color rule, the numeral week strip, the circle vs square checks, search over project items, and the project sort order.

## 2. Layout

### ~1440px (the frame is 2 panes plus a status bar)
```
+--------------------------------------------------------------------------------------------+
| [v] 我的待办        [ 搜索或新建…  ⌘K ]   [+ 新建]                        9月24日 周四     | 40
+----------------------+---------------------------------------------------------------------+
| 队列           272px | [总览] [Exception 需求开发 x] [*发布上线流程*]                        |
| 一 二 [三] 四 五 六 日|---------------------------------------------------------------------|
| 22 23  24  25 26 27 28|  总览                                                              |
|         2   .  1     |  项目 1                                    排序：优先级, 待修        |
| 今天              2  |  Exception 需求开发  P0   修第二轮 review 的 4 个 P1                  |
|   o Bunning  逾期7天 |      待修 5   我要做 4   等别人 3   上线前 4   上线后 1   3/14 16:15 |
|   o 黑五稳定性    P0 |  ---------------------------------------------------------------   |
| 处理中            3  |  今天到期 2                        最近进展                          |
|   o Exception  ⟳3/14 |  o Bunning … 逾期 7 天             16:07 Exception 第二轮 review…   |
|     待修 5 · 我要做 4|  o 黑五稳定性文档，发版计划        15:54 Exception v21 过 Gate 1    |
|   o 黑五稳定性    P0 |                                    昨天 18:40 黑五 发版计划初稿      |
|   o Bunning       P2 |                                                                     |
| 收集箱            1  |                                                                     |
|   o 查一下 …         |                                                                     |
| 等待中 0 · 将来也许 0|                                                                     |
| 已完成 12         >  |                                                                     |
| 文档              1  |                                                                     |
+----------------------+---------------------------------------------------------------------+
| ⟳ 1 个来源 16:15   |   上次备份 9 天前 · 导出   |   上海 23° 多云                              | 28
+--------------------------------------------------------------------------------------------+
```
**Project tab** (the center splits into content 1fr and log 300px):
```
Exception 需求开发  P0 · 处理中 · @电脑 · 截止 —     [处理中▾][P0▾][@电脑▾][日期]
AI Anomaly Prediction · 同步 16:15 · 技术方案 v21 已过 Gate 1，正在第二轮 review
| 下一步  修第二轮 review 的 4 个 P1                    |  进展            [记一条… ⏎]
待修 5 (signal)            我要做 4                    |  16:07 ⟳ 第二轮 review …
[] P1 规则改名 … service.go:1265   [] 自己 review PR …  |  15:54 ⟳ v21 过 Gate 1 …
[] P1 backfill … aggregator.go:431 [] 找 BFF owner …    |  13:46 ⟳ 第一轮 review 修完
等别人 3                   上线前 4                    |  备注
- Leo：事件量级 …          [] search 接口字段 …        |  [ textarea            ]
上线后 1                                               |  同步原文 ▸
```
Groups keep **Claude's order and headings** and flow into two columns (CSS columns, so no forced equal heights). A plain task tab uses the same frame without the groups: controls, 下一步, 备注 on the left and 进展 on the right.

### ~768px
The queue narrows to 232px. The tab's log column moves below the content. The status bar keeps the icons, sync time and temperature only.

### ~390px
A bottom tab bar with **队列 / 总览 / 文档**. Opening an item pushes a full-screen tab with a back chevron. 总览 rows stack (name, next step, counts line). Search is an icon in the header. [+] opens a bottom sheet. Status-bar items move into a "状态" sheet.

## 3. Feature map (changes from v1 only)
| Feature | Location |
|---|---|
| Calendar | Week strip with due counts as numerals (from A). Clicking a date filters the queue, clicking again clears it, and 月 opens a month popover |
| 进展记录 | The log column inside each task or project tab. The merged view is "最近进展" on 总览 |
| Quick add | [+ 新建] opens a small form (title, P, @, date), prefilled with the list you're focused on. ⌘K also creates a task when there's no match (no token parsing in the demo) |
| Search | ⌘K over tasks, **project items** (from A) and docs, grouped |
| Docs | Open as a normal tab with an edit/preview toggle. No special modes |

Everything else stays as in v1.

## 4. Decisions

**(a) Not empty, not heavy.** The frame is 2 panes, and there is no third pane to sit idle. Empty lists collapse into one dim line (`等待中 0 · 将来也许 0`), so today's queue shows 6 rows with no dead sections. 总览 carries its own content even with one project: the project row, today's due tasks, and the merged recent log. With one project, 总览 reads as a daily brief, and with six, it becomes a matrix of work streams. Tabs follow the **preview tab** rule: a single click replaces the one italic preview tab, and a tab only stays open if you edit it or double-click. At most 6 tabs, and 总览 is pinned. That stops tabs from piling up.

**(b) Claude's groups are shown as they are.** I've dropped the ownership regrouping. The markdown is a contract between the user, Claude and the sync-todo skill, and he reads the same headings in the Claude session. Reinterpreting it fails silently when the headings change. The visual cues do the work instead: square checks for items he can tick, bullets for read-only lines, signal color on 待修 only. 总览's columns are the headings as written, with the five known ones in a fixed order and any unknown heading added after them.

**(c) Shortcuts in the demo:** `⌘K`/`Ctrl K` and `/` open search, `Esc` closes palette/popover/preview, `j`/`k` move and `Enter` opens in the queue, `x` ticks the selected task or item, `c` opens new-task. Each one has a mouse target: the search field, the rows, the checks, the [+ 新建] button and the close control on each tab. **Later:** `g` chords, tab switching, field-focus keys. v1's `⌘1–9`, `⌘W` and `⌘J` are dropped because the browser owns them.

## 5. Visual language (deltas)
- **Color rule (from A, softened):** `--signal` (#c4432c / #ec6a52) marks only overdue dates, P0 labels, and 待修 counts above 0, as text or outline, never as filled rows. P1 is shown as an outlined label and P2 as muted text. Teal (#0f766e / #3cb3a4) stays, but only for selection, focus rings, progress and the one primary button. That leaves exactly one chromatic color each for "you're here" and "needs you".
- **Checks:** a circle for tasks, a 4px square for checklist items.
- Tokens, type scale (13 base, 20 editor title), radius (panes 0, floating 8, controls 6, tags 4) and motion stay as in v1. Tab swaps are an opacity-only crossfade.

## 6. Remaining risks
1. **Preview tabs** are an IDE habit that a mouse user may find surprising. The italic title and a double-click-to-keep behavior have to be obvious.
2. **Two-column groups** in the project tab can get lopsided when one group has 15 items. Groups longer than 6 collapse behind "展开全部 N 项".
3. **总览 at 10+ projects** needs vertical scroll. That is acceptable, but the sort order (P level, then open 待修) has to carry it.

## 7. Note: what the demo does about A's critique
- **Too much frame for the data.** There are 2 panes plus a 28px status bar, and no third pane. 总览 is a daily brief: the project table, today's due tasks and the merged log. Empty lists (等待中, 将来也许) collapse into one dim line. A second, sample-labeled project shows the table at more than one row.
- **Which task a log goes to.** The progress input lives inside each task's tab. It is headed "记到 <任务名>", and its placeholder and aria-label name the task too. After you submit, a toast repeats the task name. Synced log entries carry a sync icon, and the ones you write don't.
- **Tabs piling up.** A single click opens one italic preview tab and replaces it on the next click. A tab only stays open when you double-click it, edit something in it or tick an item. The cap is 6 tabs, and 总览 is pinned. Nothing is persisted.
- **Truncated Chinese titles.** The queue is 300px, and titles wrap to 2 lines instead of truncating. 今天 is a filter toggle (全部 / 今天), not a separate section, so rows no longer repeat.
- **Backup reminder.** The status bar shows the backup age and turns amber after 7 days. 总览 also shows a one-line notice with an 导出备份 button.
- **Progress figure.** Progress is computed from the note: 0/13 checkable items for Exception. Group counts use only the unticked checkboxes when a group has any, so 待修 shows 5 (the note line about "测试有效性" isn't counted).
