# Tandoor Indian Cuisine — Provo

A redesign of [tandoorindiancuisineprovo.com](https://tandoorindiancuisineprovo.com/). One
self-contained page: `index.html`. No build step, no dependencies — open it, or drop it on any
static host (GitHub Pages, Netlify, Cloudflare Pages).

The only external requests are the two Google Fonts stylesheets. Everything else — CSS, JS, the
tandoor mark — is inline.

## What's in it

- Sticky header, hero, the clay-oven section, full menu, lunch buffet, story, visit, footer
- **Live open/closed indicator** computed in `America/Denver`, so it's correct for any visitor's
  time zone. Hours live in `OPEN_MIN` / `CLOSE_MIN` at the top of the script.
- **Dietary filter** (vegetarian / vegan / gluten-free) driven by `data-diet` on each `.dish`.
  Add a token to that attribute and the filter picks the dish up — no JS change needed.
- Light and dark themes, both designed, all colours defined as tokens on `:root`.
- `Restaurant` JSON-LD in the head for Google's listing panel.

## Menu source

Every dish, price and description is transcribed from the restaurant's own printed menu card
(three pages: appetizers/soups/Indo-Chinese, dosa/biryani/naan/vegetarian/tandoor, and
non-vegetarian/desserts/beverages/condiments). 98 dishes across 12 sections. The menu data is
plain HTML in `index.html` — each dish is an `<li class="dish">` carrying `data-veg` and
`data-search`, so the search box and the vegetarian toggle pick up any dish you add without a
code change.

## Dietary marks

The printed card marks vegetarian with a green leaf and gluten-free with a crossed-wheat icon.
Those are transcribed as `V` and `GF` badges. Two departures, both deliberate:

- **`GF` appears on exactly two items** — Kachumber and Butternut Squash Soup — because those are
  the only two the card marks. Nothing else is claimed gluten-free, even where it plainly is.
  Allergen claims the restaurant hasn't made itself don't belong on its website.
- **`V` is applied a little more widely than the card's leaf icons**, which are inconsistent: the
  Vegetarian Delights, Naan, Desserts, Beverages, Condiments and Soups sections are marked
  wholesale (the card's own section headings and item names establish it), and Chilli Paneer,
  Paneer Tikka Kebab and the paneer/vegetable dosas and biryanis carry a leaf the card omits.
  Egg Biryani is deliberately **not** marked vegetarian.

If any of those is wrong, fix the `data-veg` attribute on that `<li>` and the badge beside it.

## Still to confirm

1. **The lunch buffet.** Yelp lists a daily buffet; the printed menu card doesn't mention one. The
   page has a buffet section with no price and no specific times, which is as far as the sources
   go. Confirm it still runs, then add times and a price — or delete the section.
2. **Hours.** Mon–Sat 11 am – 10 pm, closed Sunday, per Google and Yelp. The live status pill in
   the hero reads from `OPEN_MIN` / `CLOSE_MIN` in the script.
3. **Photography.** See `img/README.md`.
