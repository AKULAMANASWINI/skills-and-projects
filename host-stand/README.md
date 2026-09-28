# Host Stand

A reservation book and seating chart for the host stand, to replace the paper
book. It is standalone: it does not connect to Toast or any POS. One file,
`index.html`, is the whole application. No build step and no server needed.

## What it does

**Floor**: the restaurant's own room, traced from the hand-drawn plan: booths
101–106, the 200s run, the 300s wall (312–316), the rounds (2, 307–310) and the
buffet room's two long tables. On a landscape screen the plan turns sideways to
fill it (the top of the drawing goes to the left). On a portrait screen it shows
as drawn. Setup → *Show the floor* fixes either one. Every table shows its state
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

To seat a party, tap **Seat**. The banner suggests the best fits, like
`309 · 6`, `307 · 4+1` (one added chair) or `312+313 · 8`. Tap a suggestion, or
tap tables yourself, then **Seat here**. The banner says whether the pick fits,
needs added chairs, or is short. Tapping an open table directly
lets you seat a walk-in there in two taps.

**Book**: the day's page from the book: every reservation and walk-in with time,
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

Seat counts for the other tables were read off the sketch (2 for the small
booths, 4 for 104 and 204, 6 for tables 2 and 309). Correct any of them in Setup.

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

- `config/settings`: `{ name, turn, hold, aspect, scale, orient }`
- `tables/<id>`: `{ id, label, seats, max, min, join, section, shape, x, y }`:
  `max` is capacity with added chairs, `min` the smallest party it is offered to,
  `join` the push-together group, and `x`/`y` a percentage of the floor as drawn
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
