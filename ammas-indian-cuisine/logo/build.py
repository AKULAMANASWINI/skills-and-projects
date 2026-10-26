"""
Draws the Amma's logo concepts as self-contained SVGs: every letter is
converted to an outline from the site's own fonts, so the files render the
same in a browser, a print shop or a sign maker's software.

    python3 ammas-indian-cuisine/logo/build.py [options-page.html]

Writes <n>-<name>.svg (full logo) and <n>-<name>-icon.svg (small mark) next
to this script. With an argument, also writes a page comparing the concepts.
Needs: pip install fonttools brotli
"""
import math
import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "print" / "fonts"

INK = "#171614"
BRASS = "#94661c"
DARK_INK = "#f5f2ee"
DARK_BRASS = "#c9a061"


class Face:
    def __init__(self, file, wght=None):
        font = TTFont(FONTS / file)
        if wght:
            font = instantiateVariableFont(font, {"wght": wght})
        self.glyphs = font.getGlyphSet()
        self.cmap = font.getBestCmap()
        self.upm = font["head"].unitsPerEm
        self.hmtx = font["hmtx"]

    def name(self, ch):
        return self.cmap[ord(ch)]

    def advance(self, ch, size):
        return self.hmtx[self.name(ch)][0] * size / self.upm

    def bounds(self, ch, size):
        pen = BoundsPen(self.glyphs)
        self.glyphs[self.name(ch)].draw(pen)
        x0, y0, x1, y1 = pen.bounds
        k = size / self.upm
        return x0 * k, y0 * k, x1 * k, y1 * k

    def glyph_path(self, ch, matrix):
        pen = SVGPathPen(self.glyphs)
        self.glyphs[self.name(ch)].draw(TransformPen(pen, matrix))
        return pen.getCommands()

    def width(self, text, size, track=0.0):
        return sum(self.advance(c, size) for c in text) + track * size * (len(text) - 1)

    def text(self, text, x, y, size, track=0.0, anchor="start"):
        """Outline a line of text with its baseline at y. Returns SVG path data."""
        w = self.width(text, size, track)
        x -= {"start": 0, "middle": w / 2, "end": w}[anchor]
        k = size / self.upm
        parts = []
        for ch in text:
            if ch != " ":
                parts.append(self.glyph_path(ch, (k, 0, 0, -k, x, y)))
            x += self.advance(ch, size) + track * size
        return " ".join(parts)

    def ring(self, text, cx, cy, r, size, centre=""):
        """Text around a full circle, reading clockwise, letters spaced to fill it.
        The leading `centre` part of the text is centred at 12 o'clock."""
        k = size / self.upm
        natural = sum(self.advance(c, size) for c in text)
        gap = (2 * math.pi * r - natural) / len(text)
        lead = sum(self.advance(c, size) for c in centre) + gap * (len(centre) - 1)
        parts, s = [], -lead / 2
        for ch in text:
            adv = self.advance(ch, size)
            theta = (s + adv / 2) / r  # radians clockwise from 12 o'clock
            px, py = cx + r * math.sin(theta), cy - r * math.cos(theta)
            cos, sin = math.cos(theta), math.sin(theta)
            # rotate the upright glyph by theta, flip y, centre it on its advance
            a, b, c, d = k * cos, k * sin, k * sin, -k * cos
            e, f = px - cos * adv / 2, py - sin * adv / 2
            if ch != " ":
                parts.append(self.glyph_path(ch, (a, b, c, d, e, f)))
            s += adv + gap
        return " ".join(parts)


CASLON = Face("LibreCaslonDisplay-400.woff2")
HANKEN = Face("HankenGrotesk.woff2", wght=500)


def drop(cx, top, h):
    """A diya flame: pointed top, round base. Stands in for the apostrophe."""
    w = h * 0.62
    b = top + h
    return (f"M{cx:.2f} {top:.2f} C{cx + w * 0.62:.2f} {top + h * 0.42:.2f} {cx + w * 0.55:.2f} {b:.2f} {cx:.2f} {b:.2f} "
            f"C{cx - w * 0.55:.2f} {b:.2f} {cx - w * 0.62:.2f} {top + h * 0.42:.2f} {cx:.2f} {top:.2f}Z")


def wordmark(x, y, size, anchor="middle"):
    """'Amma's' with the apostrophe drawn as a brass flame. Returns (ink path, brass path, width)."""
    k_gap = -size * 0.005
    w_amma = CASLON.width("Amma", size)
    w_s = CASLON.width("s", size)
    _, ay0, _, ay1 = CASLON.bounds("’", size)
    h = (ay1 - ay0) * 1.2
    drop_w = h * 0.62
    total = w_amma + k_gap + drop_w + k_gap + w_s
    x0 = x - {"start": 0, "middle": total / 2, "end": total}[anchor]
    ink = CASLON.text("Amma", x0, y, size) + " " + CASLON.text("s", x0 + w_amma + 2 * k_gap + drop_w, y, size)
    brass = drop(x0 + w_amma + k_gap + drop_w / 2, y - ay1 + h * 0.06, h)
    return ink, brass, total


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img">'
            f"<title>{title}</title>{body}</svg>\n")


def p(d, fill):
    return f'<path d="{d}" fill="{fill}"/>'


def line(d, stroke, width):
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


SUB = "CURATED INDIAN CUISINE"


# 1 — Signature: the name alone, apostrophe as a diya flame
def signature(ink, brass):
    name, flame, w = wordmark(300, 128, 120)
    sub = HANKEN.text(SUB, 300, 178, 15, track=0.36, anchor="middle")
    return svg(600, 210, p(name, ink) + p(flame, brass) + p(sub, ink), "Amma's Indian Cuisine")


def signature_icon(ink, brass):
    a = CASLON.text("A", 50, 80, 86, anchor="middle")
    return svg(100, 100, p(a, ink) + p(drop(83, 20, 22), brass), "Amma's")


# 2 — Seal: ring of text around a single letter
def seal(ink, brass):
    c = 160
    ring_text = "AMMA’S · CURATED INDIAN CUISINE · "
    body = (f'<circle cx="{c}" cy="{c}" r="152" fill="none" stroke="{ink}" stroke-width="2.5"/>'
            f'<circle cx="{c}" cy="{c}" r="104" fill="none" stroke="{ink}" stroke-width="1.2"/>'
            + p(HANKEN.ring(ring_text, c, c, 120, 17, centre="AMMA’S"), ink)
            + p(CASLON.text("A", c, c + 46, 132, anchor="middle"), ink)
            + p(drop(c + 44, c - 70, 26), brass))
    return svg(320, 320, body, "Amma's Indian Cuisine")


def seal_icon(ink, brass):
    body = (f'<circle cx="50" cy="50" r="46" fill="none" stroke="{ink}" stroke-width="3"/>'
            + p(CASLON.text("A", 50, 74, 66, anchor="middle"), ink)
            + p(drop(73, 22, 15), brass))
    return svg(100, 100, body, "Amma's")


# 3 — Handi: the cooking pot with steam, above the name
def handi_mark(cx, top, s, brass, width):
    def pt(x, y):
        return f"{cx + x * s:.2f} {top + y * s:.2f}"
    pot = (f"M{pt(-34, 30)} L{pt(34, 30)} "
           f"M{pt(-28, 30)} C{pt(-52, 52)} {pt(-46, 92)} {pt(0, 94)} C{pt(46, 92)} {pt(52, 52)} {pt(28, 30)} "
           f"M{pt(-38, 58)} L{pt(38, 58)}")
    steam = " ".join(
        f"M{pt(x, 22)} C{pt(x - 7, 14)} {pt(x + 7, 8)} {pt(x, 0)}" for x in (-14, 0, 14))
    return line(pot, brass, width) + line(steam, brass, width)


def handi(ink, brass):
    name, flame, _ = wordmark(250, 222, 96)
    sub = HANKEN.text(SUB, 250, 262, 13, track=0.36, anchor="middle")
    return svg(500, 290, handi_mark(250, 20, 1.15, brass, 3) + p(name, ink) + p(flame, brass) + p(sub, ink),
               "Amma's Indian Cuisine")


def handi_icon(ink, brass):
    return svg(100, 100, handi_mark(50, 4, 0.98, brass, 4.5), "Amma's")


# 4 — Kolam: the threshold drawing made each morning, beside the name
def kolam_mark(cx, cy, r, brass, width):
    parts = []
    for i in range(4):
        t = math.pi / 2 * i
        def rot(x, y):
            return f"{cx + x * math.cos(t) - y * math.sin(t):.2f} {cy + x * math.sin(t) + y * math.cos(t):.2f}"
        parts.append(f"M{rot(0, 0)} C{rot(r * 0.55, -r * 0.35)} {rot(r * 0.6, -r * 1.05)} {rot(0, -r * 1.05)} "
                     f"C{rot(-r * 0.6, -r * 1.05)} {rot(-r * 0.55, -r * 0.35)} {rot(0, 0)}")
    dots = "".join(
        f'<circle cx="{cx + d * math.sin(a):.2f}" cy="{cy - d * math.cos(a):.2f}" r="{width * 1.05:.2f}" fill="{brass}"/>'
        for d, a in [(0, 0)] + [(r * 0.62, math.pi / 2 * i) for i in range(4)] + [(r * 0.86, math.pi / 4 + math.pi / 2 * i) for i in range(4)])
    ring = f'<circle cx="{cx}" cy="{cy}" r="{r * 1.22:.2f}" fill="none" stroke="{brass}" stroke-width="{width * 0.6:.2f}"/>'
    return line(" ".join(parts), brass, width) + dots + ring


def kolam(ink, brass):
    name, flame, w = wordmark(196, 112, 100, anchor="start")
    sub = HANKEN.text(SUB, 198, 152, 12.5, track=0.36)
    width = 196 + max(w, HANKEN.width(SUB, 12.5, 0.36)) + 20
    return svg(width, 190, kolam_mark(88, 95, 58, brass, 3) + p(name, ink) + p(flame, brass) + p(sub, ink),
               "Amma's Indian Cuisine")


def kolam_icon(ink, brass):
    return svg(100, 100, kolam_mark(50, 50, 36, brass, 3.4), "Amma's")


CONCEPTS = [
    ("1", "signature", "Signature", signature, signature_icon,
     "The name alone in the website's serif, with the apostrophe drawn as a brass diya flame.",
     "Quietest and most fine-dining. Reads like Le Bernardin or Per Se.",
     "The small mark is just an A, so it relies on the name being seen elsewhere."),
    ("2", "seal", "Seal", seal, seal_icon,
     "A round seal with the name and Curated Indian Cuisine around a single A.",
     "Ready-made for stamps, stickers, takeaway bags and the round Instagram picture.",
     "Ring text is unreadable below about 60 pixels; the small version keeps only the A."),
    ("3", "handi", "Handi", handi, handi_icon,
     "A brass handi, the pot biryani is cooked in, with steam above the name.",
     "Says Indian kitchen at a glance and matches the doodles behind the website menu.",
     "A pot icon is common among Indian restaurants, so it is the least distinctive."),
    ("4", "kolam", "Kolam", kolam, kolam_icon,
     "A kolam, the dot-and-loop drawing mothers make at the doorstep each morning, beside the name.",
     "Most personal: it is literally Amma's mark at the threshold. Holds up well at small sizes.",
     "Not every guest will recognise it as a kolam; some will just see a flower."),
]


def page(pieces):
    cards = []
    for n, slug, title, full, icon, what, good, risk in pieces:
        cards.append(f"""
  <section class="concept" id="c{n}">
    <header><span class="num">Option {n}</span><h2>{title}</h2><p>{what}</p></header>
    <div class="boards">
      <div class="board light">{full(INK, BRASS)}</div>
      <div class="board dark">{full(DARK_INK, DARK_BRASS)}</div>
    </div>
    <div class="small">
      <div class="tile"><span class="lbl">App and map pin</span><div class="sq">{icon(INK, BRASS)}</div></div>
      <div class="tile"><span class="lbl">Instagram</span><div class="round">{icon(INK, BRASS)}</div></div>
      <div class="tile"><span class="lbl">Browser tab, 32px</span><div class="tab">{icon(INK, BRASS)}</div></div>
      <div class="tile"><span class="lbl">Browser tab, 16px</span><div class="tab tiny">{icon(INK, BRASS)}</div></div>
    </div>
    <dl><div><dt>Good for</dt><dd>{good}</dd></div><div><dt>Watch out</dt><dd>{risk}</dd></div></dl>
  </section>""")
    return f"""<title>Amma's Logo Options</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Display&family=Hanken+Grotesk:wght@300;500&display=swap">
<style>
/* Layout: a presentation board per concept: full logo on paper and on night, then the sizes it must survive. Single light look. */
:root {{
  --page: #ffffff; --ink: #171614; --soft: #6d6862; --hair: #e6e2dc; --brass: #94661c; --night: #141311; --wash: #f6f4f1;
  --display: "Libre Caslon Display", Georgia, serif;
  --sans: "Hanken Grotesk", "Helvetica Neue", Arial, sans-serif;
  color-scheme: light;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--page); color: var(--ink); font: 300 1rem/1.6 var(--sans); }}
.wrap {{ max-width: 1100px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 48px 72px; }}
h1, h2 {{ font-family: var(--display); font-weight: 400; margin: 0; text-wrap: balance; }}
h1 {{ font-size: clamp(2.2rem, 6vw, 3.6rem); line-height: 1; }}
.intro {{ display: grid; gap: 14px; margin-bottom: 48px; }}
.intro p {{ color: var(--soft); max-width: 62ch; margin: 0; }}
.num, .lbl, dt {{ font: 500 0.68rem/1.4 var(--sans); letter-spacing: 0.22em; text-transform: uppercase; }}
.num {{ color: var(--brass); }}
.concept {{ border-top: 1px solid var(--hair); padding-block: 40px; display: grid; gap: 22px; }}
.concept header {{ display: grid; gap: 6px; }}
.concept h2 {{ font-size: 2rem; }}
.concept header p {{ color: var(--soft); margin: 0; max-width: 64ch; }}
.boards {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
.board {{ display: grid; place-items: center; padding: 36px 24px; min-height: 260px; }}
.board svg {{ width: 100%; max-width: 380px; height: auto; max-height: 240px; }}
.light {{ background: var(--page); border: 1px solid var(--hair); }}
.dark {{ background: var(--night); }}
.small {{ display: flex; flex-wrap: wrap; gap: 24px; align-items: end; }}
.tile {{ display: grid; gap: 8px; justify-items: start; color: var(--soft); }}
.sq {{ width: 96px; height: 96px; background: var(--wash); border-radius: 22px; display: grid; place-items: center; padding: 14px; }}
.round {{ width: 96px; height: 96px; background: var(--wash); border-radius: 50%; display: grid; place-items: center; padding: 16px; }}
.tab {{ width: 32px; height: 32px; display: grid; place-items: center; outline: 1px dashed var(--hair); }}
.tab.tiny {{ width: 16px; height: 16px; }}
.sq svg, .round svg, .tab svg {{ width: 100%; height: 100%; }}
dl {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px 32px; margin: 0; }}
dt {{ color: var(--ink); margin-bottom: 4px; }}
dd {{ margin: 0; color: var(--soft); }}
@media (max-width: 720px) {{
  .boards, dl {{ grid-template-columns: minmax(0, 1fr); }}
  .board {{ min-height: 0; }}
}}
</style>
<div class="wrap">
  <div class="intro">
    <span class="num">Amma's Indian Cuisine</span>
    <h1>Four logo options</h1>
    <p>Each option is shown on white and on black, then at the small sizes where a logo is seen most: the app icon, the round Instagram picture and the browser tab. All four use the website's own lettering and brass colour. Tell me the number you want.</p>
  </div>
  {"".join(cards)}
</div>
"""


def main():
    for n, slug, _title, full, icon, *_ in CONCEPTS:
        (HERE / f"{n}-{slug}.svg").write_text(full(INK, BRASS))
        (HERE / f"{n}-{slug}-icon.svg").write_text(icon(INK, BRASS))
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(page(CONCEPTS))
    print("wrote", ", ".join(f"{n}-{s}.svg" for n, s, *_ in CONCEPTS))


if __name__ == "__main__":
    main()
