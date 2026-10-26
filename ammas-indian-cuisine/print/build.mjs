/**
 * Builds the printed two-sided menu (US Letter, front and back) from the
 * website's own CONFIG and MENU, so the paper menu and the site never drift.
 *
 *   node ammas-indian-cuisine/print/build.mjs
 *
 * Writes print/menu.html and print/menu.pdf. Fails if either side overflows
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

/* Which sections go on which side. Front ~39 dishes, back ~37. */
const FRONT = ["Appetizers", "65 & Indo-Chinese", "Sizzling Tandoori", "Biryani & Pulav", "Vegetable Curries"];
const BACK = ["Non-Veg Curries", "Naan", "Breakfast", "Drinks & Desserts"];
const missing = Object.keys(MENU).filter((s) => !FRONT.includes(s) && !BACK.includes(s));
if (missing.length) throw new Error("sections not placed on either side: " + missing.join(", "));

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

.mast { text-align: center; display: grid; gap: 3pt; justify-items: center; margin-bottom: 14pt; }
.mast h1 { font-family: var(--display); font-size: 30pt; line-height: 1; letter-spacing: 0.01em; }
.mast .sub { font: 500 6.6pt/1.4 var(--sans); letter-spacing: 0.36em; text-transform: uppercase; color: var(--soft); }
.mast .rule { width: 26pt; height: 0.75pt; background: var(--brass); margin: 7pt 0 5pt; }
.mast .motto { font-family: var(--serif); font-style: italic; font-size: 8.6pt; color: var(--soft); }
.mast.small h1 { font-size: 20pt; }

.cols {
  flex: 1;
  min-height: 0;
  columns: 3;
  column-gap: 0.3in;
  column-rule: 0.5pt solid var(--hair);
  column-fill: balance;
}
.sec { text-align: center; }
.sec + .sec { margin-top: 15pt; }
.keep, .whole { break-inside: avoid; }
.sec h2 {
  font: 500 7.8pt/1.3 var(--sans);
  letter-spacing: 0.34em;
  text-transform: uppercase;
  padding-top: 2pt;
}
.sec h2::after { content: ""; display: block; width: 18pt; height: 0.75pt; background: var(--brass); margin: 5pt auto 7pt; }
.note { font-family: var(--serif); font-style: italic; font-size: 6.9pt; line-height: 1.3; color: var(--brass); margin: -2pt auto 6pt; }

.dish { break-inside: avoid; display: grid; justify-items: center; gap: 0.8pt; padding-bottom: 7.6pt; }
.tag { font: 500 5.4pt/1.3 var(--sans); letter-spacing: 0.24em; text-transform: uppercase; color: var(--brass); }
.dish h3 { font: 500 7.2pt/1.35 var(--sans); letter-spacing: 0.15em; text-transform: uppercase; }
.dish h3 .price, .dish h3 .mk { margin-left: 3pt; text-transform: none; }
.dish p { font-family: var(--serif); font-style: italic; font-size: 7.6pt; line-height: 1.32; color: var(--soft); }
.price { font: 500 7.3pt/1.35 var(--sans); letter-spacing: 0.06em; color: var(--brass); font-variant-numeric: tabular-nums; }
.price.ask { font: italic 400 7.2pt/1.35 var(--serif); letter-spacing: 0; }
.mk { font: 500 5.2pt/1 var(--sans); letter-spacing: 0.1em; color: var(--soft); border: 0.5pt solid var(--hair); padding: 1.2pt 2pt 1pt; }

.foot {
  margin-top: 8pt;
  padding-top: 8pt;
  border-top: 0.5pt solid var(--hair);
  text-align: center;
  display: grid;
  gap: 2.5pt;
  font: 400 6.6pt/1.45 var(--sans);
  color: var(--soft);
}
.foot b { font-weight: 500; color: var(--ink); letter-spacing: 0.2em; text-transform: uppercase; font-size: 6.2pt; }
</style>
</head>
<body>
  <div class="sheet" id="front">
    <header class="mast">
      <h1>Amma's</h1>
      <span class="sub">Curated Indian Cuisine</span>
      <span class="rule"></span>
      <p class="motto">Every dish is served with love, tradition, and a little taste of home.</p>
    </header>
    <div class="cols">${FRONT.map(section).join("")}</div>
    <footer class="foot">
      <span>V vegetarian &nbsp;·&nbsp; S spicy &nbsp;·&nbsp; Spice level adjusted on request &nbsp;·&nbsp; Please tell us about any allergies</span>
    </footer>
  </div>
  <div class="sheet" id="back">
    <header class="mast small">
      <h1>Amma's</h1>
      <span class="rule"></span>
    </header>
    <div class="cols">${BACK.map(section).join("")}</div>
    <footer class="foot">
      <b>${esc(hoursLine())}</b>
      <span>${CONFIG.address.map(esc).join(", ")} &nbsp;·&nbsp; ${esc(CONFIG.phone)} &nbsp;·&nbsp; ${esc(CONFIG.email)}</span>
      <span>V vegetarian &nbsp;·&nbsp; S spicy &nbsp;·&nbsp; Thank you for dining with us</span>
    </footer>
  </div>
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

/* A multicol box that is too short pushes extra columns out sideways. */
const overflow = await page.evaluate(() => [...document.querySelectorAll(".cols")].map((c) => ({
  side: c.closest(".sheet").id,
  over: c.scrollWidth - c.clientWidth,
  spare: c.clientHeight
})));
const bad = overflow.filter((o) => o.over > 1);
if (bad.length) {
  await browser.close();
  throw new Error("menu does not fit: " + bad.map((o) => `${o.side} side overflows by ${o.over}px`).join("; "));
}

await page.pdf({ path: resolve(here, "menu.pdf"), width: "8.5in", height: "11in", printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log("wrote print/menu.html and print/menu.pdf");
