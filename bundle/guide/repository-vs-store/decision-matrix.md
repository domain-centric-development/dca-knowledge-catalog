---
type: Section
title: Decision matrix
chapter: Repository vs. Store
source: guide
resource: dca-guide/architecture/repository-vs-store.md
tags: [guide, section]
---

| Criterion | Repository | Store |
|---|---|---|
| Stored object | Aggregate Root | Value Object / operational data |
| Aggregate lifecycle | yes — `save`, `delete` | no — `record`, `count`, `exists`; lookup by key allowed |
| Marker | `extends Repository<T, ID>` | `extends Store` |
| Examples | `CustomerAccountRepository`, `OrderRepository` | `LoginProtectionStore`, `AuditLogStore`, `EventStore` |

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)
