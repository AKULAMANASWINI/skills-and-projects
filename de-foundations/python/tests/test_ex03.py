from datetime import date

import pytest

from ex03_functions_errors import (chunk, clean_email, parse_amount, parse_date, parse_quantity,
                                   safe_divide, split_valid)


def test_parse_amount():
    assert parse_amount(" 1,299.50 ") == 1299.5
    assert parse_amount("$45") == 45.0
    assert parse_amount("0") == 0.0
    for junk in ["", "N/A", "unknown", None, "12abc"]:
        assert parse_amount(junk) is None, f"parse_amount({junk!r}) should be None"


def test_safe_divide():
    assert safe_divide(7, 2) == 3.5
    assert safe_divide(1, 0) is None


def test_parse_date():
    assert parse_date("2025-03-05") == date(2025, 3, 5)
    assert parse_date(" 05/03/2025 ") == date(2025, 3, 5)


def test_parse_date_rejects_garbage():
    with pytest.raises(ValueError) as err:
        parse_date("March 3rd")
    assert "March 3rd" in str(err.value), "the error message should include the bad input"


def test_clean_email():
    assert clean_email("  A.B@Example.COM ") == "a.b@example.com"
    for bad in [None, "", "  ", "no-at-sign.com", "a@@b.com", "@b.com", "a@localhost"]:
        assert clean_email(bad) is None, f"clean_email({bad!r}) should be None"


def test_parse_quantity():
    assert parse_quantity(" 3 ") == 3
    for bad in ["0", "-2", "1.5", "two"]:
        with pytest.raises(ValueError):
            parse_quantity(bad)


def test_chunk():
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert chunk([], 3) == []
    with pytest.raises(ValueError):
        chunk([1], 0)


def test_split_valid():
    good, bad = split_valid(["2", "x", "0", " 5", "-1"])
    assert good == [2, 5]
    assert bad == ["x", "0", "-1"]
