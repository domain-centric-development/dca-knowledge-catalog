---
type: Template
title: "JDBC repository adapter skeleton (JdbcClient) — Java"
parent: /template/jdbc-repository-adapter.md
tags: [template, adapter, persistence, repository, spring]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/repository.md, /marker/port-out/outputport.md, /rule/tactical/dca-tac-015.md, /rule/hexagonal/dca-hex-008.md, /rule/usecase/dca-use-009.md, /rule/tactical/dca-tac-013.md, /guide/rules.md, /guide/readme/deviations-from-the-literature.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [JDBC repository adapter skeleton (JdbcClient)](/template/jdbc-repository-adapter.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}Repository.java` — output port (unchanged)

The output port is the interface shown in the [in-memory template](/template/repository-with-in-memory-adapter.md): it sits in `application/shared/`, extends `Repository<{Name}, {Name}Id>` and carries no framework annotation. **Do not touch it** when adding JDBC.

## `schema.sql` — one table per aggregate root

```sql
CREATE TABLE IF NOT EXISTS {name} (
    id          VARCHAR(36)  PRIMARY KEY,
    sequence    BIGINT       GENERATED ALWAYS AS IDENTITY,   -- insertion order for findAll; the database assigns it
    status      VARCHAR(32)  NOT NULL,
    label       VARCHAR(120) NOT NULL,
    quantity    INTEGER      NOT NULL,
    created_at  TIMESTAMP    NOT NULL,   -- when the row was written: a fact about the row, not its order
    updated_at  TIMESTAMP    NOT NULL
);
```

Aggregate parts either become columns of this row, a JSON column, or a child table keyed by `{name}_id` that the adapter reads and writes together with the root — never across an aggregate boundary. The `sequence` column gives `findAll` its order: the database assigns it on insert, so two rows written in one instant still come back in the order they were written (`GENERATED ALWAYS AS IDENTITY` on H2, PostgreSQL and SQL Server, `AUTO_INCREMENT` on MySQL, `AUTOINCREMENT` on SQLite). A timestamp does not order two rows of one instant — the tie falls to whatever the second sort key is, a random UUID more often than not — and a heap table has no order at all; see the [ordering by timestamp](/pitfall/ordering-by-timestamp.md) pitfall.

## `Jdbc{Name}Repository.java` — outgoing adapter

```java
package {basePackage}.{context}.adapter.outgoing.persistence;

import {basePackage}.{context}.application.shared.{Name}Repository;
import {basePackage}.{context}.domain.model.{Name};
import {basePackage}.{context}.domain.model.{Name}Id;
import {basePackage}.{context}.domain.model.{Name}Status;
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
                SELECT id, status, label, quantity FROM {name} ORDER BY sequence
                """)
                .query(ROW_MAPPER)
                .list();
    }

    @Override
    public {Name} save(final {Name} aggregate) {
        // Upsert: the exact statement is dialect-specific —
        // MERGE INTO (H2, SQL Server, Oracle), INSERT ... ON CONFLICT (PostgreSQL, SQLite),
        // INSERT ... ON DUPLICATE KEY UPDATE (MySQL). The sequence column is not in the
        // column list: the database assigns it on insert and leaves it alone on update.
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

Run the same port contract test against this adapter, the in-memory one and any future implementation: `save` then `findById` round-trips every field, `findAll` returns insertion order — including two aggregates saved within one instant (save them back to back with a fixed clock, or with no clock at all: the order must not depend on one) — `deleteById` makes the id unknown, and a mutation that was not saved is not visible to the next `findById`. The JDBC adapter needs a database for it (an embedded one or a container); the assertions are the same.
