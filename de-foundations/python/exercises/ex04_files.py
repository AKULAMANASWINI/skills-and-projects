"""Python 04 exercises. Replace each `raise NotImplementedError` with your code.

Finish ex03 first: this file imports your parse_amount, parse_date and clean_email from it.
"""

import csv
import json
from pathlib import Path

from ex03_functions_errors import clean_email, parse_amount, parse_date


def normalise_header(name: str) -> str:
    """' First Name' -> 'first_name' ; 'EMAIL' -> 'email' ; 'Lifetime Value' -> 'lifetime_value'.
    Strip, lowercase, spaces -> underscores."""
    raise NotImplementedError


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a CSV with the csv module, normalising every header with normalise_header.
    Skip rows where every value is empty."""
    raise NotImplementedError


def clean_customer(row: dict[str, str]) -> dict | None:
    """Turn one raw row (normalised headers) into a clean record, or None if it can't be used.
    Output keys: customer_id (int), first_name, last_name (stripped, Title Case),
    email (clean_email), signup_date (ISO string 'YYYY-MM-DD'), lifetime_value (float or None).
    Return None if customer_id is not an integer or signup_date can't be parsed."""
    raise NotImplementedError


def clean_file(src: Path, dest: Path) -> dict[str, int]:
    """Read src, clean every row, drop rejects, and drop duplicate customer_ids (keep the FIRST).
    Write the clean rows to dest as CSV (columns in clean_customer's key order; None -> empty),
    creating dest's folder if needed. Return counts:
    {"read": rows read, "rejected": unusable rows, "duplicates": dropped dups, "written": rows written}"""
    raise NotImplementedError


def flatten_event(event: dict, parent: str = "", sep: str = "_") -> dict:
    """Flatten nested dicts into one level: {"user": {"id": 3}, "type": "x"} -> {"user_id": 3, "type": "x"}.
    Works for any depth. An empty nested dict produces no keys."""
    raise NotImplementedError


def load_events(path: Path) -> list[dict]:
    """Read the JSON array at path and return every event flattened with flatten_event."""
    raise NotImplementedError
