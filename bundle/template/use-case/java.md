---
type: Template
title: "Use case skeleton (InputPort + UseCase + Command/Query + Result) — Java"
parent: /template/use-case.md
tags: [template, application, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-009.md, /marker/port-in/usecase.md, /marker/port-in/inputport.md, /guide/rules.md, /guide/elements.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Use case skeleton (InputPort + UseCase + Command/Query + Result)](/template/use-case.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}InputPort.java` — the driving port

```java
package {basePackage}.{context}.application.{usecasename};

import dev.domaincentric.dca.buildingblocks.hexagonal.port.in.UseCase;

/** Input port for the {Name} use case (driving/primary port). */
public interface {Name}InputPort extends UseCase<{Name}Command, {Name}Result> {
    @Override
    {Name}Result execute({Name}Command input);
}
```

## `{Name}Command.java` — input (writes)

```java
package {basePackage}.{context}.application.{usecasename};

/** Immutable command carrying the data needed to mutate state. */
public record {Name}Command(
    // domain-typed fields, e.g. CustomerId customerId, Money amount
) {}
```

For a read use case, replace with `{Name}Query` and have the InputPort extend
`UseCase<{Name}Query, {Name}Result>`.

## `{Name}Result.java` — output

```java
package {basePackage}.{context}.application.{usecasename};

/**
 * Application-layer output model. The adapter maps this to a *Response DTO.
 * Values, never identities: ids, value objects, nested part records (named by content, e.g.
 * LineItemSummary), read models — no aggregate root or entity, also not inside List/Optional.
 * A command's result stays small; the view comes from a query.
 */
public record {Name}Result(
    // primitive/value fields the caller needs back
) {
    public static {Name}Result from(/* aggregate or read model */) {
        // copy values out; the static factory keeps assembly in the application layer
    }
}
```

When the projection needs several ports, assemble in the use case body; when it grows or several use cases
share it, in a `*Assembler` (use-case folder or `application/shared`). Large aggregates hand out a snapshot
(`Value` in `domain/readmodel`) that becomes the result field. See
[Result shape and assembly](/decision/result-shape-and-assembly.md).

## `{Name}UseCase.java` — implementation

```java
package {basePackage}.{context}.application.{usecasename};

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class {Name}UseCase implements {Name}InputPort {

    private final /* OutputPort */ port;   // constructor-injected output ports only

    public {Name}UseCase(/* OutputPort */ port) {
        this.port = port;
    }

    @Override
    public {Name}Result execute({Name}Command input) {
        // 1. load aggregate(s) via output ports
        // 2. apply business rules on the aggregate (logic lives in the domain)
        // 3. save, then publish + clear domain events (writes)
        // 4. assemble {Name}Result: values only (static from(...)), never the aggregate
        throw new UnsupportedOperationException("Not yet implemented");
    }
}
```

`@Transactional` at class level is the boundary when every output port is local. If the use case also reads from a
remote-capable port, drop the annotation, do the remote reads first and wrap steps 1–3 in
`transactionBoundary.inTransaction(() -> { ... })` (constructor-inject `TransactionBoundary` from the building
blocks' `application` package — it is not an output port). See
[Declarative or explicit transaction boundary](/decision/declarative-vs-explicit-transaction-boundary.md).

## Read-only variant (`{Name}Query`)

A query use case answers a question and changes nothing. It carries no `@Transactional` and no
`DomainEventPublisher` — there is no aggregate to save, so there are no events to publish. Its only
collaborators are the repository or a dedicated read port.

```java
package {basePackage}.{context}.application.{usecasename};

import dev.domaincentric.dca.buildingblocks.hexagonal.port.in.UseCase;

/** Input port for the {Name} query (driving/primary port). */
public interface {Name}InputPort extends UseCase<{Name}Query, {Name}Result> {
    @Override
    {Name}Result execute({Name}Query input);
}
```

```java
package {basePackage}.{context}.application.{usecasename};

/** Immutable query carrying the criteria of the question. */
public record {Name}Query(
    // domain-typed criteria, e.g. CustomerId customerId
) {}
```

```java
package {basePackage}.{context}.application.{usecasename};

import {basePackage}.{context}.application.shared.{Aggregate}Repository;
import org.springframework.stereotype.Service;

@Service
public class {Name}UseCase implements {Name}InputPort {

    private final {Aggregate}Repository repository;   // repository or read port only — no publisher

    public {Name}UseCase({Aggregate}Repository repository) {
        this.repository = repository;
    }

    @Override
    public {Name}Result execute({Name}Query input) {
        // 1. read via the output port
        // 2. assemble {Name}Result: values only (static from(...)), never the aggregate
        throw new UnsupportedOperationException("Not yet implemented");
    }
}
```

The `{Name}Result` record is the same as above. If the projection outgrows the aggregate, read from a
read model instead ([Add a read model](/recipe/add-a-read-model.md)).

> **Bulk command without `save`.** A command that calls a set-level method on the port — `repository.deleteAll()`,
> `repository.archiveAllBefore(cutoff)` — loads and saves no aggregate and registers no domain event, so it needs
> no `DomainEventPublisher`: `DCA-USE-009` ([Use cases that save an aggregate must publish its domain
> events](/rule/usecase/dca-use-009.md)) hangs on `save`, not on
> the command shape. It still writes, so keep `@Transactional`. See [Add a bulk operation](/recipe/add-a-bulk-operation.md)
> and [Declarative or explicit transaction boundary](/decision/declarative-vs-explicit-transaction-boundary.md).
