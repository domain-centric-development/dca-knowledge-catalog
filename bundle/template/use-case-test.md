---
type: Template
title: "Use-case test skeleton (JUnit 5 + hand-written fake ports)"
tags: [template, testing, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-in/usecase.md, /marker/port-out/repository.md, /marker/port-out/domaineventpublisher.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for a use-case unit test. It drives the input port with a `Command`/`Query`, asserts on the `Result`, and swaps every output port for a **hand-written fake** — the reference implementation uses plain JUnit 5 (`org.junit.jupiter.api`) with in-line fakes, **not Mockito or AssertJ**. Real domain objects (aggregates, value objects) are used directly, never mocked. Replace `{Name}` (use case), `{Aggregate}`, `{context}` / `{basePackage}`.

> The book's Chapter 12 also shows a Mockito variant with `@Mock` + `verify(...)`. The reference implementation deliberately prefers hand-written fakes: they exercise real port behaviour (a fake repository actually stores and returns aggregates), which catches orchestration bugs that a bare `verify()` misses. Match the reference stack unless the project already standardises on Mockito.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`use-case-test/java.md`](/template/use-case-test/java.md)

## Realizes / governed by

- Markers: [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md) · [Repository<T, ID>](/marker/port-out/repository.md) · [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- Recipe: [Test a use case](/recipe/test-a-use-case.md) · [Add a use case](/recipe/add-a-use-case.md)
- Reference tests: `cart/application/mergecarts/MergeCartsUseCaseTest`, `pricing/application/getpricesforproducts/GetPricesForProductsUseCaseTest`
