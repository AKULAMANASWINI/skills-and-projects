import pytest

from ex06_api import (PermanentError, TransientError, backoff_delays, classify_status, fetch_all_cursor,
                      fetch_all_pages, fetch_all_resilient, with_retry)


class FakeSleep:
    """Records requested delays instead of waiting."""
    def __init__(self):
        self.calls = []

    def __call__(self, seconds):
        self.calls.append(seconds)


def flaky(fail_times, exc=TransientError, result="ok"):
    state = {"calls": 0}

    def fn():
        state["calls"] += 1
        if state["calls"] <= fail_times:
            raise exc("nope")
        return result
    return fn, state


def test_classify_status():
    assert [classify_status(s) for s in (200, 204, 429, 500, 503, 400, 401, 404)] == \
        ["ok", "ok", "retry", "retry", "retry", "fail", "fail", "fail"]


def test_backoff_delays():
    assert backoff_delays(4) == [1.0, 2.0, 4.0]
    assert backoff_delays(1) == []
    assert backoff_delays(8, base=2, cap=30) == [2, 4, 8, 16, 30, 30, 30]


def test_with_retry_succeeds_after_failures():
    fn, state = flaky(2)
    sleep = FakeSleep()
    assert with_retry(fn, max_attempts=5, sleep=sleep) == "ok"
    assert state["calls"] == 3
    assert sleep.calls == [1.0, 2.0]


def test_with_retry_gives_up():
    fn, state = flaky(10)
    sleep = FakeSleep()
    with pytest.raises(TransientError):
        with_retry(fn, max_attempts=3, sleep=sleep)
    assert state["calls"] == 3
    assert sleep.calls == [1.0, 2.0], "no sleep after the final attempt"


def test_with_retry_does_not_retry_permanent():
    fn, state = flaky(1, exc=PermanentError)
    with pytest.raises(PermanentError):
        with_retry(fn, sleep=FakeSleep())
    assert state["calls"] == 1


def make_pages(n_rows, page_size):
    rows = [{"id": i} for i in range(1, n_rows + 1)]
    total = max(1, -(-n_rows // page_size))
    requested = []

    def fetch_page(page):
        requested.append(page)
        start = (page - 1) * page_size
        return {"data": rows[start:start + page_size], "page": page, "total_pages": total}
    return fetch_page, requested, rows


def test_fetch_all_pages():
    fetch, requested, rows = make_pages(23, 10)
    assert fetch_all_pages(fetch) == rows
    assert requested == [1, 2, 3]


def test_fetch_all_pages_empty():
    fetch, requested, _ = make_pages(0, 10)
    assert fetch_all_pages(fetch) == []


def test_fetch_all_cursor():
    pages = {None: ({"data": [1, 2], "next_cursor": "b"}),
             "b": {"data": [3], "next_cursor": "c"},
             "c": {"data": [], "next_cursor": None}}
    assert fetch_all_cursor(lambda c: pages[c]) == [1, 2, 3]


def test_fetch_all_resilient_retries_single_page():
    fetch, requested, rows = make_pages(25, 10)
    failures = {2: 2}  # page 2 fails twice

    def flaky_fetch(page):
        if failures.get(page, 0) > 0:
            failures[page] -= 1
            raise TransientError("503")
        return fetch(page)
    sleep = FakeSleep()
    assert fetch_all_resilient(flaky_fetch, sleep=sleep) == rows
    assert requested == [1, 2, 3], "only the failing page is retried, the extraction doesn't restart"
    assert sleep.calls == [1.0, 2.0]
