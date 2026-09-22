# Photography

Five photographs from the restaurant's shoot, cropped to the ratio each slot uses and exported at
JPEG quality 82. 583 KB for the set.

| File                    | Size      | Where it lands          |
| ----------------------- | --------- | ----------------------- |
| `hero-curry-naan.jpg`   | 1600×1200 | Hero, right column      |
| `table-setting.jpg`     | 1500×1000 | Gallery, upper left     |
| `lassi-pair.jpg`        | 900×1350  | Gallery, upper right    |
| `cut-mirchi.jpg`        | 1500×1000 | Gallery, lower left     |
| `mango-lassi.jpg`       | 900×1350  | Gallery, lower right    |

The two landscapes are the photographer's native 3:2, uncropped. The two portraits are native 2:3
and are cropped a little top and bottom by `object-fit: cover` when the column stretches them to
match the landscape beside them. The hero is the only hard crop: 3:2 down to 4:3, which takes a
slice off each side and keeps the full height.

## Captions

The visible page shows the photographs alone. The captions in each `<figure>` are the fallback
that appears only if an image fails to load, and the `alt` text describes the shot for screen
readers and search engines. Both deliberately avoid naming a dish where the photograph alone
doesn't settle it:

- `hero-curry-naan.jpg` is "curry and garlic naan" — it reads as butter chicken or chicken tikka
  masala, and those are different items at different prices on the menu.
- `table-setting.jpg` is "the table" — the crumbed batons on the triangular platter could be the
  fish pakora or the paneer pakora.

Name those two and the `alt` and caption can say so.

`cut-mirchi.jpg`, `mango-lassi.jpg` and `lassi-pair.jpg` are named from the menu with no ambiguity.

## Adding more

Copy a `<figure class="shot …">` block in `index.html` and point its `src` at the new file. A slot
whose image is missing falls back to a clay-gradient panel with the tandoor mark, so the page never
shows a broken image. Gallery tiles take `wide` (3:2) or `tall` (2:3, stretches to its row).

Keep the folder under about 2 MB total so the page stays quick on phones.

## Rights

From the shoot at
[nickigomezphotography.pixieset.com](https://nickigomezphotography.pixieset.com/tandoorindiancuisine/).
Confirm the licence covers web use, and keep the photographer credit in the gallery section and
the footer.
