---
type: Template
title: "Store skeleton (output port + in-memory outgoing adapter) — Java"
parent: /template/store-with-in-memory-adapter.md
tags: [template, application, port-out, persistence]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/store.md, /marker/port-out/outputport.md, /rule/tactical/dca-tac-018.md, /rule/tactical/dca-tac-019.md, /rule/tactical/dca-tac-020.md, /rule/tactical/dca-tac-021.md, /guide/readme/elements.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Store skeleton (output port + in-memory outgoing adapter)](/template/store-with-in-memory-adapter.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}Store.java` — output port (application layer)

```java
package {basePackage}.{context}.application.shared;

import dev.domaincentric.dca.buildingblocks.hexagonal.port.out.Store;
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
