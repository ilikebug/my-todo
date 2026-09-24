# Proposal A v2: "Routed stream + inspector"

## 1. Read and core idea (unchanged)

**Read:** a backend engineer's daily cockpit, open next to the IDE. Dense, keyboard-first, calm until something needs him.

**Core idea:** there is no separate project page. Each synced checklist item is routed into the GTD list it belongs to and shown as a child row under its parent task. One always-open inspector on the right holds everything about the selected item: detail, 下一步, 进展记录 and 备注, all in one place.

**New in v2, taken from B:** a status bar for ambient info, token quick add, a project matrix as a third lens, the 需要我动手 / 盯着就行 split in the inspector, a merged "今天动过的" timeline, and a "按原文顺序" toggle.

## 2. Layout

### ~1440px
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ✓ 我的待办   今天 3  处理中 3  收集箱 1  等待中 3  将来也许 1  已完成  文档   ⌘K 搜索   │ 48
├──────────────────────────────────────────────────────────┬─────────────────────────────┤
│ 一22  二23 [三24] 四25  五26  六27  日28   9月 ▾          │ Exception 需求开发      P0  │
│ ┌ + 加一件事  p0 @电脑 ^周五 ⏎      [P0][@电脑][9/26] ┐   │ 技术方案 v21 已过 Gate 1,   │
│                                                          │ 正在第二轮 review           │
│ 处理中                     [只看任务 | 展开项目 | 项目总览]  │ [处理中▾][P0▾][@电脑▾][日期]│
│ ○ P0 Exception 需求开发          0/13  待修 5   ⟳ 16:15   │ 下一步 [修第二轮 review 的…]│
│     ↳ 修第二轮 review 的 4 个 P1                          │ 需要我动手                  │
│     □ P1 规则改名: 批量进入 EnterRuleEpisode 仍会挪到     │  待修 5  我要做 4  上线前 4  │
│       新名字  service.go:1265                             │ 盯着就行                    │
│     □ 自己 review PR: trackings #1391 → search #432 …    │  等别人 3  上线后 1          │
│     + 另外 7 项                                            │           按原文顺序 ○      │
│ ○ P0 黑五稳定性文档,发版计划                    @电脑      │ 进展  [记一条… ⏎]           │
│ ○ P2 Bunning 需要支持 Marketplace shipments   逾期 7 天   │  9/24 16:07 ⟳ 第二轮 review │
│                                                          │  9/24 15:54 ⟳ v21 过 Gate 1 │
│                                                          │ 备注 [                    ] │
├──────────────────────────────────────────────────────────┴─────────────────────────────┤
│ ⟳ 1 个来源  16:15      备份 9 天前 [导出]      ☁ 上海 23°      j/k 选择  x 勾选  ⌘K    │ 28
└────────────────────────────────────────────────────────────────────────────────────────┘
```
- The top bar now holds only navigation and search. Sync, backup, weather and shortcut hints move to a **status bar** (B's idea).
- **Quick add** takes tokens (`p0`, `@电脑`, `^周五`), and they turn into pills. The pills are also clickable menus, so the mouse path stays visible.
- **Three lenses** in the list header: 只看任务 (plain GTD), 展开项目 (child rows, the default in 处理中), and **项目总览**, B's matrix with one row per project and 待修 / 我要做 / 等别人 / 上线前 counts as mono columns. The matrix is a view, not the home screen, so it only earns its space once there are several projects.
- The 今天 tab gets a second section, **今天动过的**: a merged log from all tasks and projects for the day (B's timeline, scoped to where the question is asked).

### (c) Width at 1280px, decided
The inspector is fluid: `clamp(360px, 30vw, 440px)`. At 1280px that is 384px, which leaves the list about 850px of content width after padding. That is more than v1's 760px and enough for the longest real title plus meta on one line. Child rows get a two-line clamp. **Below 1180px** the inspector stops docking and becomes a 400px sheet over the list, so the list never drops under 760px.

### ~768px
Tabs scroll horizontally. The inspector is a right sheet, and the status bar keeps the sync icon, backup age and temperature. The 项目总览 lens drops the 上线前 column.

### ~390px
Bottom tab bar: 今天 / 处理中 / 收集箱 / 更多. Project children collapse to a summary line (`0/13  待修 5`). Tapping a row pushes a full-screen inspector with a back button. Quick add is a fixed input above the tab bar. Status items move into 更多.

## 3. Feature map (changes only)

| Feature | v2 location |
|---|---|
| Weather, sync status | Status bar |
| Backup reminder | Status bar shows the backup age at all times and turns amber after 7 days. After **14 days** a one-line notice with [导出] also appears above the list, dismissible for the session. Two levels, because localStorage is the only copy |
| Export / import | [导出] in the status bar; import in ⌘K commands and the 更多 menu |
| Quick add | Token input plus clickable pills |
| Synced project overview | 项目总览 lens |
| Cross-project "what moved" | 今天 → 今天动过的 |

Everything else stays as in v1: lists as tabs, 今天 with P0 待修 rows, week strip plus month popover as the date filter, ⌘K search across tasks, project items and docs, docs as a list with preview in the inspector, and detail always in the inspector.

## 4. (b) When sync headings don't match the routing, decided

Routing uses a keyword table (待修/bug/阻塞 → act-now; 我要做/我来 → act; 等/依赖 → watch; 上线前/检查 → launch checklist; 上线后/以后 → later). Rules:
1. **Unknown headings are never routed out of the project.** Their items stay under the project row in its current list and show in the inspector under their original heading, in source order.
2. **They are not hidden.** The project row shows an `未归类 N` count next to `待修 N` until the group is known, so a new heading from Claude is noticed on day one.
3. **按原文顺序** in the inspector turns off ownership grouping and shows the syncNote exactly as written. The raw markdown is one click further.
4. Items without a checkbox (for example under 等别人) route as read-only bullets. Items ticked upstream render as locked.
5. I'll suggest (not make) a heading contract for the sync-todo skill so new streams use the five known headings.

## 5. (a) Accent color, decided: keep teal

In v1 I proposed dropping teal. I'm reversing that. The user has seen the teal refresh and liked it, it matches the favicon, and for a daily personal tool, continuity is worth more than a stronger design statement. What v1 got right carries over as a **usage rule**, not a palette change:
- **Teal** (#0f766e / dark #3cb3a4) is used only for interaction and progress: selection bar, focus ring, primary button, progress fraction and ticked boxes.
- **Red** (#c4432c / dark #ec6a52) means "needs you now": P0, overdue and 待修 counts above 0. Nothing else is red.
- **Amber** is only for the backup warning and P1 labels, used as text, never as fills.
- Selected rows use a neutral --sel background with a 2px teal left edge, not a teal fill, so a long list stays calm.

Other tokens are unchanged from v1 (bg #f5f6f7/#0f1113, pane #fff/#16191c, line #e2e5e8/#272b30, ink #16181b/#e8eaed). Type is unchanged: Geist, Geist Mono and PingFang SC; 11/12/13/15/18; mono for counts, times and file:line. Radius: panes 10, controls 6, round check for tasks, square 4px check for synced items. Motion is 150-240ms, with no drawer slide on desktop.

## 6. Remaining risks

1. **Three lenses is one more concept.** The default is picked per list (展开项目 in 处理中, 只看任务 elsewhere) and remembered, so most days the toggle is never touched.
2. **Child rows make 处理中 long at 5+ projects.** The cap is 3 child rows per project, sorted by open 待修; beyond that, 项目总览 is the intended view.
3. **Tokens can misparse Chinese text** (for example `^周五` inside a sentence). Tokens are recognized only when separated by spaces, and the pill preview shows what was parsed before Enter.

## Note after B's critique (built into demo-A.html)

**Plain bullets never leave the project.** B was right: 等别人 and 上线后 are plain `- ` bullets in the real sync note, so routing them into 等待中 / 将来也许 would leave rows there that can never be completed. In the demo only `- [ ]` items are routed (待修 and 我要做 as child rows, 上线前 as the launch checklist in the detail panel). 等别人 and 上线后 stay in the detail panel under "盯着就行" and count only in the 项目总览 matrix. Tab counts include real tasks only. 等待中 and 将来也许 show them as a folded, read-only "项目里在等的人 / 项目上线后的事" section marked "不计入本清单". Each 等别人 bullet has a one-click "转成任务", which creates a real, completable 等待中 task (note: 来自项目 X) and marks the bullet "已转成任务". The sample project includes a `### 待确认` heading, which shows how an unknown heading is handled (the 未归类 count on the row, and the group kept as-is in the detail panel).
