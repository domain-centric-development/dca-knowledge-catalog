---
type: Decision
title: Who uses a domain service — and where a read model computes
tags: [decision, tactical, domain, domain-service, application]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/domain-layer-rules.md, /rule/advanced/dca-adv-021.md, /rule/advanced/dca-adv-019.md, /rule/hexagonal/dca-hex-012.md, /marker/tactical/domainservice.md, /decision/reading-an-aggregate.md, /pitfall/asking-the-aggregate-and-deciding-outside.md]
---

A domain service holds logic that spans aggregates — a workload over several assignments from two sources, a check across two aggregates. It is tempting to reach for it from wherever its answer is needed: a model type that wants the workload, a read model that shows it, an adapter that writes it, the wiring that checks a configured value at start-up. Each of those moves a decision out of the use case that owns it.

## The discriminator

Ask, for each place that wants what a domain service computes:

1. **Is it the application — a use case?** Then it calls the service and carries the outcome in its result. This is the only caller besides another domain service.
2. **Is it another domain service?** It may use one: services compose.
3. **Is it the composition root?** It constructs the service and hands it to the use case. It does not call it — not to validate a setting, not to warm a cache.
4. **Is it an aggregate, an entity or a value?** It is told the outcome by the use case, as a parameter of the operation that needs it. The service takes the aggregate, not the reverse.
5. **Is it a read model, a result type, an adapter of either direction?** It reads what the use case returned. A read model computes on query through the aggregate and its values only.

## Options

### The use case calls the service and returns the outcome (do this)

```java
public PlanReview execute(ReviewPlan query) {
    Plan plan = plans.findById(query.planId()).orElseThrow();
    Workload load = balancing.loadOf(plan, calendars.forTeam(plan.teamId()));
    return new PlanReview(PlanView.of(plan), load);
}
```

The page reads `load` from the result. A second caller that needs the same workload runs the same use case, or the use case's result carries it.

### A decision the aggregate takes itself: ask the aggregate

If the answer needs nothing but the aggregate's own state, it is no domain service at all — it is a method of the aggregate (`plan.canBeApproved()`). A copy the use case returns is a read model; it answers from the values it was built from and never calls back into the domain.

### The service called from outside the application (avoid)

A read model whose getter calls `balancing.loadOf(...)`, an outgoing adapter that computes the workload while it exports, a configuration class that calls the service at start-up: each decides when the service runs, outside the transaction and outside the result. The caller cannot be tested through the input port, and two callers drift.

## Consequences

- The rule `DCA-ADV-021` (experimental) holds the whole: outside the application, nothing but a domain service calls, accesses or constructs one; the composition root may construct one to hand it to a use case. `DCA-ADV-019` (model types) and `DCA-HEX-012` (incoming adapters) each hold a part of it and stay, so either rule set stands alone.
- A type named as a parameter or a field is not a use — a use case's constructor names its services, and the composition root passes them in.
- Where a language marks no module with a role, a module of free functions is not recognised as a domain service; a domain service there is a type that carries the role.

## Anchors

- Guide: [Domain layer rules](/guide/rules/domain-layer-rules.md) — a domain service is used by the application and by other domain services only
- Rules: [Domain services are used only by the application and by other domain services](/rule/advanced/dca-adv-021.md) · [Aggregates, entities and value objects must not use domain services](/rule/advanced/dca-adv-019.md) · [Incoming Adapters must not depend on domain services](/rule/hexagonal/dca-hex-012.md)
- Marker: [DomainService](/marker/tactical/domainservice.md)
- Related decision: [Reading an aggregate](/decision/reading-an-aggregate.md)
- Related pitfall: [Asking the aggregate, deciding outside it](/pitfall/asking-the-aggregate-and-deciding-outside.md)
