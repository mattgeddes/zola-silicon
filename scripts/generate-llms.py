#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt for the site.

Zola renders templates only when a page claims them, with two special cases
(sitemap.xml and robots.txt). An arbitrary templates/llms.txt is silently
ignored, so these are produced here and written into static/, where Zola copies
them to the site root.

    python3 scripts/generate-llms.py     # writes static/llms.txt + llms-full.txt
    python3 scripts/generate-llms.py --check   # non-zero if stale (CI)

The script detects the site root on its own: if run from a directory that
contains a config.toml it treats that directory as the site, otherwise it falls
back to the directory the script lives in (so the sample site keeps working
with no flags). Override explicitly with --site-root, --content, --config or
--output.

A site that consumes this repository as a theme does not need to copy the
script: point at the theme's copy, e.g.

    python3 themes/zola-silicon/scripts/generate-llms.py --site-root .

Both files are gitignored; run this before `zola build` (see the Makefile).

Excluded from the output: legal pages, which are boilerplate rather than
context, and the 404 page. Drafts are skipped.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Resolved in main() from CLI args (or, by default, from the script location,
# which keeps the sample site working exactly as before).
CONTENT: Path = ROOT / "content"
CONFIG: Path = ROOT / "config.toml"
OUT_DIR: Path = ROOT / "static"
BASE_URL: str = "https://example.com"

# Pages whose content is boilerplate rather than useful context.
EXCLUDE_SLUGS = {"privacy", "terms", "404", "not-found"}

# Zola content files are delimited with +++ (--- is only used by Jekyll).
FM_RE = re.compile(r"^[+-]{3}\s*$")
CODE_FENCE_RE = re.compile(r"^```.*?^```", re.S | re.M)


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Split a Zola content file into (front matter, body)."""
    lines = text.split("\n")
    if not lines or not FM_RE.match(lines[0]):
        return {}, text
    for i in range(1, len(lines)):
        if FM_RE.match(lines[i]):
            raw = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1 :])
            try:
                return tomllib.loads(raw), body
            except tomllib.TOMLDecodeError as exc:
                print(f"  ! bad front matter: {exc}", file=sys.stderr)
                return {}, body
    return {}, text


def strip_markdown(md: str) -> str:
    """Reduce Markdown to readable prose.

    Deliberately conservative: it removes syntax that would read as noise in an
    LLM context but does not try to be a Markdown parser. Shortcode calls are
    dropped because they are template syntax, not content.
    """
    md = CODE_FENCE_RE.sub("\n", md)
    md = re.sub(r"\{\{[%<].*?[%>]\}\}", " ", md, flags=re.S)  # shortcodes
    md = re.sub(r"\{[%{].*?[%}]\}", " ", md, flags=re.S)      # leftover Tera
    md = re.sub(r"<!--.*?-->", " ", md, flags=re.S)          # comments
    md = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", md)        # images -> alt
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)          # links -> text
    md = re.sub(r"^#{1,6}\s*", "", md, flags=re.M)            # headings
    md = re.sub(r"^>\s?", "", md, flags=re.M)                 # blockquote
    md = re.sub(r"^\s*[-*+]\s+", "", md, flags=re.M)          # bullets
    md = re.sub(r"^\s*\d+\.\s+", "", md, flags=re.M)          # ordered
    md = re.sub(r"\*\*([^*]+)\*\*", r"\1", md)               # bold
    md = re.sub(r"(?<!\w)[*_]([^*_\n]+)[*_](?!\w)", r"\1", md)  # italic
    md = re.sub(r"`([^`]+)`", r"\1", md)                      # code spans
    md = re.sub(r"\|", " ", md)                               # tables
    md = re.sub(r"^[-=]{3,}$", "", md, flags=re.M)           # rules
    md = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def collect() -> list[dict]:
    """Every non-draft, non-excluded content page, in site order."""
    pages = []
    for path in sorted(CONTENT.rglob("*.md")):
        fm, body = parse_front_matter(path.read_text(encoding="utf-8"))
        if fm.get("draft"):
            continue
        rel = path.relative_to(CONTENT).with_suffix("")
        parts = list(rel.parts)
        if parts[-1] == "_index":
            parts = parts[:-1]
        url = BASE_URL.rstrip("/") + "/" + "/".join(parts) + "/" if parts else BASE_URL.rstrip("/") + "/"
        slug = parts[-1] if parts else "index"
        if slug in EXCLUDE_SLUGS:
            continue
        # Skip anything under a section whose own index is excluded.
        if any(p in EXCLUDE_SLUGS for p in parts):
            continue
        pages.append(
            {
                "title": fm.get("title") or slug,
                "description": fm.get("description", "") or "",
                "url": url,
                "slug": slug,
                "section": parts[0] if len(parts) > 1 else "",
                "date": str(fm.get("date", ""))[:10],
                "tags": fm.get("taxonomies", {}).get("tags", []) or [],
                "text": strip_markdown(body),
            }
        )
    return pages


def render_index(site: dict, pages: list[dict]) -> str:
    root = BASE_URL.rstrip("/")
    out = [
        f"# {site['title']}",
        "",
        f"> {site['description']}",
        "",
        f"Optional context for LLM assistants reading {root}. "
        "The full text of every page is in /llms-full.txt.",
        "",
    ]

    nav = site.get("nav", [])
    if nav:
        out += ["## Pages", ""]
        for item in nav:
            out.append(f"- [{item['label']}]({root}{item['url']})")
        out.append("")

    posts = [p for p in pages if p["slug"] not in EXCLUDE_SLUGS and p["date"]]
    if posts:
        out += ["## Writing", ""]
        for p in sorted(posts, key=lambda x: x["date"], reverse=True):
            tag = f" — {', '.join(p['tags'])}" if p["tags"] else ""
            desc = f": {p['description']}" if p["description"] else ""
            out.append(f"- [{p['title']}]({p['url']}){tag}{desc}")
        out.append("")

    # Everything else, grouped so products and services do not read as one blob.
    covered = {root + item["url"].rstrip("/") + "/" for item in nav}
    others = [
        p
        for p in pages
        if p["url"] not in covered
        and p["url"] not in {x["url"] for x in posts}
        and not p["slug"].endswith(".html")
    ]
    grouped: dict[str, list[dict]] = {}
    for p in others:
        grouped.setdefault(p["section"] or "Site", []).append(p)
    for section in sorted(grouped):
        out += [f"## {section}", ""]
        for p in sorted(grouped[section], key=lambda x: x["title"]):
            desc = f": {p['description']}" if p["description"] else ""
            out.append(f"- [{p['title']}]({p['url']}){desc}")
        out.append("")

    out += [
        "## Optional",
        "",
        f"- [Atom feed]({root}/blog/atom.xml)",
        f"- [Sitemap]({root}/sitemap.xml)",
        "",
    ]
    return "\n".join(out)


def render_full(site: dict, pages: list[dict]) -> str:
    out = [
        f"# {site['title']} — full text",
        "",
        f"> {site['description']}",
        "",
        f"Full text of the main pages of {BASE_URL}. Legal pages are omitted.",
        "",
        "---",
        "",
    ]
    for p in pages:
        out.append(f"## {p['title']}")
        out.append("")
        out.append(f"Source: {p['url']}")
        out.append("")
        if p["description"]:
            out += [p["description"], ""]
        if p["tags"]:
            out += ["Tags: " + ", ".join(p["tags"]), ""]
        out += [p["text"], "", "---", ""]
    return "\n".join(out)


def main() -> int:
    global BASE_URL, CONTENT, CONFIG, OUT_DIR
    parser = argparse.ArgumentParser(
        description="Generate llms.txt and llms-full.txt from a Zola site's content.",
    )
    parser.add_argument(
        "--content", type=Path, default=None,
        help="content directory (default: <site>/content)",
    )
    parser.add_argument(
        "--config", type=Path, default=None,
        help="config.toml (default: <site>/config.toml)",
    )
    parser.add_argument(
        "--output", type=Path, default=None,
        help="output directory (default: <site>/static)",
    )
    parser.add_argument(
        "--site-root", type=Path, default=None,
        help="site root; derives content/config/output from it (default: script location)",
    )
    parser.add_argument("--check", action="store_true", help="fail if stale (CI)")
    args = parser.parse_args()

    # Default site root: the current directory if it looks like a Zola site,
    # otherwise the directory the script lives in (keeps the sample site working
    # without any flags).
    if args.site_root is not None:
        root = args.site_root.resolve()
    elif (Path.cwd() / "config.toml").exists():
        root = Path.cwd()
    else:
        root = ROOT
    CONTENT = root / "content"
    CONFIG = root / "config.toml"
    OUT_DIR = root / "static"
    if args.content is not None:
        CONTENT = args.content.resolve()
    if args.config is not None:
        CONFIG = args.config.resolve()
    if args.output is not None:
        OUT_DIR = args.output.resolve()

    if not CONFIG.exists():
        print(f"error: {CONFIG} not found", file=sys.stderr)
        return 2
    cfg = tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    BASE_URL = cfg.get("base_url", BASE_URL)

    brand = cfg.get("extra", {}).get("brand", {})
    site = {
        "title": cfg.get("title") or brand.get("name", "This site"),
        "description": cfg.get("description", ""),
        "nav": cfg.get("extra", {}).get("nav", []),
    }

    pages = collect()
    index = render_index(site, pages)
    full = render_full(site, pages)

    targets = {"llms.txt": index, "llms-full.txt": full}
    stale = False
    for name, content in targets.items():
        path = OUT_DIR / name
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current == content:
            continue
        stale = True
        if args.check:
            print(f"{name} is STALE", file=sys.stderr)
        else:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    if args.check:
        if stale:
            print("Run: python3 scripts/generate-llms.py", file=sys.stderr)
            return 1
        print("llms.txt and llms-full.txt are up to date")
        return 0

    verb = "refreshed" if stale else "already up to date"
    print(f"{verb}: {len(pages)} pages -> {OUT_DIR}/llms.txt, {OUT_DIR}/llms-full.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())