#!/usr/bin/env python3
"""
Capstone: measure what one FitFindr run costs.

    PORT=5050 AI201_CACHE=0 python serve.py        # terminal A
    python measure_cost.py                         # terminal B

Sends 10 different queries to /ask (each one finds a different listing, so
none of them can be a cache hit), then reads those 10 records back from
logs/runs.jsonl and averages them: tokens, model calls, total time, and the
time of each stage. Then it sends 2 requests that should fail (an empty body
and a query that matches nothing), so the log has failures to show too. The
failures are not part of the averages.

The server must run on this machine with AI201_CACHE=0, so the old
prompt-level cache in generate.py can't answer for the model.

Writes results/cost_<date>.md.
"""

import argparse
import datetime as dt
import json
import statistics

import requests

import config

QUERIES = [
    "vintage graphic tee under $30",
    "90s track jacket size M",
    "corduroy pants under $40",
    "platform sneakers under $50",
    "leather belt",
    "linen blazer under $45",
    "chelsea boots",
    "bucket hat",
    "knit cardigan under $40",
    "denim shorts under $30",
]
LOG_FILE = config.ROOT / "logs" / "runs.jsonl"
STAGES = ["parse_query", "search_listings", "suggest_outfit", "create_fit_card"]


def read_log() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    return [json.loads(line) for line in LOG_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:5050")
    args = parser.parse_args()

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        raise SystemExit(f"Nothing answering at {args.url}. Start it: PORT=5050 AI201_CACHE=0 python serve.py")

    before = len(read_log())

    print(f"Sending {len(QUERIES)} queries to {args.url}/ask ...")
    for i, query in enumerate(QUERIES, 1):
        body = requests.post(f"{args.url}/ask", json={"query": query}, timeout=120).json()
        print(f"  [{i:2}/{len(QUERIES)}] cache_hit={body.get('cache_hit')}  "
              f"{(body.get('selected_item') or {}).get('id')}  {query}")

    print("Sending 2 requests that should fail ...")
    r1 = requests.post(f"{args.url}/ask", data="", headers={"Content-Type": "application/json"}, timeout=30)
    r2 = requests.post(f"{args.url}/ask", json={"query": "purple ballgown size XXS under $5"}, timeout=120)
    print(f"  empty body -> {r1.status_code};  no-match query -> {r2.status_code}, "
          f"error: {(r2.json().get('error') or '')[:50]}...")

    new = read_log()[before:]
    runs = new[:len(QUERIES)]
    failures = new[len(QUERIES):]
    if len(runs) != len(QUERIES):
        raise SystemExit(f"Expected {len(QUERIES)} new log records, found {len(runs)}. "
                         f"Is the server running on this machine?")
    hits = [r for r in runs if r["cache_hit"]]
    if hits:
        print(f"!! {len(hits)} of the 10 were cache hits. Restart the server and run again.")

    def avg(field):
        return statistics.mean(r[field] for r in runs)

    def stage_avg(stage):
        values = [r["timings_ms"][stage] for r in runs if r.get("timings_ms") and stage in r["timings_ms"]]
        return statistics.mean(values) if values else 0

    total_ms = avg("duration_ms")
    lines = [
        "# Cost of one run",
        "",
        f"- Produced by: `measure_cost.py::main` · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- Server: {args.url}, response cache cold (10 different queries), `AI201_CACHE=0`",
        f"- Model: `{config.MODEL}`, temperature {config.TEMPERATURE}",
        "- Numbers are read from `logs/runs.jsonl`; tokens are what the Gemini API reported "
        "(`generate.py::token_counts`).",
        "",
        "## Averages over 10 runs (all cache misses)",
        "",
        "| Measure | Average | Min | Max |",
        "|---|---|---|---|",
    ]
    for field in ["prompt_tokens", "output_tokens", "model_calls", "duration_ms"]:
        values = [r[field] for r in runs]
        lines.append(f"| {field} | {statistics.mean(values):.1f} | {min(values)} | {max(values)} |")
    total_tokens = [r["prompt_tokens"] + r["output_tokens"] for r in runs]
    lines.append(f"| total tokens | {statistics.mean(total_tokens):.1f} | {min(total_tokens)} | {max(total_tokens)} |")

    lines += ["", "## Where the time goes (latency breakdown, averages)", "",
              "| Stage | Average ms | Share of total |", "|---|---|---|"]
    for stage in STAGES:
        ms = stage_avg(stage)
        lines.append(f"| {stage} | {ms:.0f} | {ms / total_ms:.0%} |")
    lines.append(f"| **total (duration_ms)** | **{total_ms:.0f}** | |")

    lines += ["", "## The 10 runs", "", "```json"]
    lines += [json.dumps(r, ensure_ascii=False) for r in runs]
    lines += ["```", "", "## The 2 failures (not in the averages)", "", "```json"]
    lines += [json.dumps(r, ensure_ascii=False) for r in failures]
    lines += ["```", ""]

    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / f"cost_{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines[8:lines.index("## The 10 runs")]))
    print(f"Wrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
