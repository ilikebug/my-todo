#!/usr/bin/env python3
"""Condense an exported Claude session (zip from export_transcript, or a .jsonl) into
user messages + substantive assistant replies, oldest first, with UTC timestamps.

  digest_session.py <export.zip|session.jsonl> [--out digest.txt] [--since 2026-09-20]
"""
import argparse, io, json, sys, zipfile


def lines_from(path):
    if path.endswith(".zip"):
        z = zipfile.ZipFile(path)
        # main transcript = the largest top-level .jsonl (subagent transcripts live in subfolders)
        names = [n for n in z.namelist() if n.endswith(".jsonl") and "/" not in n.strip("/")]
        if not names:
            sys.exit("no transcript .jsonl in zip")
        main = max(names, key=lambda n: z.getinfo(n).file_size)
        return io.TextIOWrapper(z.open(main), encoding="utf-8")
    return open(path, encoding="utf-8")


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(x.get("text", "") for x in content if isinstance(x, dict) and x.get("type") == "text")
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--out")
    ap.add_argument("--since", help="only keep entries at/after this ISO date")
    a = ap.parse_args()
    out = []
    for ln in lines_from(a.path):
        try:
            e = json.loads(ln)
        except ValueError:
            continue
        ts = (e.get("timestamp") or "")[:16]
        if a.since and ts and ts < a.since:
            continue
        txt = text_of((e.get("message") or {}).get("content")).strip()
        if e.get("type") == "user":
            # drop tool results, notifications, injected skill bodies and command echoes
            if not txt or txt.startswith(("<task-notification", "<local-command", "<system", "Base directory for this skill")) \
                    or "<command-" in txt[:40]:
                continue
            out.append(f"\n=== USER {ts}\n{txt[:1500]}")
        elif e.get("type") == "assistant" and len(txt) > 200:
            out.append(f"\n--- AI {ts}\n{txt[:1500]}")
    res = "\n".join(out)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(res)
        print(f"{len(out)} entries, {len(res)} chars -> {a.out}")
    else:
        print(res)


if __name__ == "__main__":
    main()
