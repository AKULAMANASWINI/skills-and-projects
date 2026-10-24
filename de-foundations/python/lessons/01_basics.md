# Python 01 — First programs: values, variables, decisions, loops, functions

**Goal:** write small programs that compute things and make decisions.
**Time:** ~6 hours. Exercises: `python/exercises/ex01_basics.py`, check with
`python python/check.py ex01`.

## Setup (once)

1. Install Python 3.12+ from python.org (Windows: tick "Add python.exe to PATH").
   Check: `python --version` (macOS/Linux may need `python3`).
2. Install VS Code + the "Python" extension. Open the `de-foundations` folder.
3. Two ways to run Python:
   - **REPL** (try things): type `python`, then lines one at a time. `exit()` to leave.
   - **Script** (real work): put code in `something.py`, run `python something.py`.

## Values and types

```python
42            # int
3.14          # float
"Hyderabad"   # str (text) — single or double quotes, same thing
True, False   # bool
None          # "no value" — Python's NULL
type(42)      # <class 'int'>
```

Arithmetic: `+ - * /` (`/` always gives a float: `7 / 2 == 3.5`), `//` floor division
(`7 // 2 == 3`), `%` remainder (`7 % 2 == 1`), `**` power.

Floats are approximate: `0.1 + 0.2 == 0.30000000000000004`. Money in pipelines uses
`decimal.Decimal` or integer cents — remember this for interviews.

## Variables

A name that points at a value. No declaration needed.

```python
price = 25.0
qty = 3
total = price * qty
print(total)                 # 75.0
print(f"Total: {total:.2f}") # f-string: Total: 75.00
```

Names: `snake_case`, descriptive. `order_total`, not `ot` or `x1`.

## Strings

```python
city = "  Hyderabad "
city.strip()        # "Hyderabad" — remove surrounding whitespace
city.lower()        # "  hyderabad "
"a,b,c".split(",")  # ["a", "b", "c"]
"-".join(["a","b"]) # "a-b"
"Hyd" in city       # True
len("abc")          # 3
"Hyderabad"[0:3]    # "Hyd" — slicing: start inclusive, end exclusive
```

Strings are **immutable**: `city.strip()` returns a *new* string; `city` is unchanged
unless you reassign: `city = city.strip()`.

Converting: `int("42")`, `float("3.5")`, `str(42)`. `int("abc")` raises an error —
lesson 03 handles that.

## Decisions: if / elif / else

```python
if qty <= 0:
    status = "invalid"
elif qty < 10:
    status = "normal"
else:
    status = "bulk"
```

**Indentation is syntax.** Four spaces. The indented block belongs to the line ending in `:`.

Comparisons: `== != < <= > >=`. Combine with `and`, `or`, `not`.
Check for None with `is`: `if email is None:` (same idea as SQL's `IS NULL`).

Truthiness: empty string `""`, `0`, `None`, empty list `[]` all count as False in an
`if`. Handy, but `if amount:` is wrong when 0 is a valid amount — be explicit then.

## Loops

```python
for i in range(5):        # 0,1,2,3,4
    print(i)

for city in ["Pune", "Dublin"]:
    print(city.upper())

n = 0
while n < 3:              # repeat while condition is true
    n += 1                # same as n = n + 1
```

`break` leaves the loop; `continue` skips to the next iteration.

## Functions

A named, reusable piece of logic. Data engineering code is *mostly* functions.

```python
def net_amount(quantity, unit_price, discount=0.0):
    """Revenue for one order line."""
    return quantity * unit_price * (1 - discount)

net_amount(2, 25.0)          # 50.0
net_amount(2, 25.0, 0.1)     # 45.0
```

- `return` sends the result back. A function without `return` returns `None` —
  the #1 beginner bug is `print`ing instead of `return`ing.
- `discount=0.0` is a default value.
- The `"""docstring"""` says what it does.

## How the exercises work

Each exercise is a function with `raise NotImplementedError`. Replace that line
with your code. The checker calls your function with test inputs:

```
python python/check.py ex01
```

`ok` = passed, `x` = wrong (it shows what it expected), `.` = not attempted.
Read the failure message carefully — learning to read errors is half the job.
