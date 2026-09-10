---
type: Template
title: "Project starter: agent instructions for a catalog-driven DCA project"
tags: [template, bootstrap, governance]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/archunit-governance/core-rule-categories.md, /guide/readme/java-package-structure.md]
applies_to: [language-neutral]
framework: [framework-neutral]
---

A drop-in instructions block for a **new project** so a coding agent (any LLM,
any harness) builds it *from this catalog* instead of from memory. Use together
with [Bootstrap a new application](/recipe/bootstrap-a-new-application.md).

Append the block to wherever your agent reads its project instructions —
`AGENTS.md`, a system prompt, or your tool's equivalent — and make the catalog
available to the agent (a local copy of this bundle; note its path in the same
file).

## Agent instructions block

```markdown
## Architecture: Domain-Centric Architecture (DCA)

This project follows DCA, governed by ArchUnit (`./gradlew test-architecture`).
The DCA knowledge catalog (an OKF markdown graph) lives at: `{catalog-path}`.

**Before constructing anything** (aggregate, use case, adapter, event, context),
work from the catalog, not from memory:

1. Route via the task router (`recipe/build-a-dca-application.md`)
2. Resolve the "Decide first" forks (entity-vs-VO, repository-vs-store, …)
3. Generate from the linked template, satisfying the recipe's rule checklist
4. Verify with `./gradlew test-architecture`

Never invent DCA conventions from memory — if the catalog doesn't cover it,
say so explicitly and record the resolved answer (as a project note or ADR)
instead of silently improvising.
```

Replace `{catalog-path}` with the location of the catalog copy in the project
(keep the copy out of version control and refresh it from its source; commit
only the path reference).

## Anchors

- Recipe: [Bootstrap a new application](/recipe/bootstrap-a-new-application.md) · [Build a DCA application](/recipe/build-a-dca-application.md) (task router)
- Governance: [Core rule categories](/guide/archunit-governance/core-rule-categories.md)
- Structure the agent will build: [Java package structure](/guide/readme/java-package-structure.md)
- Recording decisions along the way: [Creating an ADR](/process/creating-an-adr.md)
