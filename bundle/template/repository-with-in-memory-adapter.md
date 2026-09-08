---
type: Template
title: "Repository skeleton (output port + in-memory outgoing adapter)"
tags: [template, application, repository]
---

Domain-free skeleton for a repository: the collection-like output port for one aggregate root. The **interface** is an output port that lives in `application/shared/` and extends `Repository<T, ID>`; the **implementation** is a secondary (outgoing) adapter in `adapter/outgoing/persistence/`. One repository per aggregate root — never per entity. Method names use the ubiquitous language, not generic CRUD. Replace `{Name}` (aggregate) / `{context}` / `{basePackage}`. This template uses a `ConcurrentHashMap` store to match the reference implementation; swap it for a database adapter without touching the port.

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

## Realizes / governed by

- Marker: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md)
- Rules: [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/repository-interfaces-should-extend-repository-marker-interface.md) · [Repository Interfaces must reside in application output port package](/rule/tactical/repository-interfaces-must-reside-in-the-application-layer-s-shared-output-port-package.md) · [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/repository-implementations-must-reside-in-adapter-outgoing-package.md) · [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md) · [Repository Interfaces must end with 'Repository'](/rule/naming/repository-interfaces-must-end-with-repository.md)
- Guide: [Deviations from the literature](/guide/readme/deviations-from-the-literature.md) · [Layer rules](/guide/readme/rules.md) · [Ports and adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- Recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md) · [Add a bulk operation](/recipe/add-a-bulk-operation.md)
- Sibling template: [Aggregate root skeleton](/template/aggregate-root.md) — where `reconstitute` comes from
- Pitfall: [Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md)
