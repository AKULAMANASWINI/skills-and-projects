# Host Stand

A reservation book and seating chart for the host stand, to replace the paper
book. It is standalone: it does not connect to Toast or any POS. One file,
`index.html`, is the whole application. No build step and no server needed.

## What it does

**Floor**: the dining room drawn to match your layout. Every table shows its state
at a glance:

| Colour | Meaning |
|---|---|
| Green outline | Open |
| Amber, dashed | Held: a reservation assigned to it is due within the hold window (30 min by default) |
| Blue | Seated: party name, size and minutes at the table |
| Red | Seated past turn time (90 min by default) |

The right-hand rail is the working list for the shift:

- **Waiting**: walk-ins and arrived reservations, with minutes waited against the
  quoted time. The time turns red once they've waited past the quote.
- **Arriving**: today's reservations in time order, flagged `late 12m` when they
  are overdue. Buttons for **Arrived**, **Seat** and **No-show**.
- **Seated**: who is in the house and for how long. **Clear table** when they
  leave, **Move** to change tables.

To seat a party, tap **Seat**, then tap one table or several (push two four-tops
together for a party of eight), then **Seat here**. Tapping an open table directly
lets you seat a walk-in there in two taps.

**Book**: the day's page from the book: every reservation and walk-in with time,
guests, phone, table, status and notes. A covers-per-half-hour strip shows where
the rush is. Use the arrows at the top to go to any date and take bookings for
next week.

**Setup**: restaurant name, turn time, hold window, and the table list (name,
seats, section, shape). **Arrange floor** lets you drag tables into place on the
floor plan. A sample 19-table room (main dining, bar, patio) is there to start
from.

**Your data**: export the full history as CSV, or take a JSON backup and
restore it on another device.

## Where the data lives

| Where it runs | Storage |
|---|---|
| claude.ai artifact | the artifact's shared document store: every signed-in device sees the same book, live |
| opened from disk, or any static host | `localStorage`: this browser on this device only |

`boot()` asks the artifact runtime for its `db` capability and falls back to
`localStorage` when there isn't one. The header says which mode it is in.

In local mode, **take a backup** (Setup → Backup) regularly. Clearing browser
data deletes the book.

## Data model

Three collections, the same shape in both backends and in the JSON backup:

- `config/settings`: `{ name, turn, hold }`
- `tables/<id>`: `{ id, label, seats, section, shape, x, y }`, with `x`/`y` as a
  percentage of the floor
- `parties/<id>`: one row per reservation or walk-in:

| Field | |
|---|---|
| `type` | `res` or `walkin` |
| `date`, `time` | local `YYYY-MM-DD`, `HH:MM` (walk-ins have no time) |
| `name`, `size`, `phone`, `notes`, `tags[]` | |
| `status` | `booked` → `waiting` → `seated` → `done`, or `noshow` / `cancelled` / `left` |
| `tableIds[]` | one table, or several pushed together |
| `quote` | quoted wait in minutes (walk-ins) |
| `createdAt`, `arrivedAt`, `seatedAt`, `closedAt` | epoch ms |

The CSV export flattens this to one row per party and derives `wait_min`
(arrived → seated) and `table_min` (seated → cleared), ready for a notebook or
a warehouse load.
