---
type: Template
title: "Use case skeleton (InputPort + UseCase + Command/Query + Result)"
tags: [template, application, use-case]
---

Domain-free skeleton for one application-layer use case. A use case is a self-contained folder `application/{usecasename}/` (lowercase) with four files. Replace `{Name}` (PascalCase), `{usecasename}` (lowercase), `{context}`, `{basePackage}`. Use `Command` for writes, `Query` for reads.

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

## Realizes / governed by

- Markers: [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md) · [InputPort](/marker/port-in/inputport.md)
- Guide: [Layer rules](/guide/readme/rules.md) · [Layer elements](/guide/readme/elements.md)
- Recipe: [Add a use case](/recipe/add-a-use-case.md)
