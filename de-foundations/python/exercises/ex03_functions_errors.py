"""Python 03 exercises. Replace each `raise NotImplementedError` with your code."""

from datetime import date, datetime


def parse_amount(raw: str | None) -> float | None:
    """Turn messy money text into a float, or None if it isn't a number.
    ' 1,299.50 ' -> 1299.5 ; '$45' -> 45.0 ; '' / 'N/A' / 'unknown' / None -> None.
    Use try/except ValueError, not a list of bad words."""
    raise NotImplementedError


def safe_divide(a: float, b: float) -> float | None:
    """a / b, or None when b is 0."""
    raise NotImplementedError


def parse_date(raw: str) -> date:
    """Accept 'YYYY-MM-DD' or 'DD/MM/YYYY' (surrounding spaces allowed) and return a date.
    Anything else: raise ValueError with a message that includes the bad input."""
    raise NotImplementedError


def clean_email(raw: str | None) -> str | None:
    """Strip and lowercase. Return None if empty, or if it doesn't have exactly one '@'
    with something before it and a '.' somewhere after it."""
    raise NotImplementedError


def parse_quantity(raw: str) -> int:
    """int(raw) after stripping. Raise ValueError if it isn't a whole number or is <= 0."""
    raise NotImplementedError


def chunk(items: list, size: int) -> list[list]:
    """Split into consecutive lists of `size` (last one may be shorter).
    chunk([1,2,3,4,5], 2) -> [[1,2],[3,4],[5]]. Raise ValueError if size < 1."""
    raise NotImplementedError


def split_valid(raw_quantities: list[str]) -> tuple[list[int], list[str]]:
    """Use parse_quantity on each. Return (good_values, bad_raw_strings), both in input order.
    Bad rows are kept, not thrown away — so they can be reported."""
    raise NotImplementedError
