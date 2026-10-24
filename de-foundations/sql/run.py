"""Run SQL against the practice database without installing anything.

    python sql/run.py "SELECT * FROM products LIMIT 5"
    python sql/run.py                      # interactive: type a query, end it with ;

Type .tables to list tables, .schema orders to see a table's columns, .quit to leave.
"""

import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "shop.db"


def show(con, sql: str, max_rows: int = 50) -> None:
    try:
        cur = con.execute(sql)
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return
    if cur.description is None:
        print("OK")
        return
    cols = [d[0] for d in cur.description]
    rows = cur.fetchmany(max_rows + 1)
    cells = [[("NULL" if v is None else str(v)) for v in r] for r in rows[:max_rows]]
    widths = [max(len(c), *(len(r[i]) for r in cells)) if cells else len(c) for i, c in enumerate(cols)]
    print(" | ".join(c.ljust(w) for c, w in zip(cols, widths)))
    print("-+-".join("-" * w for w in widths))
    for r in cells:
        print(" | ".join(v.ljust(w) for v, w in zip(r, widths)))
    more = " (showing first %d)" % max_rows if len(rows) > max_rows else ""
    print(f"({len(cells)} row{'s' if len(cells) != 1 else ''}){more}")


def repl(con) -> None:
    buf = []
    while True:
        try:
            line = input("sql> " if not buf else "...> ")
        except EOFError:
            break
        cmd = line.strip()
        if not buf and cmd in (".quit", ".exit"):
            break
        if not buf and cmd == ".tables":
            show(con, "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            continue
        if not buf and cmd.startswith(".schema"):
            table = cmd.split(maxsplit=1)[1] if " " in cmd else ""
            show(con, f"SELECT name AS column_name, type, \"notnull\", pk FROM pragma_table_info('{table}')")
            continue
        buf.append(line)
        if cmd.endswith(";"):
            show(con, "\n".join(buf))
            buf = []


if __name__ == "__main__":
    if not DB.exists():
        sys.exit("data/shop.db is missing. Run:  python data/build_db.py")
    connection = sqlite3.connect(DB)
    if len(sys.argv) > 1:
        show(connection, " ".join(sys.argv[1:]))
    else:
        repl(connection)
