# Python 07 — DataFrames, data at scale, and file formats

Roadmap items: *pandas vs polars, chunked reads, memory profiling* and *File formats &
storage layout*. Time: ~8 hours. No auto-checker: the tasks are measurements you
record in your journal — that's the point.

```bash
pip install pandas polars pyarrow
```

## DataFrames in 10 lines

A DataFrame is a table in memory: named, typed columns.

```python
import pandas as pd
import sqlite3

con = sqlite3.connect("data/shop.db")
items = pd.read_sql("SELECT * FROM order_items", con)
items["net"] = items["quantity"] * items["unit_price"] * (1 - items["discount"])
items.groupby("product_id")["net"].sum().sort_values(ascending=False).head(3)
```

Every SQL idea has a DataFrame twin: `df[df.status == "completed"]` (WHERE),
`groupby().agg()` (GROUP BY), `merge` (JOIN), `sort_values` (ORDER BY),
`drop_duplicates` (DISTINCT). If you know SQL 01–05, pandas is mostly vocabulary.

## pandas vs polars

| | pandas | polars |
|---|---|---|
| maturity | 15 years, everywhere, every tutorial | newer, growing fast |
| engine | mostly single-threaded, eager | multi-threaded Rust, has a **lazy** mode with a query optimiser |
| memory | often 5–10× the file size | much closer to file size, Arrow-native |
| when | small/medium data, ecosystem compatibility, existing code | larger-than-comfortable data, speed, new projects |

```python
import polars as pl
(pl.scan_parquet("items.parquet")             # lazy: nothing read yet
   .filter(pl.col("discount") > 0)
   .group_by("product_id").agg(pl.col("quantity").sum())
   .collect())                                 # plan optimised, then executed
```

`scan_*` + `collect()` lets polars read only the columns and row groups it needs —
same idea as SQL 06's "read less data".

You need to *read* both and *defend a choice*. At Microsoft-stack jobs, the heavy
lifting happens in Spark/Fabric (Phase 3); pandas/polars are for scripts, tests and
small jobs.

## When data doesn't fit in memory

1. **Read less:** only the columns you need (`usecols=`, `columns=`), only the rows
   (filter at the source — SQL `WHERE`, Parquet predicate pushdown).
2. **Smaller types:** `category` dtype for repeated strings, `int32` instead of `int64`.
3. **Chunk:** `for chunk in pd.read_csv(path, chunksize=100_000): ...` — aggregate each
   chunk, combine partial results (like the generator pattern in lesson 05).
4. **Change tool:** polars lazy, DuckDB (SQL straight on files), Spark.

Measure, don't guess: `df.memory_usage(deep=True).sum()`, `tracemalloc`, `time.perf_counter()`.

## File formats

**Row vs columnar.** CSV/JSON store row after row. Parquet stores column after column.
Analytics queries read a few columns of many rows → columnar wins massively.

**Parquet internals** (interview favourite):
- file → **row groups** (e.g. ~128 MB each) → **column chunks** → pages
- each column chunk stores **statistics** (min, max, null count). A reader looking for
  `order_date >= '2025-12-01'` skips any row group whose max is earlier — **predicate pushdown**
- columns are **encoded** (dictionary, run-length) then **compressed** (`snappy` fast,
  `zstd` smaller, `gzip` legacy)
- the schema and types are stored in the file — no guessing "is '00123' a number?"

**Partitioning:** split a dataset into folders by a column:
```
orders/order_month=2025-11/part-0.parquet
orders/order_month=2025-12/part-0.parquet
```
A query filtering on `order_month` reads only matching folders (**partition pruning**).
Partition on a low-cardinality column you filter by (date). Partitioning on
`customer_id` creates millions of tiny folders.

**The small-file problem:** 100,000 files of 10 KB is far slower than 10 files of 100 MB —
each file has open/metadata overhead. Streaming and frequent appends cause it;
**compaction** (rewrite into bigger files) fixes it. You'll see `OPTIMIZE` do this on
Delta Lake in Phase 3.

## Tasks (write numbers in your journal)

1. Export `order_items` joined to `orders` to CSV, Parquet-snappy and Parquet-zstd
   (`df.to_parquet(path, compression="zstd")`). Compare file sizes.
2. Time reading only 2 columns from the CSV vs from the Parquet file.
3. Measure the DataFrame's memory with `memory_usage(deep=True)`; convert `status` and
   `channel` to `category` and measure again.
4. Rewrite the "revenue per product" aggregation using `read_csv(chunksize=500)` and
   check you get exactly the same numbers as the SQL in SQL 02 q6.
5. Write the dataset partitioned by month (`df.to_parquet("out", partition_cols=["month"])`),
   look at the folder tree, and read back a single month with polars.
6. `pyarrow.parquet.ParquetFile(path).metadata` — find the row groups and a column's min/max statistics.
