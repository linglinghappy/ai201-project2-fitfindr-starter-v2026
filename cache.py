"""
Capstone: the response cache in front of serve.py's /ask route.

When the same request comes in again, serve.py returns the saved session
instead of running the agent: no parsing, no MCP search, no model calls.

    key = cache.make_key(query, wardrobe)
    session = cache.get(key)        # None on a miss
    cache.put(key, session)         # after a run; skipped if it failed

The rules, from the README's The Shape:

  • The key is the query (lower case, extra spaces removed) plus the wardrobe.
    A different wardrobe needs a different outfit, so it has to be in the key.
  • An entry expires after config.RESPONSE_CACHE_TTL_S seconds.
  • At most config.RESPONSE_CACHE_MAX entries; when full, the one used longest
    ago is dropped (LRU).
  • A session with session["error"] set is never saved, so one failure doesn't
    keep being served after the problem is gone.

It lives in this process's memory. A restart (or Render waking up from
sleep) starts it empty.
"""

import copy
import hashlib
import json
import threading
import time
from collections import OrderedDict

import config

_entries: OrderedDict = OrderedDict()  # key -> (saved_at, session)
_lock = threading.Lock()


def make_key(query: str, wardrobe: dict) -> str:
    normal_query = " ".join(query.lower().split())
    blob = json.dumps([normal_query, wardrobe], sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def get(key: str) -> dict | None:
    """The saved session for this key, or None if there isn't a fresh one."""
    with _lock:
        entry = _entries.get(key)
        if entry is None:
            return None
        saved_at, session = entry
        if time.monotonic() - saved_at > config.RESPONSE_CACHE_TTL_S:
            del _entries[key]
            return None
        _entries.move_to_end(key)  # most recently used
        return copy.deepcopy(session)


def put(key: str, session: dict) -> bool:
    """Save a finished session. Returns False if it wasn't saved (a failed run)."""
    if session.get("error"):
        return False
    with _lock:
        _entries[key] = (time.monotonic(), copy.deepcopy(session))
        _entries.move_to_end(key)
        while len(_entries) > config.RESPONSE_CACHE_MAX:
            _entries.popitem(last=False)  # least recently used
    return True


def clear() -> int:
    """Empty the cache. Returns how many entries were removed."""
    with _lock:
        count = len(_entries)
        _entries.clear()
    return count


def size() -> int:
    with _lock:
        return len(_entries)
