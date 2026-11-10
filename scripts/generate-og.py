#!/usr/bin/env python3
"""Generate per-page Open Graph images for a Zola site.

Zola has no built-in OG image generation, so this script renders a 1200x630
branded card for every content page and writes it into static/og/. Run it
before `zola build` (see the Makefile).

    python3 scripts/generate-og.py            # (re)generate all images
    python3 scripts/generate-og.py --check     # fail if any are missing/stale

The site root is detected the same way as generate-llms.py: the current
directory if it contains a config.toml, otherwise the script's own location.
Override with --site-root, --content or --output.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("error: Pillow is required (pip install Pillow)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
CONTENT: Path = ROOT / "content"
CONFIG: Path = ROOT / "config.toml"
OUT_DIR: Path = ROOT / "static"
OG_DIRNAME = "og"

WIDTH, HEIGHT = 1200, 630

# Palette (mirrors the theme tokens).
NAVY = (18, 33, 47)        # Midnight Navy
NAVY_2 = (29, 43, 56)
TEAL = (19, 124, 122)      # Secure Teal
CYAN = (57, 198, 214)      # Signal Cyan
PORCELAIN = (247, 248, 245)
MIST = (170, 180, 186)
GRAPHITE = (52, 65, 75)

FM_RE = re.compile(r"^[+-]{3}\s*$")
EXCLUDE_SLUGS = {"privacy", "terms", "404", "not-found"}


def parse_front_matter(text: str) -> tuple[dict, str]:
    lines = text.split("\n")
    if not lines or not FM_RE.match(lines[0]):
        return {}, text
    for i in range(1, len(lines)):
        if FM_RE.match(lines[i]):
            raw = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1 :])
            try:
                return tomllib.loads(raw), body
            except tomllib.TOMLDecodeError:
                return {}, body
    return {}, text


def slug_for(path: Path, content: Path) -> str:
    """Relative path under content, .md -> .png, _index -> index."""
    rel = path.relative_to(content).with_suffix("")
    parts = list(rel.parts)
    if parts and parts[-1] == "_index":
        parts[-1] = "index"
    return "/".join(parts) + ".png"


def wrap(draw, text, font, max_width):
    if not text:
        return []
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def find_font(bold: bool, size: int):
    candidates_bold = [
        "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    candidates_reg = [
        "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in (candidates_bold if bold else candidates_reg):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render(site_title: str, title: str, description: str) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(img)

    # Subtle vertical gradient.
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(NAVY[0] + (NAVY_2[0] - NAVY[0]) * t)
        g = int(NAVY[1] + (NAVY_2[1] - NAVY[1]) * t)
        b = int(NAVY[2] + (NAVY_2[2] - NAVY[2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Accent bar at the top.
    draw.rectangle([(0, 0), (WIDTH, 6)], fill=TEAL)

    pad = 72
    title_font = find_font(True, 62)
    desc_font = find_font(False, 26)
    brand_font = find_font(True, 22)
    url_font = find_font(False, 20)

    # Brand / site name, top-left.
    draw.text((pad, pad - 8), site_title.upper(), font=brand_font, fill=CYAN)

    # Title, wrapped.
    title_lines = wrap(draw, title or site_title, title_font, WIDTH - 2 * pad)
    title_lines = title_lines[:3]
    y = 150
    for line in title_lines:
        draw.text((pad, y), line, font=title_font, fill=PORCELAIN)
        y += 74

    # Description.
    if description:
        desc_lines = wrap(draw, description, desc_font, WIDTH - 2 * pad)
        desc_lines = desc_lines[:3]
        y += 12
        for line in desc_lines:
            draw.text((pad, y), line, font=desc_font, fill=MIST)
            y += 34

    # Bottom accent line + footer text.
    draw.rectangle([(pad, HEIGHT - 60), (pad + 64, HEIGHT - 56)], fill=TEAL)
    footer = site_title
    draw.text((pad, HEIGHT - 46), footer, font=url_font, fill=MIST)

    return img


def main() -> int:
    global CONTENT, CONFIG, OUT_DIR
    parser = argparse.ArgumentParser(description="Generate per-page Open Graph images.")
    parser.add_argument("--content", type=Path, default=None)
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--site-root", type=Path, default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.site_root is not None:
        root = args.site_root.resolve()
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
    site_title = cfg.get("title") or cfg.get("extra", {}).get("brand", {}).get("name", "This site")

    pages = []
    for path in sorted(CONTENT.rglob("*.md")):
        fm, _ = parse_front_matter(path.read_text(encoding="utf-8"))
        if fm.get("draft"):
            continue
        rel = path.relative_to(CONTENT).with_suffix("")
        parts = list(rel.parts)
        if parts and parts[-1] == "_index":
            parts = parts[:-1]
        slug = parts[-1] if parts else "index"
        if slug in EXCLUDE_SLUGS:
            continue
        pages.append((path, fm, slug))

    og_dir = OUT_DIR / OG_DIRNAME
    og_dir.mkdir(parents=True, exist_ok=True)

    expected = set()
    missing = []
    for path, fm, slug in pages:
        out_rel = slug_for(path, CONTENT)
        out_path = OUT_DIR / out_rel  # static/og/...png
        expected.add(out_path)
        title = fm.get("title") or site_title
        description = fm.get("description", "")
        img = render(site_title, title, description)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path, format="PNG", optimize=True)

    # Also keep a top-level static/og.png for the home page / fallback.
    home_candidates = [p for p in pages if p[2] == "index" or str(p[0].relative_to(CONTENT)) == "_index.md"]
    if home_candidates:
        home_img = render(site_title, home_candidates[0][1].get("title") or site_title,
                          home_candidates[0][1].get("description", ""))
        (OUT_DIR / "og.png").write_bytes(home_img.tobytes()) if False else home_img.save(OUT_DIR / "og.png", format="PNG", optimize=True)

    if args.check:
        # verify every expected file exists and is non-empty
        bad = [p for p in expected if not p.exists() or p.stat().st_size == 0]
        if bad:
            for p in bad:
                print(f"MISSING: {p}", file=sys.stderr)
            print(f"{len(bad)} missing image(s)", file=sys.stderr)
            return 1
        print(f"all {len(expected)} OG images present")
        return 0

    print(f"generated {len(pages)} OG images in {og_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
