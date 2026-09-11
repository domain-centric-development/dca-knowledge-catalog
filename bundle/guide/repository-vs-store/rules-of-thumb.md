---
type: Section
title: Rules of thumb
chapter: Repository vs. Store
source: guide
resource: dca-guide/architecture/repository-vs-store.md
tags: [guide, section]
---

1. Lookup by key (`findById`) is allowed on a Store too; aggregate lifecycle determines Repository semantics.
2. Need `record()` or `count()`? → Store (the object is recorded, not managed).
3. In doubt: if the stored object is a `Value` or a record, it's almost always a Store.

> **Note on EventStore (Event Sourcing):** The `EventStore` from Event Sourcing is a *specialization* of Store — one specifically for Domain Events that supports aggregate reconstruction. The general `Store` is the broader pattern for any operational data.

> **Note on cross-cutting `*Response` classes:** Generic Response/error classes (`ErrorResponse`, base `Response`, `SimpleResponse`) belong in the **shared kernel's adapter-incoming package**, not in any individual bounded context. ArchUnit rules that check `*Response` placement must include the shared kernel adapter — discover its package dynamically via `@SharedKernel` rather than hardcoding the name (`shared` / `common` / `core` / `sharedkernel`).

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
