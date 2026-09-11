---
type: Section
title: Store
chapter: Repository vs. Store
source: guide
resource: dca-guide/architecture/repository-vs-store.md
tags: [guide, section]
---

Records or queries operational data without an own aggregate lifecycle.

- Exists for **Value Objects, Events, or technical state** without an aggregate lifecycle
- Append-/record-style semantics: `record()`, `count()`, `exists()`, `reset()` — lookup by key is allowed; no aggregate `save()` / `delete()` semantics
- Extends the `Store` marker (`Store extends OutputPort`) — never the `Repository` marker
- Implementation lives in `adapter.outgoing/`

```java
public interface LoginProtectionStore extends Store {
    void record(LoginAttempt attempt);
    int  countRecentFailures(BaseStore baseStore, Email email, Duration window);
    boolean isLoginBlocked(BaseStore baseStore, Email email);
}
```

## Related mentions (heuristic)

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)
