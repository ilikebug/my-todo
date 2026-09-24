# Critique: Designer B on Proposal A

A is a disciplined proposal. It is honest about what it gives up, and several of its choices are better than mine. Below is what I would take from it, then what I think breaks for this user, who uses the page daily, has 4 tasks today that will grow into several synced work streams, and reads a Chinese UI.

## Worth stealing

1. **Color means "needs you now" (§5).** This is the strongest idea in either proposal. P1 and P2 become typographic (outlined or muted), and one signal hue covers P0, overdue and 待修. Once 6 projects share a screen, that is the only thing that keeps the eye from wandering. I am adopting the typographic P1/P2 and the single signal hue. I am not dropping the accent (see problem 4).
2. **Week strip with numerals instead of dots (§2, the `四 25•` row).** A count answers "how much is due", which a dot does not, and the strip costs one line instead of a 230px calendar block. I'm taking it.
3. **Circle for owned tasks, 4px square for project checklist items (§5, radius rule).** It is a zero-cost way to tell "my GTD task" from "an item in Claude's checklist" wherever the two sit together. I'm taking it.
4. **⌘K also searches project items, and projects sort by P level, then by open 待修 count (§3 and §4).** Both are needed once more syncs arrive. I'm taking both.
5. **A backup chip instead of a banner, and a collapsed 同步原文.** These are quiet defaults and they are correct. I'm taking both.

## Serious problems for this user

1. **Routing rewrites Claude's structure in the place where it is least safe.** The routing table sends 等别人 to 等待中 and 上线后 to 将来也许. In the real `syncNote`, both groups are plain bullets, not `- [ ]` items (for example "Leo：事件量级…" and "存量合并脚本"), so they cannot be ticked or completed. They would sit in 等待中 and 将来也许 permanently, and inflate those tab counts: the top bar's "等待中 3" counts project bullets, not tasks. GTD lists stop meaning "things I own in this state". Worse, the user reads the same headings in the Claude session, so the page now disagrees with the source. (I had a milder version of this problem with my ownership split, and I am dropping it in v2 for the same reason.)
2. **There is no cross-project view, which is the thing the user actually asked for.** "Doesn't feel like a real workbench" plus "more synced projects will come" means he needs to answer "where is each stream" in one glance. In A, project state only exists as child rows inside 处理中 (at most 3 children plus "+ 另外 6 项") and inside the inspector, one project at a time. With 5 projects of about 13 items each, 处理中 becomes a long scroll that mixes tasks and checklist lines. The "展开项目 / 只看任务" toggle makes you choose between seeing the list and seeing the work.
3. **Top-tab lists hide the queue.** With lists as tabs (`今天 3 处理中 3 收集箱 1 等待中 3…`), you can see only one list at a time. His daily question is "what's overdue, what's in progress, did anything land in the inbox", and that takes three clicks. The 52px bar also has to fit 7 Chinese labels, 文档, ⌘K, weather, sync and ⋯. That fits at 1440px, but at 1280px the ⌘K field has to shrink or wrap.
4. **Dropping the accent turns day one mostly red.** Today 2 of 3 tasks in 处理中 are P0, 1 is overdue, and the project has 待修 5. Under A's rule most rows carry vermilion on first load, and selection is only an `#e9ecef` background in light mode, which is weak for keyboard focus. "Signal only when urgent" works when urgency is rare. Here it is the norm, so a neutral accent for selection and focus still has a job.
5. **Doc editing "expands the inspector to full width."** It is a mode switch that hides the stream while editing a runbook, and it is the only place where the inspector changes shape. That is a lot of special-casing for a feature he uses weekly.
