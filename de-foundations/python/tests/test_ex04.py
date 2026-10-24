import csv
from pathlib import Path

from ex04_files import clean_customer, clean_file, flatten_event, load_events, normalise_header, read_csv_rows

RAW = Path(__file__).resolve().parents[2] / "data" / "raw"


def test_normalise_header():
    assert normalise_header(" First Name") == "first_name"
    assert normalise_header("EMAIL") == "email"
    assert normalise_header("last_name ") == "last_name"


def test_read_csv_rows():
    rows = read_csv_rows(RAW / "customers_export.csv")
    assert len(rows) == 63, "60 customers + 1 duplicate + 2 bad rows; the blank row must be skipped"
    assert set(rows[0]) == {"customer_id", "first_name", "last_name", "email", "signup_date", "lifetime_value"}
    assert all(isinstance(v, str) for v in rows[0].values())


def test_clean_customer():
    raw = {"customer_id": "12", "first_name": "  PRIYA ", "last_name": "reddy",
           "email": " P@X.COM", "signup_date": "05/03/2024", "lifetime_value": "N/A"}
    assert clean_customer(raw) == {"customer_id": 12, "first_name": "Priya", "last_name": "Reddy",
                                   "email": "p@x.com", "signup_date": "2024-03-05", "lifetime_value": None}


def test_clean_customer_rejects():
    base = {"customer_id": "1", "first_name": "a", "last_name": "b", "email": "",
            "signup_date": "2024-01-01", "lifetime_value": "1"}
    assert clean_customer({**base, "customer_id": "C-61"}) is None
    assert clean_customer({**base, "signup_date": "March 3rd"}) is None


def test_clean_file(tmp_path):
    dest = tmp_path / "clean" / "customers.csv"
    stats = clean_file(RAW / "customers_export.csv", dest)
    assert stats == {"read": 63, "rejected": 2, "duplicates": 1, "written": 60}
    with open(dest, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 60
    assert list(rows[0]) == ["customer_id", "first_name", "last_name", "email", "signup_date", "lifetime_value"]
    assert all(len(r["signup_date"]) == 10 and r["signup_date"][4] == "-" for r in rows), "every date must be ISO"
    five = [r for r in rows if r["customer_id"] == "5"]
    assert len(five) == 1 and five[0]["email"] != "dup@example.com", "keep the FIRST row for a duplicate id"


def test_flatten_event():
    e = {"event_id": 1, "user": {"id": 3, "geo": {"country": "UK"}}, "props": {}, "type": "x"}
    assert flatten_event(e) == {"event_id": 1, "user_id": 3, "user_geo_country": "UK", "type": "x"}


def test_load_events():
    events = load_events(RAW / "events.json")
    assert len(events) == 25
    assert all("user_id" in e and "user" not in e for e in events)
