# repository-vs-store

- [Decision matrix](decision-matrix.md) — Decision matrix
- [Repository](repository.md) — Collection-like interface for Aggregate Roots (Evans, Vernon).
- [Rules of thumb](rules-of-thumb.md) — 1. Lookup by key (`findById`) is allowed on a Store too; aggregate lifecycle determines Repository semantics.
- [Separate domain and persistence model](separate-domain-and-persistence-model.md) — A repository implementation maps between two models: the aggregate the domain owns, and the
- [Store](store.md) — Records or queries operational data without an own aggregate lifecycle.
- [Why the distinction matters](why-the-distinction-matters.md) — The naming is part of the Ubiquitous Language. A reader should know from the interface name alone whether they're dea...
