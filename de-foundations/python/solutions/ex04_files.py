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
    return name.strip().lower().replace(" ", "_")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a CSV with the csv module, normalising every header with normalise_header.
    Skip rows where every value is empty."""
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = [normalise_header(h) for h in next(reader)]
        rows = []
        for values in reader:
            if all(v.strip() == "" for v in values):
                continue
            rows.append(dict(zip(header, values)))
    return rows


def clean_customer(row: dict[str, str]) -> dict | None:
    """Turn one raw row (normalised headers) into a clean record, or None if it can't be used.
    Output keys: customer_id (int), first_name, last_name (stripped, Title Case),
    email (clean_email), signup_date (ISO string 'YYYY-MM-DD'), lifetime_value (float or None).
    Return None if customer_id is not an integer or signup_date can't be parsed."""
    try:
        cid = int(row["customer_id"])
        signup = parse_date(row["signup_date"]).isoformat()
    except (ValueError, KeyError):
        return None
    return {
        "customer_id": cid,
        "first_name": row["first_name"].strip().title(),
        "last_name": row["last_name"].strip().title(),
        "email": clean_email(row["email"]),
        "signup_date": signup,
        "lifetime_value": parse_amount(row["lifetime_value"]),
    }


def clean_file(src: Path, dest: Path) -> dict[str, int]:
    """Read src, clean every row, drop rejects, and drop duplicate customer_ids (keep the FIRST).
    Write the clean rows to dest as CSV (columns in clean_customer's key order; None -> empty),
    creating dest's folder if needed. Return counts:
    {"read": rows read, "rejected": unusable rows, "duplicates": dropped dups, "written": rows written}"""
    rows = read_csv_rows(src)
    seen: set[int] = set()
    out, rejected, dups = [], 0, 0
    for r in rows:
        c = clean_customer(r)
        if c is None:
            rejected += 1
        elif c["customer_id"] in seen:
            dups += 1
        else:
            seen.add(c["customer_id"])
            out.append(c)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fields = ["customer_id", "first_name", "last_name", "email", "signup_date", "lifetime_value"]
    with open(dest, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for c in out:
            w.writerow({k: ("" if v is None else v) for k, v in c.items()})
    return {"read": len(rows), "rejected": rejected, "duplicates": dups, "written": len(out)}


def flatten_event(event: dict, parent: str = "", sep: str = "_") -> dict:
    """Flatten nested dicts into one level: {"user": {"id": 3}, "type": "x"} -> {"user_id": 3, "type": "x"}.
    Works for any depth. An empty nested dict produces no keys."""
    flat = {}
    for k, v in event.items():
        name = f"{parent}{sep}{k}" if parent else k
        if isinstance(v, dict):
            flat.update(flatten_event(v, name, sep))
        else:
            flat[name] = v
    return flat


def load_events(path: Path) -> list[dict]:
    """Read the JSON array at path and return every event flattened with flatten_event."""
    return [flatten_event(e) for e in json.loads(Path(path).read_text(encoding="utf-8"))]
