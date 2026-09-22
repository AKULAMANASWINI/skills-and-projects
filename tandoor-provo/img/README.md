# Photography

Ten photographs on the page, cropped to each slot and exported at JPEG quality 82.

| File                    | Size      | Where it lands                       |
| ----------------------- | --------- | ------------------------------------ |
| `pani-puri.jpg`         | 1500×1000 | Menu, after Appetizers               |
| `bhel-puri.jpg`         | 1500×1000 | Menu, after Soups & Salads           |
| `cut-mirchi.jpg`        | 1500×1000 | Menu, after Indo-Chinese             |
| `hero-curry-naan.jpg`   | 1600×1200 | Menu, before From the Tandoor Oven   |
| `mint-chutney.jpg`      | 1500×1000 | Menu, after Non-Vegetarian Delights  |
| `lassi-pair.jpg`        | 900×1350  | Menu, after Naan                     |
| `catering-line.jpg`     | 1500×1000 | Catering, upper left                 |
| `catering-spread.jpg`   | 900×1400  | Catering, right column               |
| `catering-labels.jpg`   | 1500×1000 | Catering, lower left                 |
| `storefront-night.jpg`  | 1800×1013 | Visit, above the panels              |

`mango-lassi.jpg` and `table-setting.jpg` are kept as spares and are not referenced: the lassi
pair says the same thing better, and the fried batons on the table platter were never identified.

The six menu photographs are captioned with the dish and its price, so each one is a menu entry as
well as a picture. To add another, copy a `<figure class="menu-photo">` block into the grid next to
the section it belongs to.

## The logo

`logo.png` (511×212) is the mark as the gift card prints it: orange wordmark and pot, INDIAN
CUISINE in white. It was lifted from the printed menu card, the white page unmultiplied out of it
so it carries real alpha, and the black lettering recoloured to white to match the card.

The hero plate keeps the card's black on both themes rather than swapping the artwork per theme,
so the mark always reads the way the restaurant prints it. That is why there is one file and not
two.

**It is 511px wide** — enough at the size the hero uses, not enough to go bigger. A vector
original (SVG, EPS or AI) would drop straight in: replace `logo.png` and point the
`.logo-plate` background at it.

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
