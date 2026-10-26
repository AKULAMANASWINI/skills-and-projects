/**
 * Builds the printed menu (four US Letter pages: two sheets printed both
 * sides, or one 11x17 sheet folded) from the website's own CONFIG and MENU,
 * so the paper menu and the site never drift.
 *
 *   node ammas-indian-cuisine/print/build.mjs
 *
 * Writes print/menu.html and print/menu.pdf. Fails if any page overflows
 * the sheet, so a longer menu is caught here rather than at the printer.
 */
import { readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const site = readFileSync(resolve(here, "../index.html"), "utf8");

/* The data block sits between these two markers in the site's script. */
const start = site.indexOf("// ---- Edit your restaurant's details here");
const end = site.indexOf("// --------------------------------------------------------------------------", start);
if (start === -1 || end === -1) throw new Error("could not find the CONFIG/MENU block in index.html");
const { CONFIG, MENU } = new Function(site.slice(start, end) + "; return { CONFIG, MENU };")();

/* Each page is [left column, right column]; a section never splits across
   columns. The last page's footer carries hours and address. */
const PAGES = [
  [["Appetizers"], ["65 & Indo-Chinese"]],
  [["Sizzling Tandoori", "Naan"], ["Biryani & Pulav"]],
  [["Vegetable Curries"], ["Non-Veg Curries"]],
  [["Breakfast"], ["Drinks & Desserts"]]
];
const placed = PAGES.flat(2);

/* One photo under each page's masthead. Pages 2 and 3 borrow dishes from
   elsewhere until there are photos of biryani, tandoori and a curry. */
const PHOTOS = [
  { src: "samosa.jpg", caption: "Samosa" },
  { src: "gobi-manchurian.jpg", caption: "Gobi Manchurian" },
  { src: "medu-vada.jpg", caption: "Medu Vada" },
  { src: "gulab-jamun.jpg", caption: "Gulab Jamun" }
];
if (PHOTOS.length !== PAGES.length) throw new Error("need one photo per page");
const missing = Object.keys(MENU).filter((s) => !placed.includes(s));
if (missing.length) throw new Error("sections not placed on any page: " + missing.join(", "));

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function fmtTime(t) {
  const [h, m] = t.split(":").map(Number);
  return `${((h + 11) % 12) + 1}${m ? ":" + String(m).padStart(2, "0") : ""}${h >= 12 ? "pm" : "am"}`;
}

function hoursLine() {
  /* Monday-first, the way people read a week. */
  const week = [...CONFIG.hours.slice(1), CONFIG.hours[0]];
  const open = week.filter((h) => h.open);
  const closed = week.filter((h) => !h.open).map((h) => h.day);
  const same = open.every((h) => h.open === open[0].open && h.close === open[0].close);
  const run = open.length && week.indexOf(open.at(-1)) - week.indexOf(open[0]) === open.length - 1;
  if (same && run) {
    const days = open.length === 7 ? "Open daily" : `${open[0].day} – ${open.at(-1).day}`;
    const shut = closed.length ? ` · Closed ${closed.join(", ")}` : "";
    return `${days} ${fmtTime(open[0].open)} – ${fmtTime(open[0].close)}${shut}`;
  }
  return week.map((h) => `${h.day.slice(0, 3)} ${h.open ? fmtTime(h.open) + "–" + fmtTime(h.close) : "closed"}`).join(" · ");
}

function dish(d) {
  const marks = [d.veg ? "V" : "", d.hot ? "S" : ""].filter(Boolean).map((m) => `<span class="mk">${m}</span>`).join("");
  const price = d.price == null ? `<span class="price ask">Ask your server</span>` : `<span class="price">${d.price.toFixed(2)}</span>`;
  return `<article class="dish">
    ${d.tag ? `<span class="tag">${esc(d.tag)}</span>` : ""}
    <h3>${esc(d.name)} ${price}${marks}</h3>
    <p>${esc(d.desc)}</p>
  </article>`;
}

function photo({ src, caption }) {
  return `<figure class="photo"><img src="../images/${src}" alt="${esc(caption)}"><figcaption>${esc(caption)}</figcaption></figure>`;
}

function section(name) {
  const { items, note } = MENU[name];
  /* Heading travels with its first dish so a column never ends on a bare title. */
  const [first, ...rest] = items;
  return `<section class="sec${items.length <= 6 ? " whole" : ""}">
    <div class="keep">
      <h2>${esc(name)}</h2>
      ${note ? `<p class="note">${esc(note)}</p>` : ""}
      ${dish(first)}
    </div>
    ${rest.map(dish).join("")}
  </section>`;
}

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Amma's Indian Cuisine Menu</title>
<link rel="stylesheet" href="fonts.css">
<style>
/* Print edition of the site's tasting-menu setting: centred dishes, tracked caps, italic descriptions, brass prices. */
:root {
  --ink: #171614;
  --soft: #6d6862;
  --hair: #e3ded7;
  --brass: #94661c;
  --display: "Libre Caslon Display", Georgia, serif;
  --serif: "Libre Caslon Text", Georgia, serif;
  --sans: "Hanken Grotesk", "Helvetica Neue", Arial, sans-serif;
}
@page { size: 8.5in 11in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; background: #ffffff; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: var(--sans); }
h1, h2, h3, p { margin: 0; font-weight: 400; }

.sheet {
  width: 8.5in;
  height: 11in;
  padding: 0.5in 0.55in 0.45in;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  break-after: page;
  position: relative;
}
.sheet:last-child { break-after: auto; }
.sheet::before {
  content: "";
  position: absolute;
  inset: 0.24in;
  border: 0.75pt solid var(--ink);
  pointer-events: none;
}

.mast { text-align: center; display: grid; gap: 4pt; justify-items: center; margin-bottom: 16pt; }
.mast h1 { font-family: var(--display); font-size: 40pt; line-height: 1; letter-spacing: 0.01em; }
.mast .sub { font: 500 7.6pt/1.4 var(--sans); letter-spacing: 0.36em; text-transform: uppercase; color: var(--soft); }
.mast .rule { width: 30pt; height: 0.75pt; background: var(--brass); margin: 9pt 0 6pt; }
.mast .motto { font-family: var(--serif); font-style: italic; font-size: 10pt; color: var(--soft); }
.mast.small { margin-bottom: 14pt; }
.photo { margin: 6pt 0 0; display: grid; justify-items: center; gap: 2pt; }
.photo img { height: 0.95in; width: auto; display: block; mix-blend-mode: multiply; }
.photo figcaption { font: italic 400 7pt/1.3 var(--serif); color: var(--soft); }
.mast:not(.small) .photo img { height: 0.85in; }
/* The back page also carries hours and address, so it sets a little tighter. */
.last .photo img { height: 0.7in; }
.last .dish { padding-bottom: 8.5pt; }
.mast.small h1 { font-size: 22pt; }

.cols {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 0.5in;
}
.col { min-height: 0; overflow: hidden; }
.col + .col { border-left: 0.5pt solid var(--hair); padding-left: 0.5in; margin-left: -0.25in; }
.col:first-child { padding-right: 0.25in; }
.sec { text-align: center; }
.sec + .sec { margin-top: 22pt; }
.keep, .whole { break-inside: avoid; }
.sec h2 {
  font: 500 9pt/1.3 var(--sans);
  letter-spacing: 0.34em;
  text-transform: uppercase;
  padding-top: 2pt;
}
.sec h2::after { content: ""; display: block; width: 18pt; height: 0.75pt; background: var(--brass); margin: 7pt auto 10pt; }
.note { font-family: var(--serif); font-style: italic; font-size: 8.2pt; line-height: 1.3; color: var(--brass); margin: -3pt auto 9pt; max-width: 3.1in; }

.dish { break-inside: avoid; display: grid; justify-items: center; gap: 1.4pt; padding-bottom: 10.5pt; }
.tag { font: 500 6.2pt/1.3 var(--sans); letter-spacing: 0.24em; text-transform: uppercase; color: var(--brass); }
.dish h3 { font: 500 8.8pt/1.35 var(--sans); letter-spacing: 0.16em; text-transform: uppercase; }
.dish h3 .price, .dish h3 .mk { margin-left: 4pt; text-transform: none; }
.dish p { font-family: var(--serif); font-style: italic; font-size: 9.4pt; line-height: 1.36; color: var(--soft); max-width: 3.1in; }
.price { font: 500 8.9pt/1.35 var(--sans); letter-spacing: 0.06em; color: var(--brass); font-variant-numeric: tabular-nums; }
.price.ask { font: italic 400 8.8pt/1.35 var(--serif); letter-spacing: 0; }
.mk { font: 500 6pt/1 var(--sans); letter-spacing: 0.1em; color: var(--soft); border: 0.5pt solid var(--hair); padding: 1.2pt 2pt 1pt; }

.foot {
  margin-top: 8pt;
  padding-top: 8pt;
  border-top: 0.5pt solid var(--hair);
  text-align: center;
  display: grid;
  gap: 2.5pt;
  font: 400 7.4pt/1.5 var(--sans);
  color: var(--soft);
}
.foot b { font-weight: 500; color: var(--ink); letter-spacing: 0.2em; text-transform: uppercase; font-size: 7.2pt; }
</style>
</head>
<body>
${PAGES.map((secs, i) => {
  const first = i === 0, last = i === PAGES.length - 1;
  const mast = first
    ? `<header class="mast">
      <h1>Amma's</h1>
      <span class="sub">Curated Indian Cuisine</span>
      <span class="rule"></span>
      <p class="motto">Every dish is served with love, tradition, and a little taste of home.</p>
      ${photo(PHOTOS[i])}
    </header>`
    : `<header class="mast small"><h1>Amma's</h1><span class="rule"></span>${photo(PHOTOS[i])}</header>`;
  const foot = last
    ? `<b>${esc(hoursLine())}</b>
      <span>${CONFIG.address.map(esc).join(", ")} &nbsp;·&nbsp; ${esc(CONFIG.phone)} &nbsp;·&nbsp; ${esc(CONFIG.email)} &nbsp;·&nbsp; V vegetarian &nbsp;·&nbsp; S spicy</span>`
    : `<span>V vegetarian &nbsp;·&nbsp; S spicy &nbsp;·&nbsp; Spice level adjusted on request &nbsp;·&nbsp; Please tell us about any allergies</span>`;
  return `<div class="sheet${last ? " last" : ""}" id="page-${i + 1}">
    ${mast}
    <div class="cols">${secs.map((col) => `<div class="col">${col.map(section).join("")}</div>`).join("")}</div>
    <footer class="foot">${foot}</footer>
  </div>`;
}).join("\n")}
</body>
</html>
`;

const htmlPath = resolve(here, "menu.html");
writeFileSync(htmlPath, html);

const { chromium } = createRequire(import.meta.url)("playwright");
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(pathToFileURL(htmlPath).href);
await page.evaluate(() => document.fonts.ready);

/* A column whose content is taller than the page would be clipped. */
const overflow = await page.evaluate(() => [...document.querySelectorAll(".col")].map((c, i) => ({
  side: `${c.closest(".sheet").id} column ${(i % 2) + 1}`,
  over: c.scrollHeight - c.clientHeight,
  spare: c.clientHeight - [...c.children].reduce((h, el) => Math.max(h, el.offsetTop + el.offsetHeight - c.offsetTop), 0)
})));
console.log(overflow.map((o) => `${o.side}: ${o.over > 1 ? "OVER " + o.over : o.spare + "px spare"}`).join("\n"));
const bad = overflow.filter((o) => o.over > 1);
if (bad.length) {
  await browser.close();
  throw new Error("menu does not fit: " + bad.map((o) => `${o.side} overflows by ${o.over}px`).join("; "));
}

await page.pdf({ path: resolve(here, "menu.pdf"), width: "8.5in", height: "11in", printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log("wrote print/menu.html and print/menu.pdf");
