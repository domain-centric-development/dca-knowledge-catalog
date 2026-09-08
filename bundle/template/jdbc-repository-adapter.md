---
type: Template
title: "JDBC repository adapter skeleton (JdbcClient)"
tags: [template, adapter, persistence, repository, spring]
---

Domain-free skeleton for a **JDBC outgoing adapter** that implements the *same* `{Name}Repository` output port as the [in-memory adapter](/template/repository-with-in-memory-adapter.md) and the [JPA adapter](/template/jpa-repository-adapter.md). The port and the aggregate do not change; only the class behind the boundary does. It lives in `adapter/outgoing/persistence/`, is named `Jdbc{Name}Repository`, and speaks SQL through Spring's `JdbcClient`: `save` is an upsert, a `RowMapper` rebuilds the aggregate through its `reconstitute(...)` factory, and `findAll` orders by an explicit column. Replace `{Name}` (aggregate) / `{name}` / `{context}` / `{basePackage}`.

**When to pick JDBC over JPA.** Choose it when you want the SQL to be visible and the mapping to be yours: no ORM identity map, no lazy loading, no dirty checking behind the aggregate's back. It fits aggregates that are stored as one row or one document (a JSON column for the parts) and read whole, which is how a repository hands out aggregates anyway. Prefer JPA when the schema is wide, relational and shared with other tooling, or when the team already carries the ORM. Either way the domain stays persistence-free; the difference is entirely inside this package.

## `{Name}Repository.java` — output port (unchanged)

The output port is the interface shown in the [in-memory template](/template/repository-with-in-memory-adapter.md): it sits in `application/shared/`, extends `Repository<{Name}, {Name}Id>` and carries no framework annotation. **Do not touch it** when adding JDBC.

## `schema.sql` — one table per aggregate root

```sql
CREATE TABLE IF NOT EXISTS {name} (
    id          VARCHAR(36)  PRIMARY KEY,
    status      VARCHAR(32)  NOT NULL,
    label       VARCHAR(120) NOT NULL,
    quantity    INTEGER      NOT NULL,
    created_at  TIMESTAMP    NOT NULL,   -- ordering column for findAll
    updated_at  TIMESTAMP    NOT NULL
);
```

Aggregate parts either become columns of this row, a JSON column, or a child table keyed by `{name}_id` that the adapter reads and writes together with the root — never across an aggregate boundary. `created_at` (or a sequence column) gives `findAll` a deterministic order; a heap table has none.

## `Jdbc{Name}Repository.java` — outgoing adapter

```java
package {basePackage}.{context}.adapter.outgoing.persistence;

import {basePackage}.{context}.application.shared.{Name}Repository;
import {basePackage}.{context}.domain.{name}.{Name};
import {basePackage}.{context}.domain.{name}.{Name}Id;
import {basePackage}.{context}.domain.{name}.{Name}Status;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Repository;

/** Maps the {Name} aggregate to and from its row. Pure mapping — no business logic. */
@Repository
public class Jdbc{Name}Repository implements {Name}Repository {

    private final JdbcClient jdbcClient;

    public Jdbc{Name}Repository(final JdbcClient jdbcClient) {
        this.jdbcClient = jdbcClient;
    }

    @Override
    public Optional<{Name}> findById(final {Name}Id id) {
        return jdbcClient.sql("""
                SELECT id, status, label, quantity FROM {name} WHERE id = :id
                """)
                .param("id", id.value().toString())
                .query(ROW_MAPPER)
                .optional();
    }

    @Override
    public List<{Name}> findAll() {
        return jdbcClient.sql("""
                SELECT id, status, label, quantity FROM {name} ORDER BY created_at, id
                """)
                .query(ROW_MAPPER)
                .list();
    }

    @Override
    public {Name} save(final {Name} aggregate) {
        // Upsert: the exact statement is dialect-specific —
        // MERGE INTO (H2, SQL Server, Oracle), INSERT ... ON CONFLICT (PostgreSQL, SQLite),
        // INSERT ... ON DUPLICATE KEY UPDATE (MySQL).
        jdbcClient.sql("""
                MERGE INTO {name} (id, status, label, quantity, created_at, updated_at)
                KEY (id)
                VALUES (:id, :status, :label, :quantity,
                        COALESCE((SELECT created_at FROM {name} WHERE id = :id), :now), :now)
                """)
                .param("id", aggregate.id().value().toString())
                .param("status", aggregate.status().name())
                .param("label", aggregate.label())
                .param("quantity", aggregate.quantity())
                .param("now", Instant.now())
                .update();
        return aggregate;
    }

    @Override
    public void deleteById(final {Name}Id id) {
        jdbcClient.sql("DELETE FROM {name} WHERE id = :id")
                .param("id", id.value().toString())
                .update();
    }

    /** Row → aggregate, through the reconstitution factory. */
    private static final RowMapper<{Name}> ROW_MAPPER = Jdbc{Name}Repository::toDomain;

    private static {Name} toDomain(final ResultSet rs, final int rowNum) throws SQLException {
        return {Name}.reconstitute(
                new {Name}Id(UUID.fromString(rs.getString("id"))),
                {Name}Status.valueOf(rs.getString("status")),
                rs.getString("label"),
                rs.getInt("quantity"));
    }
}
```

`@Repository` is Spring's stereotype on the *adapter*, never on the port. Gate this adapter and its in-memory sibling on complementary profiles so exactly one bean implements the port. `save` returns the aggregate it was given; it does **not** publish the aggregate's domain events — the use case does that after `save` returns, so publication and persistence stay in one place.

**Reconstitute, never create.** The row mapper calls `{Name}.reconstitute(...)`, a second factory on the [aggregate root](/template/aggregate-root.md) that rebuilds state *without* registering events. Calling `create(...)` here would register a fresh `{Name}Created` on every read, and the next `save` would publish a creation that happened long ago — the [reconstitution raises creation event](/pitfall/reconstitution-raises-creation-event.md) pitfall. A stored aggregate is a fact; re-reading it must not replay what its writer already published. This is also what makes the adapter obey the guide's rule that a repository hands out copies: every read constructs a new object, so an unsaved mutation is invisible to the next reader.

## Contract test on the port

Run the same port contract test against this adapter, the in-memory one and any future implementation: `save` then `findById` round-trips every field, `findAll` returns insertion order, `deleteById` makes the id unknown, and a mutation that was not saved is not visible to the next `findById`. The JDBC adapter needs a database for it (an embedded one or a container); the assertions are the same.

## Realizes / governed by

- Marker: [Repository<T, ID>](/marker/port-out/repository.md) · [OutputPort](/marker/port-out/outputport.md)
- Rules: [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/repository-implementations-must-reside-in-adapter-outgoing-package.md) · [Classes named *Repository must reside in the outgoing adapter package](/rule/hexagonal/classes-named-repository-must-reside-in-the-outgoing-adapter-package.md) · [Use cases that save an aggregate must publish its domain events](/rule/usecase/use-cases-that-save-an-aggregate-must-publish-its-domain-events.md) · [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/repository-interfaces-should-extend-repository-marker-interface.md)
- Guide: [Layer rules](/guide/readme/rules.md) (repository interface rules — "A repository hands out copies") · [Deviations from the literature](/guide/readme/deviations-from-the-literature.md)
- Pitfalls: [Reconstitution raises creation event](/pitfall/reconstitution-raises-creation-event.md) · [Business logic in adapter](/pitfall/business-logic-in-adapter.md) · [Framework leak in domain](/pitfall/framework-leak-in-domain.md)
- Sibling templates: [Repository + in-memory adapter](/template/repository-with-in-memory-adapter.md) · [JPA repository adapter](/template/jpa-repository-adapter.md) · [Aggregate root](/template/aggregate-root.md)
- Recipe: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
