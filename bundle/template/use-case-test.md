---
type: Template
title: "Use-case test skeleton (JUnit 5 + hand-written fake ports)"
tags: [template, testing, use-case]
---

Domain-free skeleton for a use-case unit test. It drives the input port with a `Command`/`Query`, asserts on the `Result`, and swaps every output port for a **hand-written fake** — the reference implementation uses plain JUnit 5 (`org.junit.jupiter.api`) with in-line fakes, **not Mockito or AssertJ**. Real domain objects (aggregates, value objects) are used directly, never mocked. Replace `{Name}` (use case), `{Aggregate}`, `{context}` / `{basePackage}`.

> The book's Chapter 12 also shows a Mockito variant with `@Mock` + `verify(...)`. The reference implementation deliberately prefers hand-written fakes: they exercise real port behaviour (a fake repository actually stores and returns aggregates), which catches orchestration bugs that a bare `verify()` misses. Match the reference stack unless the project already standardises on Mockito.

## `{Name}UseCaseTest.java` — application-layer unit test

```java
package {basePackage}.{context}.application.{usecasename};

import static org.junit.jupiter.api.Assertions.*;

import {basePackage}.{context}.application.shared.Test{Aggregate}Repository;
import {basePackage}.{context}.application.shared.TestDomainEventPublisher;
import {basePackage}.{context}.domain.{aggregate}.{Aggregate};
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

@DisplayName("{Name}UseCase")
class {Name}UseCaseTest {

  private Test{Aggregate}Repository repository;
  private TestDomainEventPublisher eventPublisher;
  private {Name}UseCase useCase;

  @BeforeEach
  void setUp() {
    repository = new Test{Aggregate}Repository();
    eventPublisher = new TestDomainEventPublisher();
    useCase = new {Name}UseCase(repository, eventPublisher);
  }

  @Nested
  @DisplayName("execute")
  class Execute {

    @Test
    @DisplayName("{one behaviour, stated in ubiquitous language}")
    void {behaviour}() {
      // Arrange — build real domain state through the fake port
      {Aggregate} aggregate = {Aggregate}.create(/* ... */);
      repository.save(aggregate);
      {Name}Command command = new {Name}Command(/* ... */);

      // Act
      {Name}Result result = useCase.execute(command);

      // Assert — on the Result and on observable state, not internals
      assertNotNull(result);
      assertTrue(repository.findById(aggregate.id()).isPresent());
    }
  }
}
```

## Shared test doubles (`src/test/java/.../{context}/application/shared/`)

The fakes are top-level classes in the **test** source set, next to the ports they double, so every use-case
test of the context reuses the same two files. With several use cases, private inner copies would otherwise
multiply — one drifting fake repository per test class. They are `public` only because the tests that use
them live in the sibling packages `application/{usecasename}`; being test code, they never reach production.

### `Test{Aggregate}Repository.java`

```java
package {basePackage}.{context}.application.shared;

import {basePackage}.{context}.domain.{aggregate}.{Aggregate};
import {basePackage}.{context}.domain.{aggregate}.{Aggregate}Id;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

/** Hand-written fake of the repository port — a real Map store, no Mockito. */
public class Test{Aggregate}Repository implements {Aggregate}Repository {

  private final Map<{Aggregate}Id, {Aggregate}> store = new ConcurrentHashMap<>();

  @Override
  public Optional<{Aggregate}> findById({Aggregate}Id id) {
    return Optional.ofNullable(store.get(id));
  }

  @Override
  public {Aggregate} save({Aggregate} aggregate) {
    store.put(aggregate.id(), aggregate);
    return aggregate;
  }

  @Override
  public void deleteById({Aggregate}Id id) {
    store.remove(id);
  }
  // implement the remaining domain-language finders the port declares
}
```

### `TestDomainEventPublisher.java`

```java
package {basePackage}.{context}.application.shared;

import dev.domaincentric.dca.buildingblocks.ddd.tactical.AggregateRoot;
import dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainEvent;
import dev.domaincentric.dca.buildingblocks.hexagonal.port.out.DomainEventPublisher;
import java.util.ArrayList;
import java.util.List;

/** Hand-written fake of the publisher port — records what was published. */
public class TestDomainEventPublisher implements DomainEventPublisher {

  private final List<DomainEvent> published = new ArrayList<>();

  @Override
  public void publish(DomainEvent event) {
    published.add(event);
  }

  @Override
  public void publishAndClearEvents(AggregateRoot<?, ?> aggregate) {
    published.addAll(aggregate.domainEvents());
    aggregate.clearDomainEvents();
  }

  public List<DomainEvent> published() {
    return published;
  }
}
```

The fake repository is a real `Map` store, so `save` then `findById` round-trips actual aggregates — the test verifies orchestration end-to-end within the application layer. To assert event hygiene, check `eventPublisher.published()` (the use case must publish, and `publishAndClearEvents` must leave `aggregate.domainEvents()` empty).

## Realizes / governed by

- Markers: [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md) · [Repository<T, ID>](/marker/port-out/repository.md) · [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- Recipe: [Test a use case](/recipe/test-a-use-case.md) · [Add a use case](/recipe/add-a-use-case.md)
- Reference tests: `cart/application/mergecarts/MergeCartsUseCaseTest`, `pricing/application/getpricesforproducts/GetPricesForProductsUseCaseTest`
