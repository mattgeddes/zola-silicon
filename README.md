# zola-biz

A website template for small tech products and tech services, built for the
[Zola](https://www.getzola.org/) static site generator.

It ships as a **working sample site** for a fictional company ("Kestrel", an
observability and edge-tooling startup) so you can see every feature in place
before you strip it out.

- Sleek, modern design system in plain CSS — no build step, no framework
- Light and dark themes, both first-class, with a system-preference default
- Responsive from 360px phones to ultrawide desktops
- Four optional sections — **Products, Services, Blog, Contact** — each with a
  single on/off switch
- A landing page that is entirely driven by front matter, so you can redesign
  it without touching a template
- Accessible by default: semantic landmarks, visible focus rings, a skip link,
  `prefers-reduced-motion` support and a working no-JS path

## Requirements

Zola 0.20 or newer. Nothing else — no Node, no Sass, no package manager.

```sh
zola serve      # live-reloading preview on http://localhost:1111
zola build      # writes to public/
```

## Quick start

1. Point `base_url` at your own domain in `config.toml`.
2. Edit `content/_index.md` — that file *is* the home page.
3. Edit the `[extra.brand]` block in `config.toml` for the name and colours.
4. Replace the contact details and footer columns further down the same file.
5. Switch off whatever you don't need (see below).
6. Replace the sample copy, graphics and legal pages with your own.
7. `zola build` and deploy `public/`.

## Turning sections on and off

Everything you are likely to want to change is in `config.toml`. The four
sections are controlled here:

```toml
[extra.sections]
products = true
services = true
blog = true
contact = true
```

Setting one to `false`:

- removes it from the header navigation and the footer,
- drops its URLs from `sitemap.xml`,
- and makes any direct URL to one of its pages return the visitor to the home
  page with a `noindex` header, rather than serving a page you have switched
  off.

Zola has to generate a file for every content page, so "switched off" is a
rendering decision rather than a deletion. If you want the content gone from
the repository as well, delete its folder under `content/`.

One thing the switch does *not* do: rewrite links you wrote in your own copy.
The sample home page has buttons and feature cards pointing at `/products/` and
`/contact/`; grep your content for the section name after switching one off.

### Navigation

`[[extra.nav]]` controls the header links and their order. An entry with a
`key` is only rendered when that key is enabled above; an entry without a `key`
is always shown, which is how the `#faq` anchor link stays put.

```toml
[[extra.nav]]
key = "products"     # must match a key in [extra.sections]
label = "Products"
url = "/products/"
```

## The home page is data, not template

`content/_index.md` holds an array of blocks and `templates/index.html` renders
whatever it finds. Each block is optional — delete it and the section
disappears.

| Block | What it renders |
| --- | --- |
| `[extra.hero]` | Headline, text, buttons, trust badges and an illustration, plus a floating stat card |
| `[extra.logos]` | "Used by" logo strip |
| `[extra.features]` | Eyebrow + heading + grid of cards, each optionally with a link |
| `[extra.steps]` | Numbered "how it works" row |
| `[extra.split]` | Image beside a checklist, with the image optionally on the left |
| `[extra.latest]` | The three most recent blog posts |
| `[extra.faq]` | Native `<details>` accordion, no JavaScript needed |
| `[extra.newsletter]` | Email capture block |
| `[extra.cta]` | Closing call-to-action band |

Within the blocks, `icon` values are names from `data/icons.toml` (see below)
and `variant` is `primary`, `secondary` or `ghost`.

## Writing content

Zola-specific front matter only supports a fixed set of root fields — `title`,
`description`, `date`, `weight`, `sort_by`, `paginate_by`, `template`,
`generate_feeds` and friends. **Anything custom must go under `[extra]`**, or
it is silently dropped:

```toml
+++
title = "Kestrel Relay"
description = "One line used for the card, the <meta> tag and the social card."
weight = 2
template = "products/page.html"   # optional; see below

[extra]
icon = "bolt"
price = "From $19/mo"
cta_label = "Start a 30-day trial"
facts = ["Grouping", "On-call routing"]
+++
```

### Templates

Zola does not look in `templates/<section>/` automatically. If you want a
section to use its own template, name it in the front matter:

```toml
template = "blog/page.html"     # a post inside content/blog/
template = "blog/section.html"  # the index of content/blog/
```

The sample content already does this. Copy `content/blog/*.md` as a starting
point for new posts and the line comes with it.

### Blog posts need a date

The blog sorts and paginates on `date`, and posts without one are skipped with
a warning. Every post also carries `paginate_by` on the section index:

```toml
# content/blog/_index.md
paginate_by = 3
generate_feeds = true
```

## Shortcodes

Four are included, in `templates/shortcodes/`.

Zola's shortcode syntax is easy to get wrong, so:

- A shortcode **with a body** opens with `{% name(args) %}` and closes with
  `{% end %}`. Angle brackets are not used.
- A shortcode **without a body** is `{{ name(args) }}`.
- Parentheses are mandatory either way.
- Arguments are named and quoted: `type="tip"`, never `type=tip`. Argument
  names may contain letters, digits and underscores only.

```md
Inline icons: {{ icon(name="bolt") }}

A button: {{ button(text="Get started", url="/contact/", variant="primary", icon="rocket") }}

{% callout(type="warning") %}
Hard ceilings need a floor that someone chose.
{% end %}

{{< video(src="/media/demo.mp4", poster="/images/demo.jpg", caption="...") >}}
```

Note that a shortcode body is emitted verbatim: write plain text or inline HTML
(`<strong>`, `<em>`, `<code>`), not Markdown. Avoid backticks in bodies too —
Zola's grammar uses them for quoted argument values.

## Icons

62 hand-drawn, stroke-based icons live in `data/icons.toml` as the inner markup
of a 24×24 `<svg>` that inherits `currentColor`. To add one, copy any entry and
edit the paths; to use one:

```md
{{ icon(name="bolt") }}
```

```jinja
{% import "partials/icons.html" as m %}
{{ m::icon(name="bolt", size=20) }}
```

An unknown name falls back to the help glyph rather than rendering an empty
box, so a typo is visible instead of silent.

## Colour themes

Both themes are driven by custom properties at the top of
`static/css/main.css`. `:root` holds the light palette, and the dark palette is
declared twice on purpose:

```css
:root[data-theme="dark"] { ... }                    /* explicit choice */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { ... }          /* no choice made yet */
}
```

A small inline script in `<head>` reads `localStorage.theme` and sets
`data-theme` before first paint, so there is no flash of the wrong theme. With
nothing stored, the site follows the operating system. The toggle in the header
cycles light/dark and remembers the choice; it also updates its `aria-label` and
keeps following OS changes while you have not made one.

### Recolouring the whole site

Edit the colour tokens in section 1 of `main.css` and their dark counterparts
in section 2. Nothing else needs touching. To go further, change
`primary` and `accent` under `[extra.brand]` in `config.toml`, which also drive
the inline logo and the favicon you regenerate in "Graphics" below.

## Graphics

All artwork was drawn for this template and is released **CC0** (public
domain) — see `LICENSE-ARTWORK.md`. Nothing is scraped from anywhere, so there
are no attribution requirements.

| File | Purpose |
| --- | --- |
| `static/images/hero-dashboard.svg` | Home page hero illustration |
| `static/images/split-architecture.svg` | "How it fits together" diagram |
| `static/images/posts/*.svg` | Blog post covers |
| `static/images/logos/*.svg` | Placeholder customer logos |
| `static/images/logo.svg` | Full lockup, for presentations and email |
| `static/favicon.svg` | Favicon, also the source for the PNG/ICO below |
| `static/og.png` | 1200×630 social card |
| `static/apple-touch-icon.png`, `static/icon-512.png` | PWA / home-screen icons |

The illustrations are dark panels on purpose: they read correctly against both
the light and the dark theme. The logo strip is flat mid-grey for the same
reason.

### Regenerating the raster icons

If you change the brand colours, redraw the favicon and rasterise it with
[`rsvg-convert`](https://gitlab.gnome.org/GNOME/librsvg):

```sh
cd static
rsvg-convert -w 180 -h 180 favicon.svg -o apple-touch-icon.png
rsvg-convert -w 512 -h 512 favicon.svg -o icon-512.png
convert -background none favicon.svg -define icon:auto-resize=48,32,16 favicon.ico
rsvg-convert -w 1200 -h 630 og.svg -o og.png
```

If you would rather not install anything, drop your own `favicon.svg`,
`favicon.ico`, `apple-touch-icon.png` and `og.png` into `static/` and reference
them from `templates/base.html`.

The social card is deliberately generic. Give a page its own image by
overriding the `og` block in that page's template:

```jinja
{% block og %}
<meta property="og:image" content="{{ config.base_url }}/images/posts/cover.svg">
{% endblock %}
```

## The newsletter form

The subscribe button is deliberately inert: a static site has nowhere to post
to. Submitting it explains as much instead of silently failing. Wire it up by
setting a `action` on the `<form>` in `templates/partials/ui.html` and dropping
the `data-newsletter` attribute (which is what the demo handler keys off), or
replace the macro with your provider's embed. If you have no newsletter, delete
the `[extra.newsletter]` block and the form goes with it.

## Before you launch

The sample site is a demo, not a real business. Replace:

- `content/privacy.md` and `content/terms.md` — they are placeholders that say
  so. Have them reviewed for your jurisdiction.
- `base_url` in `config.toml`.
- `copyright_year` in `config.toml` (bump it each January).
- The `[[extra.social]]` entries. The icons are generic on purpose; swap in
  official brand marks for the networks you actually use.
- The newsletter form.
- The sample copy in every content file.

Then turn on HTML minification for production:

```toml
minify_html = true
```

## Project layout

```
config.toml              all site-level settings, including the section switches
content/
  _index.md              the home page, as data
  products/  services/  blog/
  contact.md  privacy.md  terms.md
data/
  icons.toml             the icon library
templates/
  base.html              document shell, <head>, and the section gate
  index.html             home page blocks
  section.html           generic listing (products, services)
  blog/section.html      paginated post list
  blog/page.html         a single post
  page.html              generic interior page
  contact.html           contact page, details from [extra.contact]
  404.html
  partials/
    header.html  footer.html  logo.html
    icons.html    icons + buttons
    ui.html       cards, entries, FAQ, newsletter, CTA band
    heads.html    headings + pagination
    actions.html  front-matter-driven buttons
    svg.html      the only place an <svg> is built
  shortcodes/            icon, button, callout, video
  sitemap.xml            filters disabled sections out of Zola's own list
  robots.txt
static/
  css/main.css           the whole design system
  js/main.js             theme toggle, mobile nav, demo form handler
  images/  favicon.svg  og.png  …
```

## Notes for template authors

A few Zola 0.20 behaviours shaped this template and will trip you up if you
extend it. All of these are load-time errors rather than silent failures, which
is why the templates guard every optional field:

- **There is no `default` filter.** Use `{% if x is defined and x %}`.
- **Reading a field that does not exist fails the build.** Custom front matter
  has to be checked with `is defined` before use.
- **Macro arguments are named only**, and macros are invoked with `m::name()`
  rather than `m.name()`.
- **`self::macro` only resolves for macros invoked at the top level of a
  render**, which is why the partials reach for explicit aliases and why
  `svg.html` is kept import-free.
- **Iterating or indexing a table with a missing key is an error** — guard with
  `in` first.
- **`paginator.total_pages` is the number of items**, not pages. The page count
  is `number_pagers`.
- **`slice(limit=n)` is ignored**; use `slice(end=n)`.
- The home page has no `page` variable and the 404 template has neither
  `current_url` nor `current_path`, so both are guarded in `base.html`.
- **Content files are Markdown, not Tera.** A `{{ config.title }}` in
  `content/*.md` renders as literal text. Values a template and its content
  share go through `[extra]` in `config.toml`, which is how the contact page
  pulls its email and phone.
- `templates/sitemap.xml` and `robots.txt` receive only `entries` — they read
  `config.toml` with `load_data`.

## Licence

Template code is MIT (`LICENSE`). Artwork and icons are CC0
(`LICENSE-ARTWORK.md`). The sample content is fiction written for this
template; replace it.