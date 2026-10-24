# Python 02 — Collections: lists, dicts, sets, tuples, comprehensions

**Goal:** hold and reshape many values — in data engineering a "row" is usually a
dict and a "table" is a list of dicts. Exercises: `ex02_collections.py`.

## list — ordered, changeable

```python
cities = ["Pune", "Dublin", "Austin"]
cities[0]          # "Pune"      (first, index 0)
cities[-1]         # "Austin"    (last)
cities[1:]         # ["Dublin", "Austin"]
cities.append("Berlin")
len(cities)        # 4
"Pune" in cities   # True
sorted(cities)     # new sorted list; cities.sort() sorts in place
```

## dict — key → value lookup

```python
row = {"order_id": 17, "status": "completed", "amount": 45.0}
row["status"]                  # "completed"
row.get("channel")             # None (no KeyError)
row.get("channel", "web")      # "web" default
row["channel"] = "mobile"      # add / overwrite
for key, value in row.items():
    print(key, value)
```

Keys must be immutable (str, int, tuple). Lookups are fast no matter the size —
that's why dicts are the go-to for "have I seen this id before?".

## set — unique values, fast membership

```python
seen = set()
seen.add(5); seen.add(5)     # still one element
{1, 2, 3} & {2, 3, 4}        # {2, 3}  intersection  (SQL INTERSECT)
{1, 2, 3} - {2}              # {1, 3}  difference    (SQL EXCEPT)
```

## tuple — fixed, unchangeable sequence

```python
point = (17.38, 78.48)
lat, lon = point             # unpacking
```

Use tuples as composite dict keys: `totals[(year, channel)] += 1`.

## Comprehensions — build a collection in one line

```python
amounts = [r["amount"] for r in rows]                          # map
completed = [r for r in rows if r["status"] == "completed"]    # filter
by_id = {r["order_id"]: r for r in rows}                       # dict comprehension
countries = {c["country"] for c in customers}                  # set comprehension
```

If it doesn't fit on one readable line, use a normal `for` loop.

## Sorting with a key

```python
rows.sort(key=lambda r: r["amount"], reverse=True)              # biggest first
sorted(rows, key=lambda r: (r["country"], -r["amount"]))        # country asc, amount desc
```

`lambda r: r["amount"]` is a tiny unnamed function: "given a row, sort by its amount".

## GROUP BY in plain Python

You'll write this pattern constantly before you reach for pandas:

```python
from collections import defaultdict, Counter

totals = defaultdict(float)           # missing keys start at 0.0
for r in rows:
    totals[r["channel"]] += r["amount"]

Counter(r["status"] for r in rows)    # {'completed': 1615, 'cancelled': 171, ...}
Counter(words).most_common(3)
```

## Mutability trap

```python
a = [1, 2]
b = a           # b is the SAME list, not a copy
b.append(3)
a               # [1, 2, 3]  surprise
c = a.copy()    # real (shallow) copy
```

And never use a mutable default argument: `def f(rows=[])` shares one list across
all calls. Use `def f(rows=None):` and then `if rows is None: rows = []` inside.

## Exercises

`python python/check.py ex02`
