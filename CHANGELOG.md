# Changelog

All notable changes to **zola-silicon**, the template. This project follows
[Semantic Versioning](https://semver.org/); the template's own API is its
`templates/`, its `data/icons.toml` and its `theme.toml`.

## 0.8.0

The "consumable as a theme" release. Everything below is about this repository
working for someone else's Zola site, plus two additions.

### Added

- **`theme.toml`**, generated from the `[extra]` section of `config.toml`.
  Zola only reads `[extra]` from a theme's `theme.toml` and never reads a
  theme's `config.toml` at all, so the two are kept in step by
  `scripts/generate-theme-toml.py`. `--check` exits non-zero when stale.
- **`[extra.brand] logo`.** Set a path and the header and footer render it
  instead of the built-in mark.
- **`[extra] icon_data_path`.** Controls where `data/icons.toml` is loaded
  from, so a site consuming this repository as a theme can point at the
  theme's copy instead of copying it.
- **`llms.txt` and `llms-full.txt`**, generated into `static/` by
  `scripts/generate-llms.py`. Legal pages are excluded. Both are gitignored
  and regenerated on each build.
- **Blog tags.** `[[taxonomies]] name = "tags"`, `[taxonomies] tags` in post
  front matter, `templates/taxonomy_list.html` and
  `templates/taxonomy_single.html`, tag chips on posts, and a topic index at
  `/tags/`.
- **Six brand marks** in `data/icons.toml`: `x`, `mastodon`, `github`,
  `bluesky`, `linkedin` and `nostr`, alongside the existing hand-drawn `rss`.
- **`Makefile`** with `build`, `serve`, `check`, `llms`, `theme` and `clean`.
- **Version string** in `[extra]`, shown in the footer.

### Fixed

- `templates/llms.txt` and friends are not rendered by Zola at all; anything
  generated from content now happens before the build.
- `templates/sitemap.xml` read `config.toml` with `load_data`, which bypasses
  the `theme.toml` merge entirely and crashed for any site that did not
  redeclare `[extra.sections]`. It now filters when the site declares them and
  otherwise emits everything.
- Optional `[extra]` keys no longer fail the build. `index.html` read
  `section.extra.hero` and friends before its own `{% if %}` guards.
- The section gate resolved an absent `[extra.sections]` to `""`, and `in` on a
  string tests for substrings, which would have gated the entire site. It now
  resolves to an empty list.

### Changed

- `theme = "<name>"` must be a bare directory name: Zola prepends `themes/`
  itself, so `themes/foo` looks for `themes/themes/foo`.
- Renamed from `zola-biz` to `zola-silicon`.

### Notes for consumers

Three things a theme cannot supply, which your own `config.toml` must declare:

- `theme = "zola-silicon"` (a bare directory name)
- `[[taxonomies]] name = "tags"`, if you want tags
- `[extra] icon_data_path`, or a copy of `data/icons.toml`

### Licence

Brand marks `x`, `mastodon`, `github` and `bluesky` come from
[Simple Icons](https://simpleicons.org/) (CC0 1.0). `linkedin` and `nostr` are
hand-drawn placeholders, because Simple Icons removed the LinkedIn mark for
trademark reasons and has no Nostr mark. See `LICENSE-ARTWORK.md`.

## 0.7.0 and earlier

Development history before this file existed. The template landed with the
sample site, the design system, the four optional sections and the light/dark
theming.