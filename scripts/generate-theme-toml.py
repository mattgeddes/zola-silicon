#!/usr/bin/env python3
"""Generate theme.toml from the [extra] section of config.toml.

Zola only reads the [extra] table of a theme's theme.toml, and it never reads a
theme's config.toml at all. So everything this theme configures has to exist in
theme.toml as well. Keeping the two in step by hand invites drift, so this
script derives one from the other.

    python3 scripts/generate-theme-toml.py          # write theme.toml
    python3 scripts/generate-theme-toml.py --check  # fail if it is stale (CI)

Exit status is non-zero on --check when the committed file is out of date, so a
CI job can simply be:

    python3 scripts/generate-theme-toml.py --check
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config.toml"
THEME = ROOT / "theme.toml"

HEADER = """\
# theme.toml - defaults for sites that use this repository as a Zola theme.
#
# GENERATED FILE - do not edit by hand.
# Source: the [extra] section of config.toml
# Regenerate: python3 scripts/generate-theme-toml.py
# Verify:     python3 scripts/generate-theme-toml.py --check
#
# How Zola uses this file
# -----------------------
# Zola reads ONLY the [extra] table below. Any other key in this file is
# ignored. The theme's config.toml is never read at all, which is why every
# value this template's templates read has to appear here.
#
# Your site overrides these defaults in its own config.toml:
#
#     theme = "your-theme-dir"        # a bare directory name, not "themes/..."
#
#     [extra.brand]
#     name = "Your Company"           # wins; everything else is inherited
#
# Nested tables merge key by key. Arrays of tables - nav, footer_links,
# social - do NOT merge: your site either supplies the whole list or inherits
# the whole list, never a blend of the two. Giving a theme default a different
# TOML type to the one you set is a hard build error, so keep the shapes the
# same.
"""

TABLE_RE = re.compile(r"^\[+\s*([A-Za-z_][\w.-]*)")


def extract_extra(text: str) -> str:
    """Return the [extra] portion of a config.toml, comments and all."""
    out, capturing = [], False
    for line in text.split("\n"):
        match = TABLE_RE.match(line)
        if match:
            name = match.group(1)
            capturing = name == "extra" or name.startswith("extra.")
            if capturing:
                out.append(line)
            continue
        if capturing:
            out.append(line)
    # Trim leading/trailing blank lines so the output is tidy.
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out)


def main() -> int:
    if not CONFIG.exists():
        print(f"error: {CONFIG} not found", file=sys.stderr)
        return 2

    body = extract_extra(CONFIG.read_text())
    if not body:
        print("error: no [extra] section found in config.toml", file=sys.stderr)
        return 2

    rendered = HEADER + body + "\n"

    if "--check" in sys.argv:
        current = THEME.read_text() if THEME.exists() else ""
        if current == rendered:
            print("theme.toml is up to date")
            return 0
        print(
            "theme.toml is STALE - it no longer matches the [extra] section of\n"
            "config.toml. Run: python3 scripts/generate-theme-toml.py",
            file=sys.stderr,
        )
        return 1

    THEME.write_text(rendered)
    tables = sum(1 for line in body.split("\n") if TABLE_RE.match(line))
    print(f"wrote {THEME.relative_to(ROOT)} ({tables} tables, {len(body.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())