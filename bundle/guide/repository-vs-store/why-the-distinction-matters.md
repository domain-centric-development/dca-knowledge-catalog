---
type: Section
title: Why the distinction matters
chapter: Repository vs. Store
source: guide
resource: dca-guide/architecture/repository-vs-store.md
tags: [guide, section]
---

The naming is part of the Ubiquitous Language. A reader should know from the interface name alone whether they're dealing with a managed aggregate (Repository) or recorded data (Store) — without opening the implementation. Both are technically Output Ports in hexagonal architecture, but the business role is fundamentally different.

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
