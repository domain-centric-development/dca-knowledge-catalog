PY := PYTHONPATH=src python3

.PHONY: help generate lint test check hooks obsidian obsidian-import
help:
	@echo "generate         regenerate bundle/ (+ mirror to dca-core plugin)"
	@echo "lint             health check (broken links, stale resources, orphans, tags)"
	@echo "test             run conformance tests"
	@echo "check            CI gate: generate(no mirror) + lint + test + freshness diff"
	@echo "hooks            install the git pre-commit hook"
	@echo "obsidian         export a browsable Obsidian vault to bundle-obsidian/"
	@echo "obsidian-import  write edits to owning authored/ sources and regenerate"

generate:
	$(PY) -m dca_catalog.generate

obsidian:
	$(PY) -m dca_catalog.obsidian

obsidian-import:
	$(PY) -m dca_catalog.obsidian --import
	$(PY) -m dca_catalog.generate
	$(PY) -m dca_catalog.lint

lint:
	$(PY) -m dca_catalog.lint

test:
	$(PY) -m pytest tests/ -q

check:
	./scripts/check.sh

hooks:
	./scripts/install-hooks.sh
