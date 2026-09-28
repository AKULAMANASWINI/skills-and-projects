# Host Stand

A reservation book and seating chart for the host stand, to replace the paper
book. It is standalone: it does not connect to Toast or any POS. One file,
`index.html`, is the whole application. No build step and no server needed.

## What it does

**Floor**: a drawn floor plan of the restaurant, traced from its architectural
layout: outer walls, the 100s and 200s booths with their benches and doors,
the 312–316 row (tables along one long wall couch, two chairs facing each), the
round tables (2, 307, 308, 310 small, 309 a little bigger), the buffet room and
the entrance. On a landscape screen (a laptop, or an iPad held sideways) the
plan turns sideways to fill the space, entrance on the right. On a portrait
screen it shows as drawn, entrance at the bottom. Setup → *Show the floor* can
fix either one. Every table shows its state
at a glance:

| Table | Meaning |
|---|---|
| White | Available |
| Amber | Reservation due: one assigned to it arrives within the hold window (30 min by default) |
| Blue | Seated: guests and minutes at the table |
| Red | Seated past turn time (90 min by default) |

A table that takes extra chairs shows its range, e.g. `4–5`.

The panel beside the plan is the working list for the shift, in three tabs:

- **Upcoming**: today's reservations in time order, flagged `late 12m` when they
  are overdue. Buttons for **Seat**, **Arrived** and **No-show**.
- **Waiting**: walk-ins and arrived reservations, with minutes waited against the
  quoted time. The time turns red once they've waited past the quote.
- **Seated**: who is in the house and for how long. **Clear table** when they
  leave, **Move** to change tables.

To seat a party, tap **Seat**. The banner suggests the best fits, like
`309 · 6`, `307 · 4+1` (one added chair) or `312+313 · 8`. Tap a suggestion, or
tap tables yourself, then **Seat here**. The banner says whether the pick fits,
needs added chairs, or is short. Tapping an open table directly
lets you seat a walk-in there in two taps.

**Reservations**: the day's page from the book: every reservation and walk-in with time,
guests, phone, table, status and notes. A covers-per-half-hour strip shows where
the rush is. Use the arrows at the top to go to any date and take bookings for
next week.

**Setup**: restaurant name, turn time, hold window, floor shape, and the table
list. **Arrange floor** lets you drag tables into place.

The house seating rules are built into the table list:

| Tables | Rule |
|---|---|
| 307, 308, 310 | 4 seats, up to 5 with an added chair |
| 312–316 | push together (group `300s wall`) for parties over 6 |
| Buffet A + B | buffet room: 8 seats each normally, 12 and 13 with added chairs (25 together); only suggested for parties of 8 or more, and first choice for 13+ |

312–316 seat 4 each: 2 on the couch and 2 chairs. 309 seats 6. Booth seat
counts are 2, except 104 and 204 at 4. Correct any of them in Setup.

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

- `config/settings`: `{ name, turn, hold, orient }`
- `tables/<id>`: `{ id, label, seats, max, min, join, section, shape, x, y, w, h, benches }`:
  `max` is capacity with added chairs, `min` the smallest party it is offered to,
  `join` the push-together group. `shape` is `booth`, `round` or `rect`. `x`/`y` is
  the table's centre and `w`/`h` its size, both in plan units (the walls and booth
  rooms are the `ROOM` constant in the same units). `benches` names the booth
  sides that have a bench (`t`, `b`, `l`, `r`). `couch` is how many of a
  table's seats are on a shared couch, and `sides` which sides get chairs.
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
