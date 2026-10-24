import dataclasses
import inspect
import itertools
import logging
import time
from datetime import date

import pytest

from ex05_idiomatic import OrderLine, batched, days_between, load_lines, running_total, timed


def test_orderline_from_row_and_net():
    line = OrderLine.from_row({"order_id": "1", "product_id": "9", "quantity": "3",
                               "unit_price": "19.99", "discount": "0.2"})
    assert line == OrderLine(1, 9, 3, 19.99, 0.2)
    assert line.net == 47.98
    assert OrderLine.from_row({"order_id": "1", "product_id": "9", "quantity": "1",
                               "unit_price": "5"}).discount == 0.0


def test_orderline_is_frozen():
    line = OrderLine(1, 2, 1, 5.0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        line.quantity = 99


def test_batched_is_a_generator():
    assert list(batched(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert inspect.isgeneratorfunction(batched), "use yield"
    assert list(batched([], 3)) == []
    first_two = list(itertools.islice(batched(itertools.count(), 3), 2))  # endless input
    assert first_two == [[0, 1, 2], [3, 4, 5]]


def test_running_total():
    assert list(running_total([1, 2, 3])) == [1, 3, 6]
    assert inspect.isgeneratorfunction(running_total), "use yield"


def test_days_between():
    assert days_between(date(2026, 10, 24), date(2028, 1, 24)) == 457
    assert days_between(date(2025, 1, 2), date(2025, 1, 1)) == -1


def test_timed_records_even_on_error():
    timings = {}
    with timed("ok", timings):
        time.sleep(0.01)
    assert timings["ok"] >= 0.01
    with pytest.raises(RuntimeError):
        with timed("boom", timings):
            raise RuntimeError("x")
    assert "boom" in timings


def test_load_lines_logs_one_warning(caplog):
    rows = [{"order_id": "1", "product_id": "2", "quantity": "1", "unit_price": "5"},
            {"order_id": "x", "product_id": "2", "quantity": "1", "unit_price": "5"},
            {"order_id": "3"}]
    with caplog.at_level(logging.WARNING):
        lines = load_lines(rows)
    assert len(lines) == 1
    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert len(warnings) == 1 and "2" in warnings[0].getMessage()
