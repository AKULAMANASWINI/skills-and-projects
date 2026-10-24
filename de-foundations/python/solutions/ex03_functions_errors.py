"""Python 03 exercises. Replace each `raise NotImplementedError` with your code."""

from datetime import date, datetime


def parse_amount(raw: str | None) -> float | None:
    """Turn messy money text into a float, or None if it isn't a number.
    ' 1,299.50 ' -> 1299.5 ; '$45' -> 45.0 ; '' / 'N/A' / 'unknown' / None -> None.
    Use try/except ValueError, not a list of bad words."""
    if raw is None:
        return None
    cleaned = raw.strip().replace(",", "").replace("$", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def safe_divide(a: float, b: float) -> float | None:
    """a / b, or None when b is 0."""
    try:
        return a / b
    except ZeroDivisionError:
        return None


def parse_date(raw: str) -> date:
    """Accept 'YYYY-MM-DD' or 'DD/MM/YYYY' (surrounding spaces allowed) and return a date.
    Anything else: raise ValueError with a message that includes the bad input."""
    text = raw.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"unrecognised date: {raw!r}")


def clean_email(raw: str | None) -> str | None:
    """Strip and lowercase. Return None if empty, or if it doesn't have exactly one '@'
    with something before it and a '.' somewhere after it."""
    if raw is None:
        return None
    e = raw.strip().lower()
    if e.count("@") != 1:
        return None
    local, domain = e.split("@")
    if not local or "." not in domain:
        return None
    return e


def parse_quantity(raw: str) -> int:
    """int(raw) after stripping. Raise ValueError if it isn't a whole number or is <= 0."""
    q = int(raw.strip())
    if q <= 0:
        raise ValueError(f"quantity must be positive, got {q}")
    return q


def chunk(items: list, size: int) -> list[list]:
    """Split into consecutive lists of `size` (last one may be shorter).
    chunk([1,2,3,4,5], 2) -> [[1,2],[3,4],[5]]. Raise ValueError if size < 1."""
    if size < 1:
        raise ValueError("size must be >= 1")
    return [items[i:i + size] for i in range(0, len(items), size)]


def split_valid(raw_quantities: list[str]) -> tuple[list[int], list[str]]:
    """Use parse_quantity on each. Return (good_values, bad_raw_strings), both in input order.
    Bad rows are kept, not thrown away — so they can be reported."""
    good, bad = [], []
    for raw in raw_quantities:
        try:
            good.append(parse_quantity(raw))
        except ValueError:
            bad.append(raw)
    return good, bad
