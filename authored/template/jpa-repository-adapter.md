---
type: Template
title: "JPA repository adapter (same output port, Spring Data + entity + mapper)"
tags: [template, adapter, persistence, repository]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/repository.md, /marker/port-out/outputport.md, /rule/tactical/dca-tac-013.md, /rule/tactical/dca-tac-014.md, /rule/tactical/dca-tac-015.md, /rule/tactical/dca-tac-016.md, /rule/tactical/dca-tac-017.md, /rule/hexagonal/dca-hex-005.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for a **JPA outgoing adapter** that implements the *same* `{Name}Repository` output port as the [in-memory adapter](/template/repository-with-in-memory-adapter.md). The port and the domain aggregate do not change — only the outgoing adapter is swapped. Three collaborators live behind the boundary in `adapter/outgoing/persistence/jpa/`: a `@Entity` mapping class **separate** from the domain aggregate (so the domain stays persistence-free — the central DCA point), a Spring Data `JpaRepository` interface, and the adapter class that maps between aggregate and entity and implements the port. Replace `{Name}` (aggregate) / `{name}` / `{context}` / `{basePackage}`.

## `{Name}Repository.java` — output port (unchanged)

The output port is identical to the one shown in the [in-memory template](/template/repository-with-in-memory-adapter.md): an interface in `application/shared/` that extends `Repository<{Name}, {Name}Id>`, carrying no framework annotation. **Do not touch it** when adding JPA — that stability is the whole point of the hexagonal boundary.

## `{Name}JpaEntity.java` — persistence entity (outgoing adapter)

```java
package {basePackage}.{context}.adapter.outgoing.persistence.jpa;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

/** JPA mapping for the {Name} aggregate. A persistence type — never crosses a port boundary. */
@Entity
@Table(name = "{name}s")
public class {Name}JpaEntity {

    @Id
    @Column(length = 64)
    private String id;

    @Column(nullable = false, length = 32)
    private String status;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt = Instant.now();

    // Aggregate parts belong in child tables under the root's lifecycle:
    @OneToMany(mappedBy = "{name}", cascade = CascadeType.ALL, orphanRemoval = true,
               fetch = FetchType.LAZY)
    private List<{Name}LineJpaEntity> lines = new ArrayList<>();

    // getters / setters
}
```

This class is a plain persistence structure: no invariants, no domain methods. Aggregate parts (child entities) cascade from the root with `orphanRemoval = true`; **never** cascade across an aggregate boundary. Value objects can be flattened to columns or mapped `@Embeddable`.

## `SpringData{Name}Repository.java` — Spring Data interface (outgoing adapter)

```java
package {basePackage}.{context}.adapter.outgoing.persistence.jpa;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

/** Spring Data CRUD over the entity — keyed by the primitive id, not the domain id type. */
public interface SpringData{Name}Repository extends JpaRepository<{Name}JpaEntity, String> {

    List<{Name}JpaEntity> findByStatus(String status);
}
```

This interface speaks entities and primitives, so it must **not** be injected into use cases — only the adapter below depends on it.

## `Jpa{Name}RepositoryAdapter.java` — outgoing adapter that maps + implements the port

```java
package {basePackage}.{context}.adapter.outgoing.persistence.jpa;

import {basePackage}.{context}.application.shared.{Name}Repository;
import {basePackage}.{context}.domain.{name}.{Name};
import {basePackage}.{context}.domain.{name}.{Name}Id;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

/** Maps between the {Name} aggregate and its JPA entity. Pure mapping — no business logic. */
@Repository
@Primary
public class Jpa{Name}RepositoryAdapter implements {Name}Repository {

    private final SpringData{Name}Repository jpa;

    public Jpa{Name}RepositoryAdapter(final SpringData{Name}Repository jpa) {
        this.jpa = jpa;
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<{Name}> findById(final {Name}Id id) {
        return jpa.findById(id.value()).map(this::toDomain);
    }

    @Override
    @Transactional
    public {Name} save(final {Name} aggregate) {
        final {Name}JpaEntity entity = toEntity(aggregate);
        entity.setUpdatedAt(Instant.now());
        return toDomain(jpa.saveAndFlush(entity));
    }

    @Override
    @Transactional
    public void deleteById(final {Name}Id id) {
        jpa.deleteById(id.value());
    }

    @Override
    @Transactional(readOnly = true)
    public List<{Name}> findAll() {
        return jpa.findAll().stream().map(this::toDomain).toList();
    }

    private {Name}JpaEntity toEntity(final {Name} aggregate) {
        // build the entity from the aggregate's public accessors
    }

    private {Name} toDomain(final {Name}JpaEntity entity) {
        // rebuild through the reconstitution factory — it registers no event, so nothing to clear
        return {Name}.reconstitute(new {Name}Id(entity.getId()) /*, entity.getStatus(), lines... */);
    }
}
```

`@Repository` is Spring's stereotype on the *adapter* (a wired bean), never on the port. Gate this adapter and its in-memory sibling on complementary profiles (`@Profile("!inmemory")` here, `@Profile("inmemory")` there) so exactly one bean exists — `@Primary` would select this one even under the in-memory profile, because it ranks *registered* beans rather than gating registration. Transaction boundaries can also sit at the use-case level; reads use `readOnly = true`.

**Mapping keeps the domain persistence-free.** The aggregate carries no JPA annotations; the entity carries no invariants. The aggregate has no setters, so the mapper rebuilds it through `{Name}.reconstitute(...)`, never through `create(...)`: `create` enforces creation invariants and registers `{Name}Created`, which the next `save()` would publish as a phantom event for an aggregate that already exists ([Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md)). Because `reconstitute` registers nothing, the mapper has no events to clear. The mapper must contain *no* business logic — computing state during a save is a [business-logic-in-adapter](/pitfall/business-logic-in-adapter.md) smell. Putting `@Entity`/`jakarta.persistence` on the aggregate itself is a [framework-leak-in-domain](/pitfall/framework-leak-in-domain.md).

## Realizes / governed by

- Marker: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md)
- Rules: [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/dca-tac-013.md) · [Repository Interfaces must reside in application output port package](/rule/tactical/dca-tac-014.md) · [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/dca-tac-015.md) · [Repositories must only exist for Aggregate Roots](/rule/tactical/dca-tac-016.md) · [Repository methods must not return non-root Entities](/rule/tactical/dca-tac-017.md) · [Outgoing adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/dca-hex-005.md)
- Guide: [Deviations from the literature](/guide/readme/deviations-from-the-literature.md) · [Layer rules](/guide/readme/rules.md)
- Sibling templates: [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md) · [Aggregate root skeleton](/template/aggregate-root.md) — where `reconstitute` comes from
- Pitfall: [Reconstitution raises the creation event](/pitfall/reconstitution-raises-creation-event.md)
- Recipe: [Swap the in-memory adapter for JPA](/recipe/swap-in-memory-for-jpa.md) · [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
