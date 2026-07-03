---
type: Template
title: "Project starter: CLAUDE.md + conventions for a catalog-driven DCA project"
tags: [template, bootstrap, governance]
---

Drop-in files for a **new project** so a coding agent builds it *from this
catalog* instead of from memory. Use together with
[Bootstrap a new application](/recipe/bootstrap-a-new-application.md).

> **Automated path:** `/dca-bootstrap` (dca-core plugin) installs these two files
> itself — its "catalog wiring" decision appends the CLAUDE.md section and, for a
> live catalog, writes `conventions.md`. This template is the **manual fallback**
> for setups without the plugin's bootstrap run, and the canonical text the skill
> installs. Replace `{catalog-path}` only if you want the live catalog instead of
> the plugin's vendored snapshot.

## 1. One-time plugin install (per machine)

```
/plugin marketplace add <path-to>/dca-marketplace
/plugin install dca-core@dca-marketplace
/plugin install software-craftsmanship@dca-marketplace
```

The dca-core plugin ships a vendored copy of this catalog, so `/dca-knowledge`
works in any project with zero setup.

## 2. `CLAUDE.md` — architecture section (append to the project's CLAUDE.md)

```markdown
## Architecture: Domain-Centric Architecture (DCA)

This project follows DCA, governed by ArchUnit (`./gradlew test-architecture`).

**Before constructing anything** (aggregate, use case, adapter, event, context):
run the `/dca-knowledge build <thing>` loop — it reads the canonical OKF catalog:

1. Route via the task router (`recipe/build-a-dca-application.md`)
2. Resolve the "Decide first" forks (entity-vs-VO, repository-vs-store, …)
3. Generate from the linked template, satisfying the recipe's rule checklist
4. Verify with `./gradlew test-architecture`

Never invent DCA conventions from memory — if the catalog doesn't cover it,
say so, then `/dca-knowledge save` the resolved answer as a new catalog node.
Apply `/dca-discipline` while editing domain/application/adapter code;
run `/dca-review` before committing.
```

## 3. `.claude/dca/conventions.md` — optional live-catalog override

Only when the canonical catalog is regenerable on the same machine; otherwise
omit and the plugin's vendored snapshot is used (right default for teammates/CI).

```markdown
catalog_path: {catalog-path}/bundle
```

## Anchors

- Recipe: [Bootstrap a new application](/recipe/bootstrap-a-new-application.md) · [Build a DCA application](/recipe/build-a-dca-application.md) (task router)
- Governance: [ADR-015 ArchUnit Governance](/adr/adr-015-archunit-governance.md)
- Structure the agent will build: [Java package structure](/guide/readme/java-package-structure.md)
- Recording decisions along the way: [Creating an ADR](/process/creating-an-adr.md)
