---
type: Decision
title: Plain query use case or a dedicated read model
tags: [decision, application, use-case, cqrs, repository, performance]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/elements.md, /guide/readme/integration-patterns.md, /marker/port-in/usecase.md, /marker/port-out/repository.md, /rule/usecase/dca-use-003.md]
---

You need to read data out of a context. The fork is whether a **plain query use case over the domain repository** suffices, or whether the read deserves a **dedicated read model** — a separate query side, possibly its own store, kept up to date by projection (CQRS). The first is the default and costs almost nothing; the second buys read performance and shape at the price of eventual consistency and more moving parts.

## The discriminator

Ask, in order:

1. **Can the aggregate answer the query as-is?** If loading the aggregate (or a straightforward finder on its repository) gives the data in an acceptable shape, write a **plain query use case**. If the read must span many aggregates or contexts, or wants a denormalized shape the domain model doesn't hold, that pressure points to a **read model**.
2. **Do reads and writes have the same requirements?** If read and write load, consistency, and scaling are similar, keep them on one model. A **high read/write ratio**, different consistency guarantees, or independent scaling needs justify splitting the query side off.
3. **Is there an actual performance problem?** Don't add CQRS "just in case." Reach for a read model when you have a real query-performance or reporting requirement — not before. Multiple read representations of the same data (search, cache, reporting) is a strong signal.
4. **Can the read tolerate being slightly stale?** A dedicated read model updated by projection is **eventually consistent**. If the business needs the read to reflect the latest write immediately, either stay on the domain query or keep the read model in the same database (Level 1).

## Options

### Plain query use case over the domain repository

An `application/{usecasename}/` folder with a `{Name}Query`, a `{Name}Result`, and a use case that loads via the aggregate's repository and maps to the result. Same model, immediate consistency, no projection machinery.

- **When:** the domain model can answer it; reads and writes have similar needs; no proven performance problem.
- Build it: [Add a use case](/recipe/add-a-use-case.md) (pick the read/`Query` path)
- **Example:** a list page shows "12 open items" above the list. The counter is a field of the list query's result — `ListTasksResult` with `List<TaskSummary> tasks` and `int openCount` — computed in the same use case from the same repository call. It is not a `CountOpenTasks` use case of its own (one page, one query) and not a read model (nothing to project, no skew between reads and writes). · shape: [Layer elements](/guide/readme/elements.md)

### Dedicated read model / CQRS split

A separate query side with its own read model and projections. Three escalating levels: **Level 1** — separate read/write models, *same* database (immediate consistency, simple, the recommended starting point when you split at all); **Level 2** — separate databases updated by events (eventual consistency, independent scaling); **Level 3** — different technologies for read vs. write (e.g. a search or cache store), maximum flexibility and highest complexity.

- **When:** high read/write ratio, different consistency or scaling needs, complex reporting, or several read representations — and a real requirement to justify it.
- Ground: [Enriched read model pattern](/guide/readme/integration-patterns.md)

**Default:** the **plain query use case** is the default — start there for every read. Escalate to a read model only when a concrete requirement (read/write skew, reporting, multiple representations, independent scaling) forces it, and even then prefer the lowest CQRS level that solves the problem: same-database separation before separate stores, separate stores before separate technologies. Simple CRUD, low complexity, or a need for immediate consistency everywhere all argue *against* a read model.

## Anchors

- Markers: [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md)
- Rules: [Queries must end with `Query` and reside in the application package](/rule/usecase/dca-use-003.md)
- Guide: [Layer elements](/guide/readme/elements.md)
- Recipes: [Add a use case](/recipe/add-a-use-case.md)
- Templates: [Enriched domain model](/template/enriched-domain-model.md) · [ViewModel](/template/view-model.md)
- Related decisions: [Specification vs. query method](/decision/specification-vs-query-method.md) · [Repository vs. store](/decision/repository-vs-store.md)
