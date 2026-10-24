"""Python 02 exercises. Replace each `raise NotImplementedError` with your code.

A "row" here is a dict like {"order_id": 1, "customer_id": 7, "channel": "web", "amount": 45.0}.
"""

from collections import defaultdict


def unique_sorted(values: list) -> list:
    """Unique values, sorted ascending. [3, 1, 3, 2] -> [1, 2, 3]"""
    return sorted(set(values))


def word_counts(text: str) -> dict[str, int]:
    """Count words, case-insensitive, split on whitespace. 'a B a' -> {'a': 2, 'b': 1}"""
    counts: dict[str, int] = {}
    for w in text.lower().split():
        counts[w] = counts.get(w, 0) + 1
    return counts


def total_by(rows: list[dict], key: str, value: str) -> dict:
    """GROUP BY key, SUM(value). Round each total to 2.
    total_by(rows, "channel", "amount") -> {"web": 120.5, "store": 30.0}"""
    totals: dict = defaultdict(float)
    for r in rows:
        totals[r[key]] += r[value]
    return {k: round(v, 2) for k, v in totals.items()}


def top_n(totals: dict[str, float], n: int) -> list[tuple[str, float]]:
    """The n largest (key, value) pairs, biggest first; ties broken by key ascending."""
    return sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def index_by_id(rows: list[dict], id_field: str) -> dict:
    """{id: row}. If an id appears twice, keep the LAST row seen (like an upsert)."""
    return {r[id_field]: r for r in rows}


def missing_ids(expected: list[int], loaded: list[int]) -> list[int]:
    """Reconciliation: ids in expected but not in loaded, sorted. (SQL EXCEPT.)"""
    return sorted(set(expected) - set(loaded))


def flatten(nested: list[list]) -> list:
    """[[1, 2], [3], []] -> [1, 2, 3] (one level deep). Try a comprehension."""
    return [x for inner in nested for x in inner]


def dedupe_latest(rows: list[dict], key: str, ts: str) -> list[dict]:
    """Keep one row per key: the one with the greatest ts (ISO strings compare correctly).
    Return them sorted by key. This is SQL 05's ROW_NUMBER() ... WHERE rn = 1 in Python."""
    best: dict = {}
    for r in rows:
        k = r[key]
        if k not in best or r[ts] > best[k][ts]:
            best[k] = r
    return [best[k] for k in sorted(best)]
