---
type: Template
title: "Store skeleton (output port + in-memory outgoing adapter)"
tags: [template, application, port-out, persistence]
---

Domain-free skeleton for a **Store**: the output port for operational data that has **no aggregate lifecycle** — login attempts, an audit trail, metric snapshots, an event log. Structurally parallel to the [repository template](/template/repository-with-in-memory-adapter.md), but the vocabulary is `record` / `count` / `exists` / query-by-criteria instead of `findById` / `save` / `deleteById`, because the data is *recorded*, not loaded-mutated-saved by identity. The **interface** lives in `application/shared/` and extends the `Store` marker; the **implementation** is a secondary (outgoing) adapter in `adapter/outgoing/persistence/`. Choose Store vs Repository with the [repository-vs-store decision](/decision/repository-vs-store.md) — rule of thumb: need `findById()`? Repository. Need `record()` or `count()`? Store. Replace `{Name}` (the concern) / `{context}` / `{basePackage}` and the entry type.

## `{Name}Store.java` — output port (application layer)

```java
package {basePackage}.{context}.application.shared;

import {basePackage}.sharedkernel.marker.port.out.Store;
import java.time.Instant;
import java.util.List;

/**
 * Store output port for {operational concern}. Records entries and answers
 * aggregate questions over them — no identity-based load/mutate/save lifecycle.
 */
public interface {Name}Store extends Store {

    void record({Name}Entry entry);

    long countSince(Instant from);

    boolean exists({Criterion} criterion);

    List<{Name}Entry> findRecent(int limit);

    /** A single recorded entry — a value record, not a managed aggregate. */
    record {Name}Entry({Field} field, Instant recordedAt) {}
}
```

The interface carries no Spring annotation. It ends with `Store` and extends the
marker, which is what keeps it recognisable as an output port for recorded data.
Its methods answer questions about the recorded data; they do not return a managed
entity to mutate.

## `InMemory{Name}Store.java` — outgoing adapter

```java
package {basePackage}.{context}.adapter.outgoing.persistence;

import {basePackage}.{context}.application.shared.{Name}Store;
import java.time.Instant;
import java.util.List;
import java.util.Comparator;
import java.util.concurrent.CopyOnWriteArrayList;
import org.springframework.stereotype.Component;

/** Thread-safe in-memory adapter. Replace with a database implementation in production. */
@Component
public class InMemory{Name}Store implements {Name}Store {

    private final CopyOnWriteArrayList<{Name}Entry> entries = new CopyOnWriteArrayList<>();

    @Override
    public void record(final {Name}Entry entry) {
        entries.add(entry);
    }

    @Override
    public long countSince(final Instant from) {
        return entries.stream().filter(e -> e.recordedAt().isAfter(from)).count();
    }

    @Override
    public boolean exists(final {Criterion} criterion) {
        return entries.stream().anyMatch(e -> /* matches criterion */);
    }

    @Override
    public List<{Name}Entry> findRecent(final int limit) {
        return entries.stream()
            .sorted(Comparator.comparing({Name}Entry::recordedAt).reversed())
            .limit(limit)
            .toList();
    }
}
```

An append-only list fits the recorded-data shape; there is no keyed store to load
by identity. As with the repository, controllers and use cases depend on the port
interface, never on this class or the backing collection directly. Swap it for a
database adapter without touching the port.

## Realizes / governed by

- Marker: [Store](/marker/port-out/store.md) · [OutputPort](/marker/port-out/outputport.md)
- Decisions: [Repository or Store: which output port persists this](/decision/repository-vs-store.md)
- Note: [The Store marker has no governing ArchUnit rules](/note/store-marker-has-no-governing-rules.md) — doctrine documented, not yet mechanically enforced
- Pitfall: [Repository for a non-aggregate](/pitfall/repository-for-non-aggregate.md) — the mistake this template avoids
- Book: [Stores: persistence for non-aggregate data](/book/06-application-layer/stores-persistence-for-non-aggregate-data.md)
- Sibling template: [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md)
- Recipe: [Add a store](/recipe/add-a-store.md)
