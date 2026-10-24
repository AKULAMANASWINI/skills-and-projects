# SQL 07 — Data modeling: relational and dimensional

**Goal:** design tables, not just query them. This is the roadmap's "Relational
modeling fundamentals" and "Dimensional modeling & SCDs". Time: ~8 hours.
No auto-checker — modeling is judged by reasoning. Write designs in your journal
and the DDL in a file you can run.

## Part A — relational (how apps store data: OLTP)

### Keys

- **Primary key (PK):** uniquely identifies a row, never NULL. `customers.customer_id`.
- **Foreign key (FK):** a column pointing at another table's PK. `orders.customer_id → customers`.
  The database can refuse orphans (an order for a customer that doesn't exist) —
  **referential integrity**.
- **Natural key:** meaningful in the business (email, ISBN, employee number).
- **Surrogate key:** meaningless generated id (1, 2, 3 or a UUID). Warehouses use
  surrogates because natural keys change (people change emails) and collide across
  source systems.

### Constraints

`NOT NULL`, `UNIQUE`, `CHECK (quantity > 0)`, `PRIMARY KEY`, `FOREIGN KEY`. They are
data-quality rules the database enforces for free. Most warehouses *declare* but don't
*enforce* them — which is why Phase 2 has dbt tests.

### Normal forms (the short version that interviews want)

- **1NF:** each cell holds one value. No `"mouse, keyboard"` in a `products` column;
  no `item1, item2, item3` columns.
- **2NF:** in a table with a composite key, every non-key column depends on the
  *whole* key. In `order_items(order_id, product_id, product_name, quantity)`,
  `product_name` depends only on `product_id` → move it to `products`.
- **3NF:** non-key columns depend on the key and *nothing else*. If `customers` has
  `city` and `city_population`, population depends on city, not customer → split.

Mnemonic: *the key, the whole key, and nothing but the key.*

Normalising removes **update anomalies** (change a fact in one place). The cost is
joins. That trade-off flips in analytics — Part B.

## Part B — dimensional (how warehouses store data: OLAP), Kimball

Analysts ask "revenue by category by month by country". On a normalised schema that's
a 5-way join every time. Kimball's **star schema** reshapes data for that question:

- **Fact table** — measurements of a business event, at a declared **grain**.
  `fact_order_line`: one row per product per order. Columns: foreign keys to dimensions
  + numeric measures (`quantity`, `net_amount`).
- **Dimension tables** — the context you slice by: `dim_customer`, `dim_product`,
  `dim_date`. Wide, descriptive, denormalised (category lives *on* `dim_product`).

```
            dim_date
               |
dim_customer — fact_order_line — dim_product
               |
          dim_channel
```

### Grain first, always

Before columns, write one sentence: *"one row in this fact = one product line on one
order."* Every argument about a model ends up being about grain. Mixed grains in one
fact (some rows per order, some per line) is the worst modeling bug there is.

### Fact types

| type | one row = | example |
|---|---|---|
| transaction | one event | order line |
| periodic snapshot | state at regular intervals | inventory per product per day |
| accumulating snapshot | one process, updated as it moves | order: placed → shipped → delivered dates |

### Conformed dimensions

`dim_customer` is shared by the sales fact and the support-tickets fact, with the same
keys and meanings. That's what lets you join across business processes.

### Slowly Changing Dimensions (SCD)

A customer moves from Pune to London. What happens to last year's revenue by city?

| type | what you do | history |
|---|---|---|
| SCD 1 | overwrite city | lost — old orders now show London |
| SCD 2 | close the old row, insert a new row | kept — old orders keep Pune |
| SCD 3 | add a `previous_city` column | only one step back |

SCD 2 row layout:

| customer_sk | customer_id | city | valid_from | valid_to | is_current |
|---|---|---|---|---|---|
| 101 | 42 | Pune | 2024-03-01 | 2025-05-10 | 0 |
| 187 | 42 | London | 2025-05-10 | 9999-12-31 | 1 |

The fact table stores `customer_sk` (surrogate), so each order points at the version
that was true *when it happened*. Point-in-time lookup:

```sql
JOIN dim_customer d
  ON d.customer_id = o.customer_id
 AND o.order_date >= d.valid_from AND o.order_date < d.valid_to
```

You'll implement SCD 2 for real with dbt snapshots in Phase 2.

## Tasks

1. Is our `shop.db` in 3NF? Find one column on `order_items` that *looks* like a 2NF
   violation (`unit_price`) and argue why it's correct to keep it there.
2. Write the grain sentence and column list for `fact_order_line`, `dim_customer`,
   `dim_product`, `dim_date`.
3. Write `CREATE TABLE … AS SELECT …` statements that build `dim_product` and
   `fact_order_line` from `shop.db` (run them in a copy: `cp data/shop.db data/model.db`
   and edit `sql/run.py`'s DB path, or open model.db in DBeaver).
4. Build `dim_date` for 2024–2025 with a recursive CTE:
   `WITH RECURSIVE d(day) AS (SELECT '2024-01-01' UNION ALL SELECT date(day, '+1 day') FROM d WHERE day < '2025-12-31') …`
   Add year, month, weekday name, is_weekend.
5. Answer "net revenue by category by quarter, completed orders only" using only your
   star tables. Compare to the same number from the raw tables — they must match
   exactly. If they don't, you have a grain bug.
6. Sketch an SCD 2 `dim_customer` and write the SQL that, given a staging table of
   today's customer snapshot, (a) closes changed rows and (b) inserts new versions.
