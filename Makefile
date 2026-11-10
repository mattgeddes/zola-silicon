# zola-silicon — build helpers
#
# `make build` regenerates the generated files before invoking Zola. There is no
# Zola plugin for this: Zola renders templates only when a page claims them, with
# two special cases (sitemap.xml and robots.txt), so anything else has to exist
# on disk before the build starts.

ZOLA       ?= zola
PYTHON     ?= python3

# Site root and script location. A site that consumes this repository as a
# theme overrides THEME_DIR (and possibly PYTHON) on the command line or in its
# own Makefile, e.g.:
#
#     make build THEME_DIR=themes/zola-silicon
THEME_DIR  ?= .

.PHONY: all build serve check llms og theme clean distclean

all: build

## Regenerate the generated files, then build.
build: llms og theme
	$(ZOLA) build

## Regenerate the generated files, then serve with live reload.
serve: llms og theme
	$(ZOLA) serve

## Fail if anything generated is stale. Use in CI.
check: llms og theme
	$(PYTHON) $(THEME_DIR)/scripts/generate-theme-toml.py --check
	$(PYTHON) $(THEME_DIR)/scripts/generate-llms.py --check
	$(PYTHON) $(THEME_DIR)/scripts/generate-og.py --check

llms:
	$(PYTHON) $(THEME_DIR)/scripts/generate-llms.py --site-root .

og:
	$(PYTHON) $(THEME_DIR)/scripts/generate-og.py --site-root .

theme:
	$(PYTHON) $(THEME_DIR)/scripts/generate-theme-toml.py

clean:
	$(ZOLA) clean
	rm -f static/llms.txt static/llms-full.txt
	rm -rf static/og

distclean: clean
	rm -rf public .zola-cache
