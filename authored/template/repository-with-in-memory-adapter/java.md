---
type: Template
title: "Repository skeleton (output port + in-memory outgoing adapter) — Java"
parent: /template/repository-with-in-memory-adapter.md
tags: [template, application, repository]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules.md, /marker/port-out/repository.md, /marker/port-out/outputport.md, /rule/tactical/dca-tac-013.md, /rule/tactical/dca-tac-014.md, /rule/tactical/dca-tac-015.md, /rule/tactical/dca-tac-016.md, /rule/naming/dca-nam-004.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [Repository skeleton (output port + in-memory outgoing adapter)](/template/repository-with-in-memory-adapter.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}Repository.java` — output port (application layer)

```java
package {basePackage}.{context}.application.shared;

import {basePackage}.{context}.domain.model.{Name};
import {basePackage}.{context}.domain.model.{Name}Id;
import dev.domaincentric.dca.buildingblocks.hexagonal.port.out.Repository;
import java.util.List;
import java.util.Optional;

/**
 * Repository output port for the {Name} aggregate.
 * Inherits findById / save / deleteById from {@link Repository}; add domain-language queries here.
 * The marker fixes only those three — the port is freely extensible with whatever questions
 * its use cases ask, including set-level operations that touch no single aggregate.
 */
public interface {Name}Repository extends Repository<{Name}, {Name}Id> {

    List<{Name}> findAll();

    // domain-language finders, e.g. Optional<{Name}> findByNaturalKey({Key} key);

    /** Set-level question — a query use case asks it without loading anything. */
    long count();

    /** Set-level command — a bulk use case calls it without save(), so it publishes no events. */
    void deleteAll();
}
```

The interface carries no Spring annotation. It ends with `Repository` and extends
the marker, which is what keeps it recognisable as an output port.

## `InMemory{Name}Repository.java` — outgoing adapter

```java
package {basePackage}.{context}.adapter.outgoing.persistence;

import {basePackage}.{context}.application.shared.{Name}Repository;
import {basePackage}.{context}.domain.model.{Name};
import {basePackage}.{context}.domain.model.{Name}Id;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.springframework.stereotype.Repository;

/**
 * Thread-safe in-memory adapter. Replace with a database implementation in production.
 *
 * <p>The store holds snapshots, not the live aggregates: every read and write goes through
 * {@code {Name}.reconstitute(...)}, so a caller who mutates an aggregate and forgets {@code save()}
 * changes nothing — exactly as a database adapter would behave.
 *
 * <p>The map keeps insertion order — the port's promise that {@code findAll} returns aggregates
 * in the order they were first saved; a database adapter keeps it with a sequence column.
 */
@Repository
public class InMemory{Name}Repository implements {Name}Repository {

    private final Map<{Name}Id, {Name}> store = new LinkedHashMap<>();

    @Override
    public synchronized Optional<{Name}> findById(final {Name}Id id) {
        return Optional.ofNullable(store.get(id)).map(this::copyOf);
    }

    @Override
    public synchronized {Name} save(final {Name} aggregate) {
        store.put(aggregate.id(), copyOf(aggregate));   // re-saving keeps the first position
        return aggregate;
    }

    @Override
    public synchronized void deleteById(final {Name}Id id) {
        store.remove(id);
    }

    @Override
    public synchronized List<{Name}> findAll() {
        final List<{Name}> copies = new ArrayList<>(store.size());
        for (final {Name} stored : store.values()) {
            copies.add(copyOf(stored));
        }
        return copies;
    }

    @Override
    public synchronized long count() {
        return store.size();
    }

    @Override
    public synchronized void deleteAll() {
        store.clear();
    }

    /** Rebuild through the reconstitution factory: no shared instance, no replayed events. */
    private {Name} copyOf(final {Name} aggregate) {
        return {Name}.reconstitute(aggregate.id() /*, aggregate's persisted state via accessors */);
    }
}
```

The `@Repository` here is Spring's stereotype on the *adapter*, not on the port —
it makes the implementation a wired bean. Controllers and use cases depend on the
port interface, never on this class or on the store directly.

`findById` hands out a **copy**, rebuilt through `{Name}.reconstitute(...)` — the same factory a JDBC or
JPA adapter must use because a row leaves it no choice. Returning `store.get(id)` directly would hand out
the stored instance, so a use case that mutates it without calling `save()` would silently pass its tests
and fail against a database ([A repository hands out copies](/guide/rules.md)). Reconstitution
registers no domain event; unpublished events on the saved instance are not carried into the store.
