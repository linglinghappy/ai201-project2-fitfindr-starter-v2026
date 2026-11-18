# Capstone run log — after

- Produced by: `run_capstone.py::main` · 2026-11-17 21:51
- Service: https://fitfindr-hefr.onrender.com (`serve.py::ask`, `cache.py`) · 3 trials, cache emptied before each, 65s pause between
- Scored from the responses and from the server's own log, read back with `GET /logs`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. A cache hit doesn't call the model | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| C2. A cache hit is fast (median `duration_ms`) | ≤ 50 ms | 1 ms | 1 ms | 1 ms | MET |
| C3. A cache hit returns the same answer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| C4. A failed run is never saved | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| C5. Every request leaves exactly one log record | 100% of requests | 18/18 records, 18 complete | 18/18 records, 18 complete | 18/18 records, 18 complete | MET |

Hit durations (ms) per trial: run 1: [1, 0, 0, 1, 1]; run 2: [1, 0, 4, 0, 1]; run 3: [0, 1, 1, 1, 1]

## Real output, run 1

Log records are exactly as the server wrote them (`serve.py::log_run`, read via `serve.py::logs`). Responses are trimmed to the fields scored.

**C1 and C2** — the 5 second sends (log records 6–10):

```json
{"cache_hit": true, "cache_key": "71a70d4fe1c47a7f", "duration_ms": 1, "error": null, "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "vintage graphic tee under $30", "selected_item": "lst_002", "status": 200, "timestamp": "2026-11-18T03:47:12+00:00", "timings_ms": null, "wardrobe": "default"}
{"cache_hit": true, "cache_key": "1b9040f5cb3a023a", "duration_ms": 0, "error": null, "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "90s track jacket size M", "selected_item": "lst_004", "status": 200, "timestamp": "2026-11-18T03:47:12+00:00", "timings_ms": null, "wardrobe": "default"}
{"cache_hit": true, "cache_key": "37d8a549fc829de4", "duration_ms": 0, "error": null, "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "leather belt", "selected_item": "lst_014", "status": 200, "timestamp": "2026-11-18T03:47:12+00:00", "timings_ms": null, "wardrobe": "default"}
{"cache_hit": true, "cache_key": "b801f7b57bb9c113", "duration_ms": 1, "error": null, "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "chelsea boots", "selected_item": "lst_028", "status": 200, "timestamp": "2026-11-18T03:47:12+00:00", "timings_ms": null, "wardrobe": "default"}
{"cache_hit": true, "cache_key": "cfd99a7dfafb82ec", "duration_ms": 1, "error": null, "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "denim shorts under $30", "selected_item": "lst_016", "status": 200, "timestamp": "2026-11-18T03:47:12+00:00", "timings_ms": null, "wardrobe": "default"}
```

**C3** — first and second response for each query:

```json
{"vintage graphic tee under $30": [{"kind": "first", "cache_hit": false, "selected_item": "lst_002", "fit_card": "Channeling major 2000s energy with this butterfly print Y2K baby tee! ✨ Style it casual with baggy denim or lean into the grunge vibe with combat boots and trousers. Grab it on Depop for just $18! 🦋"}, {"kind": "second", "cache_hit": true, "selected_item": "lst_002", "fit_card": "Channeling major 2000s energy with this butterfly print Y2K baby tee! ✨ Style it casual with baggy denim or lean into the grunge vibe with combat boots and trousers. Grab it on Depop for just $18! 🦋"}]}
{"90s track jacket size M": [{"kind": "first", "cache_hit": false, "selected_item": "lst_004", "fit_card": "Channeling major 90s athletic energy with this navy and white striped track jacket! 🏃‍♀️💨 Grab it on Poshmark for just $45. Dress it down with baggy jeans or style it up with khaki trousers—tap the link to shop!"}, {"kind": "second", "cache_hit": true, "selected_item": "lst_004", "fit_card": "Channeling major 90s athletic energy with this navy and white striped track jacket! 🏃‍♀️💨 Grab it on Poshmark for just $45. Dress it down with baggy jeans or style it up with khaki trousers—tap the link to shop!"}]}
{"leather belt": [{"kind": "first", "cache_hit": false, "selected_item": "lst_014", "fit_card": "Scored this braided brown leather belt on thredUp for just $12! It adds the ultimate vintage touch to effortless earthy streetwear or a tough western-edge look. So versatile. 🤎✨"}, {"kind": "second", "cache_hit": true, "selected_item": "lst_014", "fit_card": "Scored this braided brown leather belt on thredUp for just $12! It adds the ultimate vintage touch to effortless earthy streetwear or a tough western-edge look. So versatile. 🤎✨"}]}
{"chelsea boots": [{"kind": "first", "cache_hit": false, "selected_item": "lst_028", "fit_card": "Scored these tan suede Chelsea boots for just $44 over on Poshmark! Obsessed with how easily they switch between chic earth tones and baggy vintage streetwear. Grab them in my closet before I change my mind!"}, {"kind": "second", "cache_hit": true, "selected_item": "lst_028", "fit_card": "Scored these tan suede Chelsea boots for just $44 over on Poshmark! Obsessed with how easily they switch between chic earth tones and baggy vintage streetwear. Grab them in my closet before I change my mind!"}]}
{"denim shorts under $30": [{"kind": "first", "cache_hit": false, "selected_item": "lst_016", "fit_card": "Scored these vintage cutoff denim shorts for just $24 on Poshmark! 👖✨ Rock them super casual with a white tank and chunky sneakers, or switch up the vibe with a black zip hoodie and combat boots. Shop this versatile staple in my closet now!"}, {"kind": "second", "cache_hit": true, "selected_item": "lst_016", "fit_card": "Scored these vintage cutoff denim shorts for just $24 on Poshmark! 👖✨ Rock them super casual with a white tank and chunky sneakers, or switch up the vibe with a black zip hoodie and combat boots. Shop this versatile staple in my closet now!"}]}
```

**C4** — each failing query sent twice (log records 11–16):

```json
{"cache_hit": false, "cache_key": "b1aa1c40e6fa33c6", "duration_ms": 4642, "error": "Nothing in the listings matched description 'purple ballgown', size XXS, under $5.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "purple ballgown size XXS under $5", "selected_item": null, "status": 200, "timestamp": "2026-11-18T03:47:17+00:00", "timings_ms": {"parse_query": 0, "search_listings": 4642}, "wardrobe": "default"}
{"cache_hit": false, "cache_key": "b1aa1c40e6fa33c6", "duration_ms": 3875, "error": "Nothing in the listings matched description 'purple ballgown', size XXS, under $5.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "purple ballgown size XXS under $5", "selected_item": null, "status": 200, "timestamp": "2026-11-18T03:47:21+00:00", "timings_ms": {"parse_query": 0, "search_listings": 3874}, "wardrobe": "default"}
{"cache_hit": false, "cache_key": "743b178e16d6aa53", "duration_ms": 3777, "error": "Nothing in the listings matched description 'gold sequin cape', under $3.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; raise the price ceiling above $3.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "gold sequin cape under $3", "selected_item": null, "status": 200, "timestamp": "2026-11-18T03:47:25+00:00", "timings_ms": {"parse_query": 0, "search_listings": 3777}, "wardrobe": "default"}
{"cache_hit": false, "cache_key": "743b178e16d6aa53", "duration_ms": 4148, "error": "Nothing in the listings matched description 'gold sequin cape', under $3.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; raise the price ceiling above $3.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "gold sequin cape under $3", "selected_item": null, "status": 200, "timestamp": "2026-11-18T03:47:30+00:00", "timings_ms": {"parse_query": 0, "search_listings": 4148}, "wardrobe": "default"}
{"cache_hit": false, "cache_key": "c050c1037db0e3b9", "duration_ms": 3576, "error": "Nothing in the listings matched description 'wedding dress', size XXS.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "wedding dress size XXS", "selected_item": null, "status": 200, "timestamp": "2026-11-18T03:47:34+00:00", "timings_ms": {"parse_query": 0, "search_listings": 3575}, "wardrobe": "default"}
{"cache_hit": false, "cache_key": "c050c1037db0e3b9", "duration_ms": 4072, "error": "Nothing in the listings matched description 'wedding dress', size XXS.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "wedding dress size XXS", "selected_item": null, "status": 200, "timestamp": "2026-11-18T03:47:38+00:00", "timings_ms": {"parse_query": 0, "search_listings": 4072}, "wardrobe": "default"}
```

**C5** — 18 requests sent, 18 new log records, 18 with all of timestamp, query, status, cache_hit, duration_ms, model_calls, prompt_tokens, output_tokens, error. The 2 bad requests (log records 17–18):

```json
{"cache_hit": false, "duration_ms": 0, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": null, "selected_item": null, "status": 400, "timestamp": "2026-11-18T03:47:38+00:00", "timings_ms": null, "wardrobe": null}
{"cache_hit": false, "duration_ms": 0, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": null, "selected_item": null, "status": 400, "timestamp": "2026-11-18T03:47:38+00:00", "timings_ms": null, "wardrobe": null}
```
