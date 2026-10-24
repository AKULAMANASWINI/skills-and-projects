from ex02_collections import (dedupe_latest, flatten, index_by_id, missing_ids, top_n, total_by,
                              unique_sorted, word_counts)

ROWS = [
    {"order_id": 1, "customer_id": 7, "channel": "web", "amount": 45.0},
    {"order_id": 2, "customer_id": 9, "channel": "store", "amount": 30.0},
    {"order_id": 3, "customer_id": 7, "channel": "web", "amount": 75.5},
    {"order_id": 4, "customer_id": 2, "channel": "mobile", "amount": 0.1},
    {"order_id": 5, "customer_id": 2, "channel": "mobile", "amount": 0.2},
]


def test_unique_sorted():
    assert unique_sorted([3, 1, 3, 2]) == [1, 2, 3]
    assert unique_sorted([]) == []


def test_word_counts():
    assert word_counts("a B a") == {"a": 2, "b": 1}
    assert word_counts("  ") == {}


def test_total_by():
    assert total_by(ROWS, "channel", "amount") == {"web": 120.5, "store": 30.0, "mobile": 0.3}
    assert total_by(ROWS, "customer_id", "amount")[7] == 120.5


def test_top_n():
    totals = {"web": 120.5, "store": 30.0, "mobile": 30.0, "app": 1.0}
    assert top_n(totals, 3) == [("web", 120.5), ("mobile", 30.0), ("store", 30.0)]
    assert top_n(totals, 0) == []


def test_index_by_id():
    rows = [{"id": 1, "v": "old"}, {"id": 2, "v": "x"}, {"id": 1, "v": "new"}]
    idx = index_by_id(rows, "id")
    assert len(idx) == 2
    assert idx[1]["v"] == "new"


def test_missing_ids():
    assert missing_ids([5, 1, 2, 3, 3], [2, 9]) == [1, 3, 5]
    assert missing_ids([1], [1]) == []


def test_flatten():
    assert flatten([[1, 2], [3], []]) == [1, 2, 3]


def test_dedupe_latest():
    rows = [
        {"id": 2, "ts": "2025-01-02", "v": "b1"},
        {"id": 1, "ts": "2025-03-01", "v": "a2"},
        {"id": 1, "ts": "2025-01-01", "v": "a1"},
        {"id": 2, "ts": "2025-02-01", "v": "b2"},
    ]
    assert [r["v"] for r in dedupe_latest(rows, "id", "ts")] == ["a2", "b2"]
