# Capstone run log — before

- Produced by: `run_capstone.py::main` · 2026-11-17 01:04
- Service: https://fitfindr-hefr.onrender.com (`serve.py::ask`, `cache.py`) · 3 trials, cache emptied before each, 65s pause between
- Scored from the responses and from the server's own log, read back with `GET /logs`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. A cache hit doesn't call the model | 5 of 5 | 5/5 | 4/5 | 5/5 | **MISSED** |
| C2. A cache hit is fast (median `duration_ms`) | ≤ 50 ms | 1 ms | 0.5 ms | 1 ms | MET |
| C3. A cache hit returns the same answer | 5 of 5 | 5/5 | 4/5 | 5/5 | **MISSED** |
| C4. A failed run is never saved | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| C5. Every request leaves exactly one log record | 100% of requests | 18/18 records, 18 complete | 18/18 records, 18 complete | 18/18 records, 18 complete | MET |

Hit durations (ms) per trial: run 1: [1, 1, 0, 0, 1]; run 2: [1, 0, 0, 1]; run 3: [1, 1, 1, 2, 0]

## Real output, run 1

Log records are exactly as the server wrote them (`serve.py::log_run`, read via `serve.py::logs`). Responses are trimmed to the fields scored.

**C1 and C2** — the 5 second sends (log records 6–10):

```json
{"cache_hit": true, "cache_key": "71a70d4fe1c47a7f", "duration_ms": 1, "error": null, "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "vintage graphic tee under $30", "selected_item": "lst_002", "status": 200, "timestamp": "2026-11-17T06:59:10+00:00", "timings_ms": null, "wardrobe": "default"}
{"cache_hit": true, "cache_key": "1b9040f5cb3a023a", "duration_ms": 1, "error": null, "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "90s track jacket size M", "selected_item": "lst_004", "status": 200, "timestamp": "2026-11-17T06:59:11+00:00", "timings_ms": null, "wardrobe": "default"}
{"cache_hit": true, "cache_key": "37d8a549fc829de4", "duration_ms": 0, "error": null, "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "leather belt", "selected_item": "lst_014", "status": 200, "timestamp": "2026-11-17T06:59:11+00:00", "timings_ms": null, "wardrobe": "default"}
{"cache_hit": true, "cache_key": "b801f7b57bb9c113", "duration_ms": 0, "error": null, "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "chelsea boots", "selected_item": "lst_028", "status": 200, "timestamp": "2026-11-17T06:59:11+00:00", "timings_ms": null, "wardrobe": "default"}
{"cache_hit": true, "cache_key": "cfd99a7dfafb82ec", "duration_ms": 1, "error": null, "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "denim shorts under $30", "selected_item": "lst_016", "status": 200, "timestamp": "2026-11-17T06:59:11+00:00", "timings_ms": null, "wardrobe": "default"}
```

**C3** — first and second response for each query:

```json
{"vintage graphic tee under $30": [{"kind": "first", "cache_hit": false, "selected_item": "lst_002", "fit_card": "Living out my early 2000s pop star dreams in this butterfly baby tee. 🦋✨ Grab this absolute steal for just $18 on my Depop before I change my mind and keep it! Two ways to style it: bagged-out denim for casual days, or combat boots and khaki trousers for an edgy contrast."}, {"kind": "second", "cache_hit": true, "selected_item": "lst_002", "fit_card": "Living out my early 2000s pop star dreams in this butterfly baby tee. 🦋✨ Grab this absolute steal for just $18 on my Depop before I change my mind and keep it! Two ways to style it: bagged-out denim for casual days, or combat boots and khaki trousers for an edgy contrast."}]}
{"90s track jacket size M": [{"kind": "first", "cache_hit": false, "selected_item": "lst_004", "fit_card": "Channeling peak 90s athletic energy with this navy and white stripe track jacket. Style it casually with baggy denim or layer it over a grey crewneck for that effortless streetwear look. Grab this gem for $45 over on my Poshmark closet!"}, {"kind": "second", "cache_hit": true, "selected_item": "lst_004", "fit_card": "Channeling peak 90s athletic energy with this navy and white stripe track jacket. Style it casually with baggy denim or layer it over a grey crewneck for that effortless streetwear look. Grab this gem for $45 over on my Poshmark closet!"}]}
{"leather belt": [{"kind": "first", "cache_hit": false, "selected_item": "lst_014", "fit_card": "Scored this gorgeous braided brown leather belt on thredUp for just $12! It's the ultimate finishing touch for everything from earthy streetwear to vintage Western fits. 🤎✨"}, {"kind": "second", "cache_hit": true, "selected_item": "lst_014", "fit_card": "Scored this gorgeous braided brown leather belt on thredUp for just $12! It's the ultimate finishing touch for everything from earthy streetwear to vintage Western fits. 🤎✨"}]}
{"chelsea boots": [{"kind": "first", "cache_hit": false, "selected_item": "lst_028", "fit_card": "Scored these tan suede Chelsea boots for just $44 on Poshmark! Obsessed with how they elevate my oversized crewneck streetwear looks and khaki trouser fits. Head to my closet to shop!"}, {"kind": "second", "cache_hit": true, "selected_item": "lst_028", "fit_card": "Scored these tan suede Chelsea boots for just $44 on Poshmark! Obsessed with how they elevate my oversized crewneck streetwear looks and khaki trouser fits. Head to my closet to shop!"}]}
{"denim shorts under $30": [{"kind": "first", "cache_hit": false, "selected_item": "lst_016", "fit_card": "Can't decide between a casual summer vibe or edgy warm-weather style with these high-waisted denim shorts? Grab this thrifted staple for just $24 over on my Poshmark closet and let's build both! ✨👖"}, {"kind": "second", "cache_hit": true, "selected_item": "lst_016", "fit_card": "Can't decide between a casual summer vibe or edgy warm-weather style with these high-waisted denim shorts? Grab this thrifted staple for just $24 over on my Poshmark closet and let's build both! ✨👖"}]}
```

**C4** — each failing query sent twice (log records 11–16):

```json
{"cache_hit": false, "cache_key": "b1aa1c40e6fa33c6", "duration_ms": 4485, "error": "Nothing in the listings matched description 'purple ballgown', size XXS, under $5.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "purple ballgown size XXS under $5", "selected_item": null, "status": 200, "timestamp": "2026-11-17T06:59:16+00:00", "timings_ms": {"parse_query": 0, "search_listings": 4484}, "wardrobe": "default"}
{"cache_hit": false, "cache_key": "b1aa1c40e6fa33c6", "duration_ms": 4816, "error": "Nothing in the listings matched description 'purple ballgown', size XXS, under $5.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "purple ballgown size XXS under $5", "selected_item": null, "status": 200, "timestamp": "2026-11-17T06:59:21+00:00", "timings_ms": {"parse_query": 0, "search_listings": 4816}, "wardrobe": "default"}
{"cache_hit": false, "cache_key": "743b178e16d6aa53", "duration_ms": 4388, "error": "Nothing in the listings matched description 'gold sequin cape', under $3.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; raise the price ceiling above $3.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "gold sequin cape under $3", "selected_item": null, "status": 200, "timestamp": "2026-11-17T06:59:25+00:00", "timings_ms": {"parse_query": 0, "search_listings": 4387}, "wardrobe": "default"}
{"cache_hit": false, "cache_key": "743b178e16d6aa53", "duration_ms": 4675, "error": "Nothing in the listings matched description 'gold sequin cape', under $3.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; raise the price ceiling above $3.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "gold sequin cape under $3", "selected_item": null, "status": 200, "timestamp": "2026-11-17T06:59:30+00:00", "timings_ms": {"parse_query": 0, "search_listings": 4675}, "wardrobe": "default"}
{"cache_hit": false, "cache_key": "c050c1037db0e3b9", "duration_ms": 4878, "error": "Nothing in the listings matched description 'wedding dress', size XXS.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "wedding dress size XXS", "selected_item": null, "status": 200, "timestamp": "2026-11-17T06:59:35+00:00", "timings_ms": {"parse_query": 0, "search_listings": 4878}, "wardrobe": "default"}
{"cache_hit": false, "cache_key": "c050c1037db0e3b9", "duration_ms": 4631, "error": "Nothing in the listings matched description 'wedding dress', size XXS.\nThings to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one.", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": "wedding dress size XXS", "selected_item": null, "status": 200, "timestamp": "2026-11-17T06:59:40+00:00", "timings_ms": {"parse_query": 0, "search_listings": 4631}, "wardrobe": "default"}
```

**C5** — 18 requests sent, 18 new log records, 18 with all of timestamp, query, status, cache_hit, duration_ms, model_calls, prompt_tokens, output_tokens, error. The 2 bad requests (log records 17–18):

```json
{"cache_hit": false, "duration_ms": 0, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": null, "selected_item": null, "status": 400, "timestamp": "2026-11-17T06:59:41+00:00", "timings_ms": null, "wardrobe": null}
{"cache_hit": false, "duration_ms": 0, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "model_calls": 0, "output_tokens": 0, "prompt_tokens": 0, "query": null, "selected_item": null, "status": 400, "timestamp": "2026-11-17T06:59:41+00:00", "timings_ms": null, "wardrobe": null}
```
