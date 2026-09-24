# Proposal A: "Routed stream + inspector"

## 1. Design read and core idea

**Read:** a backend engineer's daily cockpit, opened next to the IDE; dense, keyboard-first, calm until something needs him (IDE / Linear / Things-with-a-debugger vibe).

**Core idea:** stop treating synced projects as a separate page. Every `- [ ]` item in a `syncNote` is **routed into the GTD list it semantically belongs to**, shown as child rows under its parent task, and a permanent right-hand inspector replaces the drawer.

Routing rule (parsed from the `###` group title, same regex family as today's `groupIcon`):

| Group | Routed to | Shown as |
|---|---|---|
| 待修 | 处理中 (and 今天 if parent is P0) | child rows, signal color |
| 我要做 | 处理中 | child rows |
| 等别人 | 等待中 | grouped under "来自 Exception 需求开发" |
| 上线前 | stays on the project | "上线闸门" checklist in inspector |
| 上线后 | 将来也许 | grouped under the project |

The 工作台 page disappears because the work is already where GTD says it should be.

## 2. Layout

### ~1440px
```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ ✓ 我的待办  今天 3  处理中 3  收集箱 1  等待中 3  将来也许 1  已完成   文档 │ ⌘K 搜索全部 │ ☁ 24° │ ⟳ 16:15 │ ⋯ │ 52px
├──────────────────────────────────────────────────────────┬───────────────────────────────┤
│ 一 22  二 23  [三 24]  四 25•  五 26  六 27  日 28   月 ▾ │ Exception 需求开发        P0  │
│ ┌ + 加一件事  回车添加        P1 ▾  @电脑 ▾  日期 ▾ ┐     │ 技术方案 v21 已过 Gate 1,     │
│                                                          │ 正在第二轮 review             │
│ 处理中                                  展开项目 ◉ 只看任务 │ [处理中▾][P0▾][@电脑▾][日期]  │
│ ○ P0 Exception 需求开发        0/13 ▯▯▯▯▯  待修 5  ›      │ 下一步                        │
│     ↳ 修第二轮 review 的 4 个 P1                          │ ┌ 修第二轮 review 的 4 个 P1 ┐ │
│     □ P1 规则改名: EnterRuleEpisode 仍会挪到… service.go  │ 上线闸门 0/4                  │
│     □ P1 backfillFounderAttribution 借旧值… aggregator.go │ □ search 接口 3 个字段谁在用   │
│     □ 自己 review PR: trackings #1391 → …        我要做   │ □ 生产 config-center …        │
│     + 另外 6 项                                            │ 进展                          │
│ ○ P0 黑五稳定性文档,发版计划                    @电脑      │ ┌ 记一条…  Enter ┐ 已完成 进行中│
│ ○ P2 Bunning 需要支持 Marketplace shipments   逾期 7 天   │ 9/24 16:07 第二轮 review: 4 P1│
│                                                          │ 9/24 15:54 v21 过 Gate 1 …    │
│                                                          │ 同步原文 ▸  (collapsed)       │
│                                                          │ 备注                          │
│                  stream: 1fr (max 880)                   │        inspector: 460px       │
└──────────────────────────────────────────────────────────┴───────────────────────────────┘
```
- No left sidebar. Lists are top tabs with mono counts; weather, sync status, export/import/backup live in the bar.
- Calendar becomes a **week strip** (due counts as tiny numerals, not dots); "月" opens a month popover. Clicking a day sets `dayFilter`; clicking again clears.
- Inspector is always on. `j/k` moves selection, `x` ticks, `e` edits title, `n` focuses 下一步, `l` focuses 进展 input.

### ~768px
Tabs scroll horizontally; ⌘K collapses to an icon; weather hides behind ⋯. Stream goes full width; the inspector becomes a 440px sheet sliding over from the right (the only overlay in the system). Week strip stays.

### ~390px
```
┌ 处理中 ▾          🔍  + ┐
│ 二 三 [四] 五 六 日 一   │
│ ○ P0 Exception 需求开发  │
│   0/13  待修 5        ›  │
│ ○ P0 黑五稳定性文档…     │
│ ○ P2 Bunning… 逾期 7 天  │
├──────────────────────────┤
│ 今天  处理中  收集箱  更多│ bottom tab bar
└──────────────────────────┘
```
Project children collapse to a one-line summary; tap pushes a full-screen inspector with a back button. Quick add opens a bottom sheet.

## 3. Where every feature lives

| Feature | Location |
|---|---|
| 收集箱 / 处理中 / 等待中 / 将来也许 / 已完成 | Top tabs (bottom bar + 更多 on phone) |
| 今天 | First tab: due today + overdue, plus 待修 rows of P0 projects in a second section |
| Calendar date filter | Week strip + month popover above the stream |
| Quick add (P0/P1/P2, context, due) | Inline bar at top of stream; `c` focuses it; defaults to current list |
| Detail: 下一步, 进展记录, 备注, list/pri/ctx/due | Inspector, always visible on desktop |
| Global search (tasks + docs + project items) | ⌘K palette, grouped 任务 / 项目条目 / 文档; Enter opens in inspector |
| 流程文档 | 文档 tab: stream shows doc list, inspector shows preview; edit expands inspector to full width |
| Weather | Top bar chip; click to set city |
| Export / import | ⋯ menu in top bar |
| Backup reminder | after 7 days a muted "12 天未备份" chip appears next to ⋯; no full-width banner |
| Synced projects | Routed child rows (see §1) + inspector header, 上线闸门, merged log, raw 同步原文 |
| Sync status | ⟳ chip with time; hover lists each source |

## 4. Synced projects: my tasks vs project progress

There is no switch to make. A project is a task with a tray:
- **Stream row:** fraction `0/13` in mono, a 5-segment bar, and "待修 N" only when N > 0. Children show 待修 then 我要做, max 3, "+ 另外 N 项" expands in place.
- **"展开项目 / 只看任务"** toggle in the list header is the density lens. "只看任务" gives a pure GTD list; "展开项目" is the workbench.
- **Inspector** carries the project-only parts: stage line, 上线闸门, the merged timeline (synced entries marked with ⟳, mine without), and a collapsed 同步原文 for the raw markdown.
- Local ticks still write to `syncChecks`; items ticked upstream render locked.
- With 6+ projects, rows sort P0 first, then by open 待修 count, so the list tells you where to look.

## 5. Visual language

**Argued change:** color means "needs you now", nothing else. The teal accent is dropped. Interaction (selection, focus, primary buttons) uses **ink**. One signal hue (vermilion) marks P0, overdue, and 待修. P1/P2 become typographic (outlined / muted). With several projects on screen, the eye lands only on what is urgent.

| Token | Light | Dark |
|---|---|---|
| --bg | #f5f6f7 | #0f1113 |
| --pane | #ffffff | #16191c |
| --sunk | #eef0f2 | #1d2125 |
| --sel (selected row) | #e9ecef | #23272c |
| --line | #e2e5e8 | #272b30 |
| --ink | #16181b | #e8eaed |
| --ink2 | #41464e | #c1c6cc |
| --muted | #6b717a | #8e959d |
| --signal | #c4432c | #ec6a52 |
| --signal-soft | #fbe9e5 | #3a201b |

Both modes follow `prefers-color-scheme`; shadows only on popovers and the palette, tinted to --ink.

**Type:** Geist + Geist Mono, PingFang SC for Chinese. Scale 11 / 12 / 13 (base) / 15 (row title) / 18 (inspector title). Weights 400/500/600. Mono for counts, fractions, times, dates, and `file.go:123` refs.

**Radius rule:** panes and popovers 10px, controls 6px, task check = circle, project item check = 4px square (owned task vs checklist item reads at a glance). Nothing else round.

**Density:** 8px grid; collapsed row 36px, child row 28px. Hairline dividers and whitespace, no cards in the stream.

**Motion:** 150ms hover, 180ms check fill, 200ms inspector content crossfade, 240ms sheet slide on tablet. `cubic-bezier(.16,1,.3,1)`. No stagger, no list animation. Reduced motion disables all.

**Icons:** Phosphor regular, one stroke weight.

## 6. Risks and trade-offs

1. **Routing depends on group titles.** If a future sync uses a new heading ("阻塞", "待确认"), items fall into a fallback bucket on the project only. Mitigation: a visible "未分类" group in the inspector and a documented heading contract in the sync-todo skill.
2. **Always-on inspector costs width.** At 1280px the stream gets about 760px; long Chinese titles with `code` refs will truncate. Mitigation: two-line clamp on child rows, full text in inspector.
3. **Dropping the accent.** Ink-only interaction is calm but less friendly, and a bad week with many overdue items turns the page red. Mitigation: signal is text/outline by default, filled only for P0 and 待修.
