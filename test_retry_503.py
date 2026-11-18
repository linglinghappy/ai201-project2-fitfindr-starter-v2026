#!/usr/bin/env python3
"""
Capstone: check the one improvement (retry a Gemini 503) without waiting for
Gemini to be busy.

    python test_retry_503.py

The after run on Render happened to get no 503s, so it can't show the retry
working. This replaces the Gemini client inside generate.py with a fake one
that fails on purpose, and checks three cases. No real model calls, no quota.
"""

import types

import generate

generate.time.sleep = lambda seconds: None      # don't actually wait
generate._wait_for_slot = lambda: None          # no per-minute pacing needed

ERROR_503 = Exception(
    "503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently "
    "experiencing high demand. Spikes in demand are usually temporary. Please try "
    "again later.', 'status': 'UNAVAILABLE'}}"
)


def fake_client(fail_times, error=ERROR_503):
    calls = {"n": 0}

    def generate_content(**kwargs):
        calls["n"] += 1
        if calls["n"] <= fail_times:
            raise error
        return types.SimpleNamespace(text="ok", usage_metadata=None)

    return types.SimpleNamespace(models=types.SimpleNamespace(generate_content=generate_content))


def attempts(fail_times, error=ERROR_503):
    client = fake_client(fail_times, error)
    generate._get_client = lambda: client
    before = generate.call_count()
    try:
        result = generate.generate("hi", cache=False)
    except generate.ModelUnavailable:
        result = "ModelUnavailable"
    return result, generate.call_count() - before


checks = [
    ("one 503, then success: retried, and the run succeeds",
     attempts(1), ("ok", 2)),
    ("503 every time: gives up after 5 tries, the same way as before (ModelUnavailable)",
     attempts(99), ("ModelUnavailable", 5)),
    ("a bad API key: not retried, fails on the first try",
     attempts(99, Exception("400 API key not valid")), ("ModelUnavailable", 1)),
]

failed = 0
for name, got, expected in checks:
    ok = got == expected
    failed += not ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}\n       got {got}, expected {expected}")
print(f"\n{len(checks) - failed} of {len(checks)} passed")
raise SystemExit(1 if failed else 0)
