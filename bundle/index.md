# DCA Knowledge Catalog

Knowledge for building Domain-Centric Architecture applications. **Generated zone** (guide, marker, rule, process) is derived from the sources and rebuilt on every run; the implementation guide (full text) is the main body, the marker contracts and ArchUnit rules the skeleton it anchors to, and `reference/` describes the layout and discovery classes every rule is parameterised by. **Extensible zone** (recipe, decision, pitfall, template, note) is authored by a human or an LLM and survives regeneration. See `log.md`.

**Building something?** Start at [Build a DCA application](recipe/build-a-dca-application.md) — the task router mapping construction tasks to recipes.

- [decision/](decision/index.md) (20) — Decision guides for design forks (which pattern, when).
- [guide/](guide/index.md) (116) — The compact implementation guide — patterns, governance, supplementary guides (full text).
- [marker/](marker/index.md) (29) — Architectural marker interfaces — the contracts a new application implements.
- [note/](note/index.md) (1) — Compounded query answers — synthesis made permanent.
- [pitfall/](pitfall/index.md) (23) — Anti-patterns and the rules/ADRs that forbid them.
- [process/](process/index.md) (1) — How-to processes for keeping the architecture's conventions.
- [recipe/](recipe/index.md) (18) — Task playbooks — ordered steps to build a DCA construct.
- [reference/](reference/index.md) (2) — The two classes every rule is parameterised by — DcaLayout (settings, defaults, patterns) and DcaArchitecture (how contexts and modules are discovered).
- [rule/](rule/index.md) (120) — ArchUnit rules — the enforceable, machine-checkable architecture.
- [template/](template/index.md) (21) — Domain-free code skeletons to fill in.
