# Photography

Twelve photographs on the page, cropped to each slot and exported at JPEG quality 82. About
1.9 MB for the set.

| File                    | Size      | Where it lands            |
| ----------------------- | --------- | ------------------------- |
| `hero-curry-naan.jpg`   | 1600×1200 | Gallery, bottom row       |
| `bhel-puri.jpg`         | 1500×1000 | Gallery, upper left       |
| `lassi-pair.jpg`        | 900×1350  | Gallery, upper right      |
| `pani-puri.jpg`         | 1500×1000 | Gallery, middle left      |
| `mango-lassi.jpg`       | 900×1350  | Gallery, middle right     |
| `cut-mirchi.jpg`        | 1500×1000 | Gallery, bottom row       |
| `mint-chutney.jpg`      | 1500×1000 | Gallery, bottom row       |
| `table-setting.jpg`     | 1500×1000 | Gallery, bottom row       |
| `catering-line.jpg`     | 1500×1000 | Catering, upper left      |
| `catering-spread.jpg`   | 900×1400  | Catering, right column    |
| `catering-labels.jpg`   | 1500×1000 | Catering, lower left      |
| `storefront-night.jpg`  | 1800×1013 | Visit, above the panels   |

## The logo

`logo-light.png` and `logo-dark.png` (511×212) are the same mark rendered for the two grounds:
the "INDIAN CUISINE" line and its rules are black on light, cream on dark. The hero plate picks
one by CSS `background-image`, following the same cascade as the colour tokens, so only the
applied file is ever downloaded.

Both were lifted from the printed menu card and the white page unmultiplied out of them, which
means they carry real alpha and sit on any ground. **They are 511px wide — enough at the size the
hero uses, not enough to go bigger.** A vector original (SVG, EPS or AI) would drop straight in:
replace both files, or point the CSS at a single SVG and drop the theme swap, recolouring the
wordmark with `currentColor` instead.

Landscapes are the photographer's native 3:2, uncropped. The two portraits are native 2:3, cropped
slightly by `object-fit: cover` where the column stretches them to match the landscape beside them.
The hero is the only hard crop: 3:2 down to 4:3, taking a slice off each side.

Every slot falls back to a clay-gradient panel with the tandoor mark if its file is missing, so
the page never shows a broken image. Gallery tiles take `wide` (3:2) or `tall` (2:3, stretches to
its row); `.gallery-row` below holds three across.

## Captions

Visible page shows the photographs alone — the captions in each `<figure>` appear only if an image
fails to load. The `alt` text describes the shot for screen readers and search.

Two avoid naming a dish the photograph doesn't settle:

- `hero-curry-naan.jpg` — "curry and garlic naan". It reads as butter chicken or chicken tikka
  masala, which are different items at different prices.
- `table-setting.jpg` — "the table". The crumbed batons could be the fish pakora or the paneer
  pakora.

Name those two and the captions can say so. `bhel-puri`, `pani-puri`, `cut-mirchi`,
`mint-chutney`, `mango-lassi` and `lassi-pair` are named from the menu with no ambiguity.

## Not yet on file

Three batches came through in conversation without reaching the filesystem. Nothing from them is
on the page. Worth chasing, roughly best first:

- **The sizzler being carried**, steam and sparks against a black background — the single best
  shot of the lot, and lit for this site's palette. Hero material.
- **The bread basket held up**, same dark treatment.
- **The long dosa** with five chutneys — the best argument for the southern half of the menu.
- **A family of four at a table**, and **a couple toasting**. The only shots with people in them;
  check the shoot's model release before either goes up.
- **The assorted snacks platter** — matches that menu item exactly.
- **The long communal table**, a dozen people mid-meal — the best proof the room fills up, and
  the natural companion to the catering section.
- Garlic naan (twice), chana masala, samosas, onion bhaji, the rose table setting, an overhead
  spread with palak paneer and chicken lollipop, a booth of three, a guest with a strawberry
  lassi, and several more sizzler frames.

- **The branded gift card** held up in the room. The page now mentions gift cards in the Visit
  panel on the strength of this photograph; the shot itself would sit well beside that line.

Every shot with recognisable faces needs the shoot's model release checked before it goes up.

## Rights

From the shoot at
[nickigomezphotography.pixieset.com](https://nickigomezphotography.pixieset.com/tandoorindiancuisine/).
Confirm the licence covers web use, and keep the photographer credit in the gallery section and
the footer.
