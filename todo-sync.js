// 由 Claude 的 sync-todo skill 生成，不要手改。
// todo.html 打开时按来源合并：每个来源挂到你的一条任务上。
window.TODO_SYNCS = {
 "AI Anomaly Prediction": {
  "origin": {
   "kind": "claude-session",
   "session_title": "ai anomaly prediction",
   "session_id": "local_34f07015-afc2-437c-809f-825939e650df",
   "group": "Exception 需求开发"
  },
  "removePrefixes": [
   "sync:aap:"
  ],
  "attach": [
   {
    "key": "exception",
    "match": "exception",
    "fallbackText": "Exception 需求",
    "next": "修第二轮 review 的 4 个 P1",
    "syncNote": "**AI Anomaly Prediction**：把 AI 异常预测接成 Exception Workspace 的第 4 个来源。技术方案 v21 已过 Gate 1，代码基本写完，正在第二轮 review。\n\n### 🔴 待修（第二轮 review）\n- [ ] P1 规则改名：批量进入 `EnterRuleEpisode` 仍会挪到新名字（service.go:1265）\n- [ ] P1 `backfillFounderAttribution` 把旧值借给合法为空的 member（aggregator.go:431）\n- [ ] P1 Fold 时间窗口受输入顺序影响（aggregator.go:149）\n- [ ] P1 carrier 行上 manually-marked-checkpoint member 借不到 reason（aggregator.go:434）\n- [ ] P2 ×6：stale_run_hour_close 判据顺序、DelayBenchmarks 白名单、锁计数缺测试、flag 补偿、死代码、重复函数\n- 「测试有效性」agent 还没跑完，清单可能还会加\n\n### 我要做\n- [ ] 自己 review PR：trackings #1391 → search-platform #432 → shipments #958 / #932\n- [ ] 找 BFF owner：补 `delayBenchmark` 映射 + 保存时读旧值合并\n- [ ] 提交 shipments 的 go.mod / go.sum（mocha v1.2.269）\n- [ ] 决定何时把 status 改成 under-development（改后 PRD / 方案冻结）\n\n### 等别人\n- Leo：事件量级、生产 topic、age_days 锚点、probability 单调性\n- 理松 / Eason：#432 review、reindex 窗口\n- 设计：benchmark 下拉改两个选项；QA：用例按增量重写\n\n### 上线前\n- [ ] search 接口 exception_episodes 三个字段谁在用\n- [ ] 生产 config-center：Held for customs clearance 带 default_disabled: true，配两个新 type、3 个 reason\n- [ ] 前端 AI 来源筛选值 aedd → ai_prediction\n- [ ] 撞名扫描、Grafana 告警、DROP INDEX 检查文档、发布 runbook\n\n### 上线后\n- 存量同 type 多行合并脚本（Task 12）",
    "log": [
     {
      "t": 1790219580000,
      "text": "已私信 Leo：delay_benchmark 事件字段约定"
     },
     {
      "t": 1790220780000,
      "text": "trackings #1391 开 PR；exception_setting 按键合并定为 BFF 负责"
     },
     {
      "t": 1790231760000,
      "text": "第一轮 review 修完：3 个 🔴、老路径恢复原行为、P2 ×7"
     },
     {
      "t": 1790235240000,
      "text": "技术方案 v21 过 Gate 1；PRD 增量：benchmark 只做两个选项；#1391 bot review 已驳回"
     },
     {
      "t": 1790236020000,
      "text": "第二轮 review：4 个 P1、6 个 P2 待修"
     }
    ]
   }
  ],
  "source": "AI Anomaly Prediction",
  "syncedAt": 1790237753368,
  "version": "2026-09-24T08:15:53Z",
  "tasks": [],
  "docs": []
 }
};
