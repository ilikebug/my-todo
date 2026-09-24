#!/usr/bin/env python3
"""Read/modify ~/my-todo/todo-sync.js (window.TODO_SYNCS = {source: payload}).

  write_sync.py --list
  write_sync.py --source NAME --payload payload.json
  write_sync.py --remove NAME
"""
import argparse, json, os, re, sys, time
from datetime import datetime, timezone

PATH = os.path.expanduser("~/my-todo/todo-sync.js")
HEADER = ("// 由 Claude 的 sync-todo skill 生成，不要手改。\n"
          "// todo.html 打开时按来源合并：每个来源挂到你的一条任务上。\n")


def load():
    if not os.path.exists(PATH):
        return {}
    src = open(PATH, encoding="utf-8").read()
    m = re.search(r"window\.TODO_SYNCS\s*=\s*(\{.*\});?\s*$", src, re.S)
    if m:
        return json.loads(m.group(1))
    m = re.search(r"window\.TODO_SYNC\s*=\s*(\{.*\});?\s*$", src, re.S)  # legacy single-source format
    if m:
        old = json.loads(m.group(1))
        return {old["source"]: old}
    sys.exit(f"cannot parse {PATH}")


def save(data):
    tmp = PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(HEADER + "window.TODO_SYNCS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
    os.replace(tmp, PATH)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--source")
    ap.add_argument("--payload")
    ap.add_argument("--remove")
    a = ap.parse_args()
    data = load()

    if a.list:
        if not data:
            print("(no sources yet)")
        for name, p in data.items():
            keys = [x.get("match") for x in p.get("attach", [])]
            synced = datetime.fromtimestamp(p.get("syncedAt", 0) / 1000).strftime("%Y-%m-%d %H:%M")
            print(f"- {name}  | match={keys} | synced {synced} | origin={json.dumps(p.get('origin', {}), ensure_ascii=False)}")
        return

    if a.remove:
        if data.pop(a.remove, None) is None:
            sys.exit(f"no source named {a.remove!r}")
        save(data)
        print(f"removed {a.remove}")
        return

    if not (a.source and a.payload):
        ap.error("--source and --payload are required")
    payload = json.load(open(a.payload, encoding="utf-8"))
    if not payload.get("attach"):
        sys.exit("payload needs an 'attach' list (one entry per to-do)")
    for e in payload["attach"]:
        for k in ("key", "match", "syncNote"):
            if not e.get(k):
                sys.exit(f"attach entry missing {k!r}")
    now = int(time.time() * 1000)
    payload["source"] = a.source
    payload["syncedAt"] = now
    payload["version"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload.setdefault("tasks", [])
    payload.setdefault("docs", [])
    data[a.source] = payload
    save(data)
    print(f"wrote {a.source} (version {payload['version']}) -> {PATH}; sources: {list(data)}")


if __name__ == "__main__":
    main()
