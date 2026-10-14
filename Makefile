# zola-biz — build helpers
#
# `make build` regenerates the generated files before invoking Zola. There is no
# Zola plugin for this: Zola renders templates only when a page claims them, with
# two special cases (sitemap.xml and robots.txt), so anything else has to exist
# on disk before the build starts.

ZOLA       ?= zola
PYTHON     ?= python3

.PHONY: all build serve check llms theme clean distclean

all: build

## Regenerate the generated files, then build.
build: llms theme
	$(ZOLA) build

## Regenerate the generated files, then serve with live reload.
serve: llms theme
	$(ZOLA) serve

## Fail if anything generated is stale. Use in CI.
check: llms theme
	$(PYTHON) scripts/generate-theme-toml.py --check
	$(PYTHON) scripts/generate-llms.py --check

llms:
	$(PYTHON) scripts/generate-llms.py

theme:
	$(PYTHON) scripts/generate-theme-toml.py

clean:
	$(ZOLA) clean
	rm -f static/llms.txt static/llms-full.txt

distclean: clean
	rm -rf public .zola-cache