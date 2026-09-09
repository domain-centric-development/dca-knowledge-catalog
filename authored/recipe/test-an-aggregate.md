---
type: Recipe
title: Test an aggregate
tags: [recipe, testing, aggregate]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/tactical/dca-tac-002.md, /marker/tactical/aggregateroot.md, /marker/tactical/domainevent.md, /marker/tactical/value.md, /marker/tactical/domainservice.md]
---

Test an aggregate root as a pure domain unit test: no mocks, no Spring, no infrastructure. Construct the aggregate through its factory, exercise a behaviour, and assert on its state, its enforced invariants, and the domain events it raises. These are the fastest tests in the suite — plain JUnit 5, real objects only.

## Steps

1. **No test doubles** — the domain layer has zero output-port dependencies ([aggregates must not hold references to output ports](/rule/tactical/dca-tac-002.md)), so there is nothing to mock. Build the aggregate for real.
2. **Create through the factory** — `{Aggregate}.create(...)`, not a raw constructor, so creation invariants and the creation event are exercised.
3. **Assert state after a command** — call a domain method (e.g. `updatePrice(...)`) and assert the resulting state via public accessors. Test observable behaviour, not private helpers.
4. **Assert invariants reject bad input** — use `assertThrows(IllegalArgumentException.class, () -> ...)` for each guarded rule (zero/negative amounts, illegal state transitions).
5. **Assert domain events** — after a state change, check `aggregate.domainEvents()` has the expected type and payload. To test a later transition in isolation, call `clearDomainEvents()` first, then assert only the new event is present.
6. **One behaviour per test** — group with `@Nested` + `@DisplayName`; name each `@Test` in the ubiquitous language.

Value objects and domain services are tested the same way (state-based, no mocks): a value object test asserts immutability and constructor validation; a domain service test `new`s the stateless service and asserts its calculation.

## Test-quality checklist (Chapter 12)

- Pure unit test — no mocks, no infrastructure, milliseconds to run.
- Test business rules, invariants, and state transitions.
- Assert domain-event emission (type + payload).
- Test observable behaviour, never private methods.
- One scenario per test.

## Anchors

- Markers: [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md) · [DomainEvent](/marker/tactical/domainevent.md) · [Value](/marker/tactical/value.md) · [DomainService](/marker/tactical/domainservice.md)
- Rules: [Aggregate roots must not hold references to output ports](/rule/tactical/dca-tac-002.md)
- The aggregate under test: [Add an aggregate](/recipe/add-an-aggregate.md) · [Add a value object](/recipe/add-a-value-object.md)
- Testing the use case that orchestrates it: [Test a use case](/recipe/test-a-use-case.md)
- Pitfall this guards against: [Anemic domain model](/pitfall/anemic-domain-model.md) — an anemic aggregate has no behaviour to test
- Reference tests: `pricing/domain/model/ProductPriceTest`, `checkout/domain/service/CheckoutStepValidatorTest`
