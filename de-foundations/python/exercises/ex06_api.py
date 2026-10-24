"""Python 06 exercises. Replace each `raise NotImplementedError` with your code.

No real network here: every function receives the thing that talks to the API as an argument,
so tests can pass fakes. That's the design lesson.
"""

import time
from collections.abc import Callable


class TransientError(Exception):
    """A failure worth retrying (timeout, HTTP 429, HTTP 5xx)."""


class PermanentError(Exception):
    """A failure not worth retrying (HTTP 400, 401, 403, 404)."""


def classify_status(status: int) -> str:
    """'ok' for 200-299; 'retry' for 429 and 500-599; 'fail' for everything else."""
    raise NotImplementedError


def backoff_delays(max_attempts: int, base: float = 1.0, cap: float = 30.0) -> list[float]:
    """The waits BETWEEN attempts for exponential backoff (no jitter): base, base*2, base*4, ...
    capped at `cap`. There are max_attempts - 1 waits. backoff_delays(4) -> [1.0, 2.0, 4.0]"""
    raise NotImplementedError


def with_retry(fn: Callable[[], object], max_attempts: int = 5, base: float = 1.0,
               sleep: Callable[[float], None] = time.sleep):
    """Call fn(). On TransientError wait (sleep(delay) using backoff_delays) and try again,
    up to max_attempts calls in total; if the last attempt fails, re-raise its TransientError.
    Any other exception (e.g. PermanentError) is raised immediately without retrying."""
    raise NotImplementedError


def fetch_all_pages(fetch_page: Callable[[int], dict]) -> list[dict]:
    """Page-number pagination. fetch_page(n) returns {"data": [...], "page": n, "total_pages": T}.
    Start at page 1, collect every page's data in order, stop after total_pages.
    An empty "data" list also means stop."""
    raise NotImplementedError


def fetch_all_cursor(fetch: Callable[[str | None], dict]) -> list[dict]:
    """Cursor pagination. fetch(cursor) returns {"data": [...], "next_cursor": "abc" or None}.
    First call uses cursor None. Keep going until next_cursor is None."""
    raise NotImplementedError


def fetch_all_resilient(fetch_page: Callable[[int], dict], max_attempts: int = 5,
                        sleep: Callable[[float], None] = time.sleep) -> list[dict]:
    """fetch_all_pages, but every single page request goes through with_retry
    (base delay 1.0). A flaky page must not restart the whole extraction."""
    raise NotImplementedError
