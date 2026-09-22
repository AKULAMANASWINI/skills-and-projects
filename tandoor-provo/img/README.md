# Photography

Drop the eight images below into this folder, at these exact filenames, and the page picks them
up with no code change. Until a file is present, its slot renders as a clay-gradient panel with
the tandoor mark and a caption naming the shot it's waiting for — so the page looks finished
either way, and the gaps are self-documenting.

| Filename                      | Where it lands        | Crop  | What it should show                          |
| ----------------------------- | --------------------- | ----- | -------------------------------------------- |
| `hero-tandoori-platter.jpg`   | Hero, right column    | 4:5   | The mixed grill on sizzling onions           |
| `dining-room.jpg`             | Gallery, large tile   | 1:1   | The room, ideally with people in it          |
| `clay-oven.jpg`               | Gallery               | 1:1   | The tandoor itself, skewers going in         |
| `garlic-naan.jpg`             | Gallery               | 1:1   | Naan off the oven wall, blistered            |
| `masala-dosa.jpg`             | Gallery               | 1:1   | A dosa with sambar and chutney               |
| `tikka-masala.jpg`            | Gallery               | 1:1   | Curry in a copper handi                      |
| `kitchen.jpg`                 | Our Story             | 5:4   | Spices in the pan, hands working             |
| `lunch-buffet.jpg`            | Lunch Buffet          | 4:3   | The buffet line, full                        |

## Before exporting

- **Crop to the ratio in the table.** The slots use `object-fit: cover`, so an off-ratio image
  won't break the layout, but it will lose the edges.
- **Export at roughly 2× the display size** — 1600px on the long edge is plenty for every slot
  except the hero, which is worth 2000px. Save as JPEG at quality 80.
- Keep the whole folder under about 2 MB total or the page gets slow on phones.

Swapping a shot means changing the `src` on that `<figure class="shot">` in `index.html`.
Adding one means copying an existing `<figure>` block.

## Rights

These come from the restaurant's gallery at
[nickigomezphotography.pixieset.com](https://nickigomezphotography.pixieset.com/tandoorindiancuisine/).
Confirm the shoot's licence covers web use before publishing, and keep the photographer credit
that's in the gallery section and the footer.
