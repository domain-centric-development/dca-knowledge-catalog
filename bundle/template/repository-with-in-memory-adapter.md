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
import {basePackage}.sharedkernel.marker.port.out.Repository;
import java.util.List;
import java.util.Optional;

/**
 * Repository output port for the {Name} aggregate.
 * Inherits findById / save / deleteById from {@link Repository}; add domain-language queries here.
 */
public interface {Name}Repository extends Repository<{Name}, {Name}Id> {

    List<{Name}> findAll();

    // domain-language finders, e.g. Optional<{Name}> findByNaturalKey({Key} key);
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

/** Thread-safe in-memory adapter. Replace with a database implementation in production. */
@Repository
public class InMemory{Name}Repository implements {Name}Repository {

    private final ConcurrentHashMap<{Name}Id, {Name}> store = new ConcurrentHashMap<>();

    @Override
    public Optional<{Name}> findById(final {Name}Id id) {
        return Optional.ofNullable(store.get(id));
    }

    @Override
    public {Name} save(final {Name} aggregate) {
        store.put(aggregate.id(), aggregate);
        return aggregate;
    }

    @Override
    public void deleteById(final {Name}Id id) {
        store.remove(id);
    }

    @Override
    public List<{Name}> findAll() {
        return List.copyOf(store.values());
    }
}
```

The `@Repository` here is Spring's stereotype on the *adapter*, not on the port —
it makes the implementation a wired bean. Controllers and use cases depend on the
port interface, never on this class or on the store directly.

## Realizes / governed by

- Marker: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md)
- Rules: [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/repository-interfaces-should-extend-repository-marker-interface.md) · [Repository Interfaces must reside in application output port package](/rule/tactical/repository-interfaces-must-reside-in-application-output-port-package.md) · [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/repository-implementations-must-reside-in-adapter-outgoing-package.md) · [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md) · [Repository Interfaces must end with 'Repository'](/rule/naming/repository-interfaces-must-end-with-repository.md)
- ADRs: [ADR-008 Repository Interfaces as Output Ports](/adr/adr-008-repository-interfaces-as-output-ports.md) · [ADR-004 Persistence-Oriented Repository Pattern](/adr/adr-004-persistence-oriented-repository.md)
- Book: [Adapter Layer — Outgoing Adapters](/book/07-adapter-layer/outgoing-adapters.md)
- Recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
