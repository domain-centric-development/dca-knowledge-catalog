---
type: Recipe
title: Test a use case
tags: [recipe, testing, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-in/usecase.md, /marker/port-out/repository.md, /marker/port-out/domaineventpublisher.md]
---

Test a use case as an application-layer unit test: construct the `*UseCase`, feed it a `Command` (write) or `Query` (read), assert on the returned `Result` and on observable state. Every output port (repository, event publisher, gateway) is replaced with a **hand-written fake**; real domain objects are used directly, never mocked. The reference implementation uses plain JUnit 5 with in-line fakes — no Mockito, no AssertJ.

## Steps

1. **Instantiate the use case directly** — no Spring context. In `@BeforeEach`, `new` the fake output ports, then `new {Name}UseCase(fakeRepo, fakeEventPublisher, ...)`. This keeps the test a fast, pure unit test.
2. **Fake the output ports, not the domain** — implement each output-port interface with a small `Test{Aggregate}Repository` backed by a `ConcurrentHashMap`, and a `TestDomainEventPublisher` that records events. Use the [use-case test template](/template/use-case-test.md). Do **not** mock aggregates or value objects — build them for real.
3. **Arrange through the port** — seed state by calling `fakeRepo.save(aggregate)` with genuine domain objects, so the test round-trips real data.
4. **Act once** — call `useCase.execute(command)` exactly once per test.
5. **Assert on the contract, not internals** — check the `Result` fields and observable side effects (e.g. `fakeRepo.findById(...)` present/absent). Never assert on private methods or fields.
6. **Verify event hygiene** — if the use case publishes, assert the fake publisher recorded the expected event and that `publishAndClearEvents` left the aggregate's `domainEvents()` empty.
7. **One behaviour per test** — group scenarios with `@Nested` + `@DisplayName`; each `@Test` covers a single behaviour named in the ubiquitous language.

## Test-quality checklist (Chapter 12)

- Mock output ports, never domain objects — build real aggregates/value objects.
- Use hand-written fakes over Mockito to match the reference stack.
- Test orchestration and observable state, not implementation details.
- Verify domain-event publishing and clearing.
- One scenario per test; name behaviours in domain language.

## Anchors

- Template: [Use-case test skeleton](/template/use-case-test.md)
- Markers: [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md) · [Repository<T, ID>](/marker/port-out/repository.md) · [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- The use case under test: [Add a use case](/recipe/add-a-use-case.md) · its ports: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
- Testing the aggregate it orchestrates: [Test an aggregate](/recipe/test-an-aggregate.md)
- Reference tests: `cart/application/mergecarts/MergeCartsUseCaseTest`, `pricing/application/getpricesforproducts/GetPricesForProductsUseCaseTest`
