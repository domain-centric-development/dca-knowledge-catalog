---
type: Template
title: "Repository skeleton (output port + in-memory outgoing adapter) — Java"
parent: /template/repository-with-in-memory-adapter.md
tags: [template, application, repository]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/rules.md, /marker/port-out/repository.md, /marker/port-out/outputport.md, /rule/tactical/dca-tac-013.md, /rule/tactical/dca-tac-014.md, /rule/tactical/dca-tac-015.md, /rule/tactical/dca-tac-016.md, /rule/naming/dca-nam-004.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [Repository skeleton (output port + in-memory outgoing adapter)](/template/repository-with-in-memory-adapter.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}Repository.java` — output port (application layer)

```java
package {basePackage}.{context}.application.shared;

import {basePackage}.{context}.domain.{name}.{Name};
import {basePackage}.{context}.domain.{name}.{Name}Id;
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
import {basePackage}.{context}.domain.{name}.{Name};
import {basePackage}.{context}.domain.{name}.{Name}Id;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Repository;

/**
 * Thread-safe in-memory adapter. Replace with a database implementation in production.
 *
 * <p>The store holds snapshots, not the live aggregates: every read and write goes through
 * {@code {Name}.reconstitute(...)}, so a caller who mutates an aggregate and forgets {@code save()}
 * changes nothing — exactly as a database adapter would behave.
 */
@Repository
public class InMemory{Name}Repository implements {Name}Repository {

    private final ConcurrentHashMap<{Name}Id, {Name}> store = new ConcurrentHashMap<>();

    @Override
    public Optional<{Name}> findById(final {Name}Id id) {
        return Optional.ofNullable(store.get(id)).map(this::copyOf);
    }

    @Override
    public {Name} save(final {Name} aggregate) {
        store.put(aggregate.id(), copyOf(aggregate));
        return aggregate;
    }

    @Override
    public void deleteById(final {Name}Id id) {
        store.remove(id);
    }

    @Override
    public List<{Name}> findAll() {
        return store.values().stream().map(this::copyOf).toList();
    }

    @Override
    public long count() {
        return store.size();
    }

    @Override
    public void deleteAll() {
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
and fail against a database ([A repository hands out copies](/guide/readme/rules.md)). Reconstitution
registers no domain event; unpublished events on the saved instance are not carried into the store.
