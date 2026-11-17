#!/usr/bin/env python3
"""
Capstone: run the five criteria in criteria.md (C1–C5) three times against the
deployed service, and write the run log.

    export CACHE_ADMIN_TOKEN=...            # the same value as on Render
    python run_capstone.py --label before
    python run_capstone.py --label after

Each trial:
  1. empties the response cache (POST /cache/clear) and notes how many
     records the server's log already has (GET /logs);
  2. C1–C3: sends 5 queries that reach a fit card, then each one again;
  3. C4:    sends 3 queries that match nothing, each one twice;
  4. C5:    sends 2 bad requests (an empty body, and a body with no query);
  5. reads back only the log records added during this trial, and scores them.

That is 18 requests and 10 model calls a trial. The free Gemini tier allows 15
calls a minute, so the script waits --pause seconds between trials.

Writes results/capstone_<date>_<label>.md (the run log and real output) and a
.json file next to it with everything that came back.
"""

import argparse
import datetime as dt
import json
import os
import statistics
import sys
import time

import requests

import config

DEFAULT_URL = "https://fitfindr-hefr.onrender.com"

HIT_QUERIES = [            # C1–C3: each finds a listing, so each reaches a fit card
    "vintage graphic tee under $30",
    "90s track jacket size M",
    "leather belt",
    "chelsea boots",
    "denim shorts under $30",
]
ERROR_QUERIES = [          # C4: each matches nothing, so session["error"] is set
    "purple ballgown size XXS under $5",
    "gold sequin cape under $3",
    "wedding dress size XXS",
]
LOG_FIELDS = ["timestamp", "query", "status", "cache_hit", "duration_ms",
              "model_calls", "prompt_tokens", "output_tokens", "error"]


def ask(url, query):
    r = requests.post(f"{url}/ask", json={"query": query}, timeout=180)
    return r.status_code, r.json()


def run_trial(url, headers):
    r = requests.post(f"{url}/cache/clear", headers=headers, timeout=30)
    r.raise_for_status()
    log_before = len(requests.get(f"{url}/logs", headers=headers, timeout=30).json())

    sent = []   # (kind, query, status, response) in the order sent

    for q in HIT_QUERIES:
        sent.append(("first", q, *ask(url, q)))
    for q in HIT_QUERIES:
        sent.append(("second", q, *ask(url, q)))
    for q in ERROR_QUERIES:
        sent.append(("error_first", q, *ask(url, q)))
        sent.append(("error_second", q, *ask(url, q)))
    r = requests.post(f"{url}/ask", data="", headers={"Content-Type": "application/json"}, timeout=30)
    sent.append(("bad_empty_body", None, r.status_code, r.json()))
    r = requests.post(f"{url}/ask", json={"wardrobe": {}}, timeout=30)
    sent.append(("bad_no_query", None, r.status_code, r.json()))

    new_records = requests.get(f"{url}/logs", headers=headers, timeout=30).json()[log_before:]
    # One caller, one request at a time: the n-th request sent is the n-th new record.
    records = new_records + [None] * (len(sent) - len(new_records))

    firsts = {q: resp for kind, q, _, resp in sent if kind == "first"}
    seconds = [(q, resp, rec) for (kind, q, _, resp), rec in zip(sent, records) if kind == "second"]

    # C1: second send logged as a hit with no model calls
    c1 = sum(1 for _, _, rec in seconds
             if rec and rec.get("cache_hit") is True and rec.get("model_calls") == 0)

    # C2: median server-side duration of those hits
    hit_ms = [rec["duration_ms"] for _, _, rec in seconds if rec and rec.get("cache_hit")]
    c2 = statistics.median(hit_ms) if hit_ms else None

    # C3: second response has the same item id, outfit text and fit card as the first
    def same(a, b):
        return ((a.get("selected_item") or {}).get("id") == (b.get("selected_item") or {}).get("id")
                and a.get("outfit_suggestion") == b.get("outfit_suggestion")
                and a.get("fit_card") == b.get("fit_card")
                and a.get("fit_card") is not None)
    c3 = sum(1 for q, resp, _ in seconds if same(firsts[q], resp))

    # C4: the second send of a failing query is not a cache hit
    c4 = sum(1 for (kind, _, _, resp), rec in zip(sent, records)
             if kind == "error_second" and resp.get("cache_hit") is False
             and rec and rec.get("cache_hit") is False)

    # C5: one record per request, each with every field
    complete = sum(1 for rec in new_records if all(f in rec for f in LOG_FIELDS))
    c5 = (len(new_records), complete, len(sent))

    return {
        "scores": {"C1": c1, "C2": c2, "C3": c3, "C4": c4, "C5": c5},
        "hit_ms": hit_ms,
        "sent": [{"kind": k, "query": q, "status": s,
                  "cache_hit": resp.get("cache_hit"),
                  "selected_item": (resp.get("selected_item") or {}).get("id"),
                  "fit_card": resp.get("fit_card"),
                  "error": resp.get("error")} for k, q, s, resp in sent],
        "records": new_records,
    }


def verdicts(trials):
    s = [t["scores"] for t in trials]
    return {
        "C1": all(x["C1"] == 5 for x in s),
        "C2": all(x["C2"] is not None and x["C2"] <= 50 for x in s),
        "C3": all(x["C3"] == 5 for x in s),
        "C4": all(x["C4"] == 3 for x in s),
        "C5": all(x["C5"][0] == x["C5"][2] and x["C5"][1] == x["C5"][2] for x in s),
    }


def write_report(trials, args):
    v = verdicts(trials)
    mark = lambda ok: "MET" if ok else "**MISSED**"
    s = [t["scores"] for t in trials]
    rows = [
        ("C1. A cache hit doesn't call the model", "5 of 5", [f"{x['C1']}/5" for x in s], v["C1"]),
        ("C2. A cache hit is fast (median `duration_ms`)", "≤ 50 ms", [f"{x['C2']} ms" for x in s], v["C2"]),
        ("C3. A cache hit returns the same answer", "5 of 5", [f"{x['C3']}/5" for x in s], v["C3"]),
        ("C4. A failed run is never saved", "3 of 3", [f"{x['C4']}/3" for x in s], v["C4"]),
        ("C5. Every request leaves exactly one log record", "100% of requests",
         [f"{x['C5'][0]}/{x['C5'][2]} records, {x['C5'][1]} complete" for x in s], v["C5"]),
    ]
    stamp = dt.datetime.now()
    lines = [
        f"# Capstone run log — {args.label}",
        "",
        f"- Produced by: `run_capstone.py::main` · {stamp.strftime('%Y-%m-%d %H:%M')}",
        f"- Service: {args.url} (`serve.py::ask`, `cache.py`) · {len(trials)} trials, "
        f"cache emptied before each, {args.pause}s pause between",
        "- Scored from the responses and from the server's own log, read back with `GET /logs`",
        "",
        "| Criterion | Target | " + " | ".join(f"Run {i}" for i in range(1, len(trials) + 1)) + " | Verdict |",
        "|---|---|" + "---|" * len(trials) + "---|",
    ]
    for name, target, runs, ok in rows:
        lines.append(f"| {name} | {target} | " + " | ".join(runs) + f" | {mark(ok)} |")
    lines += ["", "Hit durations (ms) per trial: " +
              "; ".join(f"run {i}: {t['hit_ms']}" for i, t in enumerate(trials, 1)), ""]

    t1 = trials[0]
    recs = t1["records"]
    lines += ["## Real output, run 1", "",
              "Log records are exactly as the server wrote them (`serve.py::log_run`, read via "
              "`serve.py::logs`). Responses are trimmed to the fields scored.", "",
              "**C1 and C2** — the 5 second sends (log records 6–10):", "", "```json"]
    lines += [json.dumps(r, ensure_ascii=False) for r in recs[5:10]]
    lines += ["```", "", "**C3** — first and second response for each query:", "", "```json"]
    by_q = {}
    for x in t1["sent"]:
        if x["kind"] in ("first", "second"):
            by_q.setdefault(x["query"], []).append(
                {k: x[k] for k in ("kind", "cache_hit", "selected_item", "fit_card")})
    lines += [json.dumps({q: pair}, ensure_ascii=False) for q, pair in by_q.items()]
    lines += ["```", "", "**C4** — each failing query sent twice (log records 11–16):", "", "```json"]
    lines += [json.dumps(r, ensure_ascii=False) for r in recs[10:16]]
    lines += ["```", "",
              f"**C5** — {t1['scores']['C5'][2]} requests sent, {t1['scores']['C5'][0]} new log "
              f"records, {t1['scores']['C5'][1]} with all of {', '.join(LOG_FIELDS)}. "
              "The 2 bad requests (log records 17–18):", "", "```json"]
    lines += [json.dumps(r, ensure_ascii=False) for r in recs[16:18]]
    lines += ["```", ""]

    config.RESULTS_DIR.mkdir(exist_ok=True)
    base = config.RESULTS_DIR / f"capstone_{stamp.strftime('%Y-%m-%d_%H%M')}_{args.label}"
    base.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    base.with_suffix(".json").write_text(json.dumps(trials, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n".join(lines[6:6 + len(rows) + 2]))
    print(f"\nWrote {base.with_suffix('.md').relative_to(config.ROOT)} (and .json)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--label", required=True)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--pause", type=int, default=65)
    args = parser.parse_args()

    token = os.getenv("CACHE_ADMIN_TOKEN")
    if not token:
        sys.exit("Set CACHE_ADMIN_TOKEN first (the same value as on the server).")
    headers = {"X-Admin-Token": token}

    print(f"Waking {args.url} (up to a minute if it was asleep) ...")
    requests.get(f"{args.url}/health", timeout=120).raise_for_status()
    if requests.get(f"{args.url}/logs", headers=headers, timeout=30).status_code != 200:
        sys.exit("GET /logs refused the token. Is CACHE_ADMIN_TOKEN the same as on the server?")

    trials = []
    for i in range(1, args.trials + 1):
        if i > 1:
            print(f"Waiting {args.pause}s for the model rate limit ...")
            time.sleep(args.pause)
        print(f"Trial {i} ...")
        t = run_trial(args.url, headers)
        trials.append(t)
        print(f"  {t['scores']}")

    write_report(trials, args)


if __name__ == "__main__":
    main()
