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

## Verified against public sources

Address, phone, email, hours, the daily buffet, the 4.6-star average, the ordering and catering
links, and the restaurant's own "symphony of spices" line all come from the live site, Yelp,
ezCater and Google.

## Needs confirming before this goes live

The per-dish prices and descriptions are reconstructed, not copied — the live site was not
reachable from the build environment, so only the section price *ranges* were available
(appetizers $6.95–$16.95 across 9 items; tandoori $14.95–$22.95 across 8 items, both honoured
here). Known-real dishes are in: samosa, vegetable pakora, cut mirchi, Chicken 65, pepper
calamari, tikka masala, saag, coconut korma, vindaloo, aloo gobi, garlic naan, dosas, biryani and
the Tandoor's Mixed Grill.

Before publishing, check against the real menu:

1. Every price and dish description.
2. The lunch buffet price — deliberately left off the page rather than guessed. Add it in the
   `#buffet` section.
3. Buffet hours. The page splits lunch (11–3) from dinner (3–10); the source only confirms
   11 am – 10 pm overall.
4. The oven specs in the `.oven` section (480°C, 24-hour marinade, 90-second naan) — typical for
   a tandoor, but they should be the kitchen's own numbers.
5. Photography. The design works without it; if photos are added, the menu cards and hero are
   where they'd go.
