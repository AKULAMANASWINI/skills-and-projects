"""Python 05 exercises. Replace each `raise NotImplementedError` with your code."""

import logging
import time
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class OrderLine:
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    discount: float = 0.0

    @property
    def net(self) -> float:
        """quantity * unit_price * (1 - discount), rounded to 2."""
        return round(self.quantity * self.unit_price * (1 - self.discount), 2)

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "OrderLine":
        """Build from a dict of STRINGS (as csv gives you): convert each field to its type.
        'discount' may be missing -> 0.0."""
        return cls(
            order_id=int(row["order_id"]),
            product_id=int(row["product_id"]),
            quantity=int(row["quantity"]),
            unit_price=float(row["unit_price"]),
            discount=float(row.get("discount", 0.0)),
        )


def batched(items: Iterable, size: int) -> Iterator[list]:
    """GENERATOR: yield lists of up to `size` items from any iterable (even an endless one),
    without ever building the full list. Use `yield`."""
    batch = []
    for x in items:
        batch.append(x)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def running_total(values: Iterable[float]) -> Iterator[float]:
    """GENERATOR: yield the running sum after each value. [1, 2, 3] -> 1, 3, 6.
    (SQL 05's SUM() OVER (ORDER BY ...) in Python.)"""
    total = 0.0
    for v in values:
        total += v
        yield total


def days_between(a: date, b: date) -> int:
    """Whole days from a to b (negative if b is before a)."""
    return (b - a).days


@contextmanager
def timed(label: str, timings: dict[str, float]):
    """CONTEXT MANAGER: measure how long the `with` block takes and store it in timings[label]
    (seconds, from time.perf_counter). Must record even if the block raises."""
    start = time.perf_counter()
    try:
        yield
    finally:
        timings[label] = time.perf_counter() - start


def load_lines(rows: list[dict[str, str]]) -> list[OrderLine]:
    """Convert rows with OrderLine.from_row. Skip rows that fail (KeyError/ValueError) and
    log ONE warning at the end like 'skipped 2 bad rows' with log.warning — only if any were skipped."""
    out, skipped = [], 0
    for r in rows:
        try:
            out.append(OrderLine.from_row(r))
        except (KeyError, ValueError):
            skipped += 1
    if skipped:
        log.warning("skipped %d bad rows", skipped)
    return out
