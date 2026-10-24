# Data engineering foundations: SQL and Python from zero

This is Phase 1 of the *Data & AI Engineering → Microsoft* roadmap, rebuilt for
someone starting with **no SQL and no Python**. It covers every Phase 1 roadmap item
and gets you to the milestone: **solve 60 SQL problems unaided and ship a tested
Python ingestion script.**

## Read this first: two things you won't like

1. **The roadmap's Phase 1 assumes you already know the basics.** Its first item is
   "Advanced SQL: window functions". From zero, you first need SELECT, GROUP BY, JOINs,
   and Python variables, loops and functions. This course adds them, and that makes
   Phase 1 **10 weeks, not 8**, at about 15 hours a week. The 66-week runway can absorb
   two extra weeks: the three phases end in June 2027 and the target is January 2028.
   Rushing the foundations to protect the schedule costs more later, because every
   later phase is built on them.
2. **Reading the lessons is not the work. The exercises are.** You learn by being
   stuck and getting yourself unstuck. If you use me or any other AI to write your
   answers, the checker will show 60 passes and you'll still fail the interview.
   Ask AI for a *hint* or *why your query is wrong*, never for the answer.

## Setup (30 minutes, once)

1. Install **Python 3.12+** (python.org; on Windows tick "Add to PATH") and **VS Code**
   with the Python extension. On Windows, also install **Git** (git-scm.com).
2. Get this folder onto your machine (`git clone` the repo) and open `de-foundations/` in VS Code.
3. In a terminal inside `de-foundations/`:

```bash
python data/build_db.py          # creates data/shop.db and data/raw/ (use python3 on macOS/Linux if needed)
python sql/run.py "SELECT COUNT(*) FROM orders"    # should print 2000
python sql/check.py 01           # 8 questions, all "not attempted"
python python/check.py ex01      # 8 tests, all "not attempted"
```

Nothing else to install until week 6. Optional now: **DBeaver** (free), opening
`data/shop.db`, to look at tables with a GUI.

## What's here

| folder | what |
|---|---|
| `sql/lessons/` | 7 lessons, from SELECT to window functions, execution plans and modeling |
| `sql/exercises/` | **60 auto-checked SQL problems.** Write answers here and run `python sql/check.py` |
| `sql/solutions/` | reference answers. Open one only after a real attempt plus 20 minutes stuck |
| `python/lessons/` | 8 lessons, from the first variable to pytest, APIs, pandas/polars, Parquet, Linux and Git |
| `python/exercises/` | 47 auto-checked functions to implement. Run `python python/check.py` |
| `python/solutions/` | reference implementations, same rule as above |
| `capstone/` | the milestone project and an unreliable fake API to build it against. **No solution.** |
| `data/` | the practice shop database: customers, products, orders, order_items, plus messy raw files |

## The 10-week plan

About 2 hours on weekdays and 5 on the weekend. The **Board/Journal** columns map to
your tracker: log every day, including bad ones.

| week | dates (2026–27) | SQL | Python and tools | done when |
|---|---|---|---|---|
| 1 | Oct 26 – Nov 1 | 01 SELECT / WHERE / NULL | Py 01 basics, plus 20 min/day of lesson 08 (terminal, Git) | `check.py 01` 8/8, `ex01` 8/8, the repo is on your GitHub |
| 2 | Nov 2 – 8 | 02 GROUP BY / HAVING / CASE | Py 02 collections | 02 8/8, ex02 8/8 |
| 3 | Nov 9 – 15 | 03 JOINs, fan-out | Py 03 functions and errors | 03 8/8, ex03 8/8 |
| 4 | Nov 16 – 22 | 04 subqueries / CTEs; **redo 01–03 in a blank file** | Py 04 files, CSV, JSON | 04 7/7, ex04 7/7, `data/clean/customers.csv` written |
| 5 | Nov 23 – 29 | 05 window functions (the big one) | Py 05 idiomatic: venv/uv, dataclasses, generators, logging | 05 10/10, ex05 7/7 |
| 6 | Nov 30 – Dec 6 | **redo 05 from blank**; 06 execution plans | Py 06 pytest and APIs (install pytest) | 06 4/4 plus plan tasks, ex06 9/9, `pytest python/tests` green |
| 7 | Dec 7 – 13 | 07 relational and dimensional modeling, SCDs | Py 07 pandas vs polars, Parquet, partitioning | star schema built, revenue reconciles, file-format numbers in your journal |
| 8 | Dec 14 – 20 | 08 interview drills (15), timed | capstone: extract and retry | 08 15/15 |
| 9 | Dec 21 – 27 | 3 drills a day, mixed, from blank | capstone: transform, load, idempotency | capstone runs twice with identical counts |
| 10 | Dec 28 – Jan 3 | **milestone test** (below) | capstone: tests, README, PRs | both milestones met. Phase 2 starts Jan 4 |

### A day of study

1. **10 min:** redo yesterday's hardest problem from a blank file (spaced repetition).
2. **40 min:** lesson, with every code example typed out and run. Not copy-pasted.
3. **60 min:** exercises. Stuck? Re-read the lesson, then simplify the problem
   (run half the query), then ask for a hint. Only after all three, open the solution;
   then close it and write the answer yourself from memory.
4. **5 min:** a journal entry covering what clicked, what didn't, and one question to resolve tomorrow.
   Commit your work with a conventional commit message.

### What "unaided" means for the milestone

In week 10, copy `sql/exercises/` to a new folder with the same blank questions and
solve all 60 without the lessons, solutions, search or AI. You pass at 54/60, and
every miss gets redone two days later. Until then, a pass in the checker counts as
practice, not as the milestone.

## Roadmap coverage

| Phase 1 roadmap item | where |
|---|---|
| Advanced SQL: window functions, frames (ROWS vs RANGE), running totals, moving averages | SQL 05, 08 |
| SQL performance and execution plans: indexes, EXPLAIN, join algorithms, cardinality, statistics | SQL 06 |
| Idiomatic Python: type hints, dataclasses, generators, context managers, venv/uv, layout, logging | Py 05, capstone |
| Python data handling at scale: pandas vs polars, chunked reads, memory, retries/backoff, paginated APIs | Py 06, 07, capstone |
| Linux, Bash and Git: pipelines, cron, permissions, SSH, branching, conventional commits, PR etiquette | lesson 08 |
| Relational modeling: normal forms, PK/FK, constraints, surrogate vs natural keys, integrity | SQL 07 part A |
| Dimensional modeling and SCDs: star schema, facts vs dimensions, grain, conformed dimensions, SCD 1/2/3 | SQL 07 part B |
| File formats and storage layout: row vs columnar, Parquet internals, codecs, partition pruning, small files | Py 07 |
| *(added)* SQL basics: SELECT, filtering, NULL, GROUP BY, JOINs, subqueries, CTEs | SQL 01–04 |
| *(added)* Python basics: types, control flow, functions, collections, errors, files | Py 01–04 |

## Commands

```bash
python sql/run.py                     # interactive SQL prompt (.tables, .schema orders, .quit)
python sql/check.py                   # all SQL, with a running count toward 60
python sql/check.py 05 q3             # one question
python python/check.py ex04           # one Python exercise file
pytest python/tests                   # after installing pytest in week 6
python data/build_db.py               # reset the database (drops any indexes you added)
python capstone/fake_api.py           # the capstone's unreliable API
```
