# DCA Knowledge Catalog

Knowledge for building Domain-Centric Architecture applications. **Generated zone** (guide, marker, rule, process) is derived from the sources and rebuilt on every run; the implementation guide (full text) is the main body, the marker contracts and ArchUnit rules the skeleton it anchors to, and `reference/` describes the layout and discovery classes every rule is parameterised by. **Extensible zone** (recipe, decision, pitfall, template, note) is authored by a human or an LLM and survives regeneration. See `log.md`.

**Building something?** Start at [Build a DCA application](recipe/build-a-dca-application.md) — the task router mapping construction tasks to recipes.

**What `review:` means on an authored node.** `reviewed` — an owner and evidence have been verified. `draft` — written and wired into the graph, not yet through a review pass: usable, and it never overrides a generated node, because rules, markers and guide text are derived from the code and win on every contradiction. `superseded` — history; follow `superseded_by`. Most construction guidance is currently `draft`.

- [decision/](decision/index.md) (28) — Decision guides for design forks (which pattern, when).
- [evidence/](evidence/index.md) (125)
- [guide/](guide/index.md) (210) — The compact implementation guide — patterns, governance, supplementary guides (full text).
- [marker/](marker/index.md) (31) — Architectural marker interfaces — the contracts a new application implements.
- [note/](note/index.md) (1) — Compounded query answers — synthesis made permanent.
- [pitfall/](pitfall/index.md) (36) — Anti-patterns and the rules that forbid them.
- [process/](process/index.md) (1) — How-to processes for keeping the architecture's conventions.
- [recipe/](recipe/index.md) (20) — Task playbooks — ordered steps to build a DCA construct.
- [reference/](reference/index.md) (2) — The two classes every rule is parameterised by — DcaLayout (settings, defaults, patterns) and DcaArchitecture (how contexts and modules are discovered).
- [rule/](rule/index.md) (128) — ArchUnit rules — the enforceable, machine-checkable architecture.
- [template/](template/index.md) (49) — Domain-free code skeletons to fill in.
