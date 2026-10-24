"""Check your SQL exercise answers against the reference solutions.

    python sql/check.py            # every exercise file
    python sql/check.py 03         # only sql/exercises/03_*.sql
    python sql/check.py 03 q4      # one question

It runs your query and the reference query against data/shop.db and compares
the results. Column names don't matter; column order, values and row count do.
Row order only matters when the question says "order by ...".
"""

import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "shop.db"
EXERCISES = ROOT / "sql" / "exercises"
SOLUTIONS = ROOT / "sql" / "solutions"
MARKER = re.compile(r"^--\s*@q(\d+)\b", re.MULTILINE)


def parse_blocks(text: str) -> dict[int, str]:
    """Split a file into {question_number: sql} using '-- @qN' marker lines."""
    blocks = {}
    matches = list(MARKER.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks[int(m.group(1))] = text[m.end():end]
    return blocks


def strip_comments(sql: str) -> str:
    lines = [ln for ln in sql.splitlines() if not ln.strip().startswith("--")]
    return "\n".join(lines).strip()


def normalise(rows):
    out = []
    for row in rows:
        out.append(tuple(round(v, 2) if isinstance(v, float) else v for v in row))
    return out


def run(con, sql):
    cur = con.execute(sql)
    return normalise(cur.fetchall()), len(cur.description or [])


def check_file(con, ex_path: Path, only: int | None) -> tuple[int, int, int]:
    sol_path = SOLUTIONS / ex_path.name
    mine = parse_blocks(ex_path.read_text(encoding="utf-8"))
    ref = parse_blocks(sol_path.read_text(encoding="utf-8"))
    passed = attempted = 0
    print(f"\n{ex_path.name}")
    for q, ref_sql in sorted(ref.items()):
        if only is not None and q != only:
            continue
        ordered = "@ordered" in ref_sql
        my_sql = strip_comments(mine.get(q, ""))
        if not my_sql:
            print(f"  q{q:<2}  .  not attempted")
            continue
        attempted += 1
        try:
            got, got_cols = run(con, my_sql)
        except sqlite3.Error as e:
            print(f"  q{q:<2}  x  SQL error: {e}")
            continue
        want, want_cols = run(con, strip_comments(ref_sql))
        if got_cols != want_cols:
            print(f"  q{q:<2}  x  you returned {got_cols} column(s), expected {want_cols}")
            continue
        a, b = (got, want) if ordered else (sorted(got, key=repr), sorted(want, key=repr))
        if a == b:
            passed += 1
            print(f"  q{q:<2}  ok")
            continue
        msg = f"you returned {len(got)} row(s), expected {len(want)}"
        if len(got) == len(want):
            if not ordered or sorted(got, key=repr) != sorted(want, key=repr):
                first_bad = next(i for i, (x, y) in enumerate(zip(a, b)) if x != y)
                msg = f"row {first_bad + 1}: got {a[first_bad]}, expected {b[first_bad]}"
            else:
                msg = "right rows, wrong order (re-read the ORDER BY in the question)"
        elif want:
            msg += f"; first expected row: {want[0]}"
        print(f"  q{q:<2}  x  {msg}")
    total = len(ref) if only is None else 1
    return passed, attempted, total


def main(argv: list[str]) -> None:
    if not DB.exists():
        sys.exit("data/shop.db is missing. Run:  python data/build_db.py")
    prefix = argv[0] if argv else ""
    only = int(argv[1].lstrip("qQ")) if len(argv) > 1 else None
    files = sorted(EXERCISES.glob(f"{prefix}*.sql"))
    if not files:
        sys.exit(f"No exercise file matches '{prefix}'")
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)  # read-only: you can't break the data
    totals = [0, 0, 0]
    for f in files:
        for i, n in enumerate(check_file(con, f, only)):
            totals[i] += n
    print(f"\n{totals[0]} passed / {totals[1]} attempted / {totals[2]} questions")
    if not argv:
        print(f"Phase 1 milestone: {totals[0]} of 60 SQL problems solved")


if __name__ == "__main__":
    main(sys.argv[1:])
