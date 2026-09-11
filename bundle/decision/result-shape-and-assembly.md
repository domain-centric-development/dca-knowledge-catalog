---
type: Decision
title: "Result shape and assembly: what a use-case result carries, how big it is, who builds it"
tags: [decision, application, use-case, dto, cqrs, hexagonal, adapter]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-015.md, /marker/tactical/value.md, /marker/tactical/aggregateroot.md, /marker/tactical/entity.md, /rule/hexagonal/dca-hex-012.md, /rule/usecase/dca-use-006.md, /rule/usecase/dca-use-007.md, /marker/tactical/domainservice.md]
---

A use case has done its work and must answer. Three questions decide the shape of that answer: **what may cross the boundary** (values or the aggregate itself), **how much** (an acknowledgement or the whole view), and **who assembles it** (a static factory, the use case, a dedicated class, or the adapter). The edges are already fixed by rules — the answer is named `*Result`, lives in the use-case package, is immutable, and response DTOs and view models belong to the adapter. This decision covers the middle.

## The discriminator

Ask, in order:

1. **Would the adapter receive an identity?** If any field, nested part record or generic argument (`List<T>`, `Optional<T>`, `Map<K,V>`) of the result is an aggregate root or an entity, the adapter holds a handle on the model and can call behaviour behind the port's back. Never — replace it with ids, value objects, an enriched model or a snapshot ([Results must not expose aggregate roots or entities](/rule/usecase/dca-use-015.md)). Values are fine: primitives, nested records, value objects (the shared kernel's `Money` and `ProductId` included), enriched domain models and read models — anything marked [Value](/marker/tactical/value.md), nothing marked [AggregateRoot](/marker/tactical/aggregateroot.md) or [Entity](/marker/tactical/entity.md).
2. **Is this a command or a query?** A command answers small: ids, status or outcome, what the caller needs for its next step. The view comes from a query use case or a read model ([Read model or domain query](/decision/read-model-vs-domain-query.md)). A query answers with the read shape the caller renders. If a command wants to return the whole view, that is the documented exception — it saves a remote caller a round trip — and then it returns the read-model `Value`, never a parade of primitives.
3. **How much state does the aggregate have to hand out?** A few accessors: the result's static factory reads them. A large aggregate: it hands out a **snapshot** — a `Value` record in `domain/readmodel`, built by `Snapshot.from(aggregate)` — and the snapshot *is* the result field; the use case does not flatten it a second time.
4. **How many ports feed the projection?** One aggregate: a static `from(...)` on the result. Several ports (the aggregate plus current prices, stock, a profile): orchestration, in the use-case body. Grown, or needed by several use cases: a dedicated `*Assembler`.
5. **Does the adapter have to compute anything to render?** Calling the own, parameterless queries of a delivered value or read model (`lineTotal()`, `isValidForCheckout()`) is reading — a read model that could not answer them would be no read model. If a view model has to import a domain service, or combine values from several sources into a new fact, the result is too poor. Move the value into the result or the read model; the adapter reads and formats ([Incoming adapters must not depend on domain services](/rule/hexagonal/dca-hex-012.md)).

## Options

### Static factory on the result

```java
public record CreateOrderResult(OrderId orderId, Money total, OrderStatus status) {
    public static CreateOrderResult from(Order order) {
        return new CreateOrderResult(order.id(), order.total(), order.status());
    }
}
```

- **When:** one aggregate, a handful of values. The default.
- Parts are nested records with their own `from`, named by content (`CartItemSummary`, `LineItemData`, `ProfileView`) — `*Result` is the top level only. A part several use cases share moves to `application/shared`.

### Snapshot as the result field

```java
// domain/readmodel
public record CheckoutCartSnapshot(CheckoutSessionId sessionId, CheckoutStep step, CheckoutSessionStatus status,
        List<LineItemSnapshot> lineItems, Money subtotal, @Nullable CheckoutTotals totals /* … */) implements Value {
    public static CheckoutCartSnapshot from(CheckoutSession session) { /* copies state */ }
}

// application
public record GetCheckoutSessionResult(boolean found, @Nullable CheckoutCartSnapshot session) { /* … */ }
```

- **When:** a large aggregate and a query that renders most of it. The snapshot carries no identity of its own and no behaviour beyond derived readings.
- The command next to it stays small: `SubmitDeliveryResult(sessionId, currentStep, status)` — the next page asks the query.

### Assembly in the use-case body

```java
final EnrichedCart enriched = enrichedCartFactory.create(cart, articleDataPort.getArticleData(productIds));
return GetCartByIdResult.found(enriched, cartTotalCalculator.containedTax(enriched.calculateCurrentSubtotal()));
```

- **When:** the projection needs several ports or a domain service. That is orchestration and belongs where orchestration lives; a private method next to `execute` is fine. Where the logic itself belongs: [Where does the logic live](/decision/where-does-the-logic-live.md).

### A dedicated `*Assembler`

- **When:** the projection has grown past a screen, or several use cases build the same shape. One class, in the use-case folder or in `application/shared`, named `*Assembler` (Fowler's term). Never `*Mapper` or `*Converter` — those names belong to the adapter — and never `*Helper`.

### Not taken

- **The aggregate as the result** (Vernon's Domain Payload Object) and **double dispatch into a rendering interface** (Mediator) — not even for an in-process UI. Every adapter gets the same result model; REST and MCP are remote anyway.
- **Assembly in the adapter.** The adapter formats for HTTP, HTML or a tool protocol. It reads the domain values and read models a result delivers — their own, parameterless queries included — but it does not inject or invoke a domain service, construct aggregates, entities or domain values, combine values into a new business fact, or trigger behaviour with side effects: it turns external input into a `Command`/`Query` and calls an input port. Outgoing adapters are the deliberate exception — a repository maps, constructs and reconstitutes domain objects while implementing an output port, restoring state without making new business decisions.

## Anchors

- Rules: [Results must not expose aggregate roots or entities](/rule/usecase/dca-use-015.md) · [Incoming adapters must not depend on domain services](/rule/hexagonal/dca-hex-012.md) · [Results must end with `Result` and reside in the application package](/rule/usecase/dca-use-006.md) · [Results should be immutable](/rule/usecase/dca-use-007.md)
- Markers: [Value](/marker/tactical/value.md) · [AggregateRoot](/marker/tactical/aggregateroot.md) · [Entity](/marker/tactical/entity.md) · [DomainService](/marker/tactical/domainservice.md)
- Guide: [Layer elements](/guide/elements.md) — the use-case pattern and its result · [Deviations from the literature](/guide/readme/deviations-from-the-literature.md)
- Related decisions: [Enriched value model or aggregate](/decision/enriched-model-vs-aggregate.md) · [Read model or domain query](/decision/read-model-vs-domain-query.md) · [Where does the logic live](/decision/where-does-the-logic-live.md)
- Recipes and templates: [Add a use case](/recipe/add-a-use-case.md) · [Use case skeleton](/template/use-case.md) · [Enriched domain model](/template/enriched-domain-model.md)
