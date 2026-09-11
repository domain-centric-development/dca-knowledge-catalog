---
type: Section
title: Repository
chapter: Repository vs. Store
source: guide
resource: dca-guide/architecture/repository-vs-store.md
tags: [guide, section]
---

Collection-like interface for Aggregate Roots (Evans, Vernon).

- Exists **only** for Aggregate Roots
- Identity + lifecycle semantics: `findById()`, `save()`, `delete()`
- Extends the `Repository<T, ID>` marker
- One Repository per Aggregate Root

```java
public interface CustomerAccountRepository extends Repository<CustomerAccount, CustomerAccountId> {
    Optional<CustomerAccount> findById(CustomerAccountId id);
    void save(CustomerAccount account);
}
```

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
