---
type: Rule
id: DCA-USE-012
title: Use cases that publish domain events must have a transaction boundary
rule: "Integration events are relayed after commit (@TransactionalEventListener, @ApplicationModuleListener) and their publication is registered in the publishing transaction. Without an active transaction the after-commit listeners are skipped silently and nothing is registered: the use case succeeds, the other contexts never hear of it. The use case that publishes owns the boundary - either declarative transaction metadata (@Transactional on the class or the executing method) or an explicit TransactionBoundary.inTransaction(...) around save and publish. Checked per entry path, following calls within the class: from every entry point - a method callable from outside the class, or one nothing in the class calls - no route down to the publishing method may be free of an annotation or a boundary; a covered caller does not cover another route to the same helper, and a boundary on one route does not cover a second route. Whether the publication sits inside the block handed to inTransaction(...) is not visible in ArchUnit's call model, which folds a lambda's body into the enclosing method; that placement stays a review check."
constraint: Use cases that publish domain events must have a transaction boundary.
selects: "Non-interface classes in <module>.application.. whose simple name ends with the configured use-case suffix."
checks: "For every method that calls a DomainEventPublisher, every route from each entry point down to it is covered: the class carries the configured @Transactional, or every uncovered unit on the route is either annotated or calls TransactionBoundary.inTransaction. A covered caller does not cover a second route to the same helper. Whether the publish call sits inside the inTransaction block is not checked - ArchUnit folds a lambda into its enclosing method."
enforced_by: "UseCaseRules#DCA-USE-012"
status: enforced
rule_set: usecase
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
not_applicable_dotnet: "Guards Spring's after-commit relay (@TransactionalEventListener / @ApplicationModuleListener), which is skipped silently without an active transaction. .NET has no ambient transaction attribute on use cases; after-save delivery is the job of the integration-event outbox adapter, not of the use case"
---

## Selection

Non-interface classes in <module>.application.. whose simple name ends with the configured use-case suffix.

## Check

For every method that calls a DomainEventPublisher, every route from each entry point down to it is covered: the class carries the configured @Transactional, or every uncovered unit on the route is either annotated or calls TransactionBoundary.inTransaction. A covered caller does not cover a second route to the same helper. Whether the publish call sits inside the inTransaction block is not checked - ArchUnit folds a lambda into its enclosing method.

## Implementation

```java
DcaRule.of(
        "DCA-USE-012",
        "Use cases that publish domain events must have a transaction boundary",
        "Integration events are relayed after commit (@TransactionalEventListener,"
            + " @ApplicationModuleListener) and their publication is registered in the publishing"
            + " transaction. Without an active transaction the after-commit listeners are skipped"
            + " silently and nothing is registered: the use case succeeds, the other contexts never"
            + " hear of it. The use case that publishes owns the boundary - either declarative"
            + " transaction metadata (@Transactional on the class or the executing method) or an"
            + " explicit TransactionBoundary.inTransaction(...) around save and publish. Checked"
            + " per entry path, following calls within the class: from every entry point - a"
            + " method callable from outside the class, or one nothing in the class calls - no route"
            + " down to the publishing method may be free of an annotation or a boundary; a covered"
            + " caller does not cover another route to the same helper, and a boundary on one route"
            + " does not cover a second route. Whether the publication sits inside the block"
            + " handed to inTransaction(...) is not visible in ArchUnit's call model, which folds a"
            + " lambda's body into the enclosing method; that placement stays a review check",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .haveSimpleNameEndingWith(layout.useCaseSuffix())
                .and()
                .areNotInterfaces()
                .should(
                    beTransactionalWhenPublishing(
                        layout.frameworkAnnotations().transactional()))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. whose simple name ends with the configured use-case suffix.")
    .checking(
        "For every method that calls a DomainEventPublisher, every route from each entry point down to it is covered: the class carries the configured @Transactional, or every uncovered unit on the route is either annotated or calls TransactionBoundary.inTransaction. A covered caller does not cover a second route to the same helper. Whether the publish call sits inside the inTransaction block is not checked - ArchUnit folds a lambda into its enclosing method.")
```

## Helpers

### `beTransactionalWhenPublishing`

```java
private static ArchCondition<JavaClass> beTransactionalWhenPublishing(String transactional) {
  return new ArchCondition<>("be transactional when publishing domain events") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        if (!calls(unit, DomainEventPublisher.class)) {
          continue;
        }
        for (JavaCodeUnit entry : calls.entryPointsOf(unit)) {
          if (pathIsTransactional(item, entry, unit, calls, transactional)) {
            continue;
          }
          events.add(
              SimpleConditionEvent.violated(
                  item,
                  item.getSimpleName()
                      + "."
                      + pathName(entry, unit)
                      + " publishes domain events without @"
                      + simpleName(transactional)
                      + " on the class or on a method of that path, and without"
                      + " TransactionBoundary.inTransaction(...) on it - after-commit"
                      + " listeners are skipped"));
        }
      }
    }
  };
}
```

### `calls`

```java
private static boolean calls(JavaCodeUnit unit, Class<?> targetType) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(call -> call.getTargetOwner().isAssignableTo(targetType));
}

private static boolean calls(JavaCodeUnit unit, Class<?> targetType, String methodName) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(
          call ->
              call.getTarget().getName().equals(methodName)
                  && call.getTargetOwner().isAssignableTo(targetType));
}
```

### `pathIsTransactional`

```java
/**
   * Whether every route from {@code entry} down to {@code publisher} is covered: the class is
   * annotated, or no route reaches the publisher through units none of which carries the annotation
   * or draws an explicit boundary. A boundary on one route does not cover another route to the same
   * publisher.
   */
  private static boolean pathIsTransactional(
      JavaClass item,
      JavaCodeUnit entry,
      JavaCodeUnit publisher,
      IntraClassCalls calls,
      String transactional) {
    if (item.isMetaAnnotatedWith(transactional)) {
      return true;
    }
    Predicate<JavaCodeUnit> uncovered =
        unit -> !unit.isMetaAnnotatedWith(transactional) && !callsBoundary(unit);
    return !calls.reachableThrough(entry, uncovered).contains(publisher);
  }
```

### `pathName`

```java
/** {@code execute} for the unit itself, {@code execute (via persist)} when reached through it. */
  private static String pathName(JavaCodeUnit entry, JavaCodeUnit unit) {
    return entry.equals(unit) ? entry.getName() : entry.getName() + " (via " + unit.getName() + ")";
  }
```

### `simpleName`

```java
private static String simpleName(String annotation) {
  return annotation.substring(annotation.lastIndexOf('.') + 1);
}
```

### `IntraClassCalls.entryPointsOf`

```java
/**
   * The paths a unit can be entered on: those of its (transitive) callers - the unit itself
   * included - that are entry points. A unit is an entry point when it can be called from outside
   * the class (any code unit that is not private, synthetic or a bridge - a public method stays an
   * entry point even when another method of the class also calls it) or when no unit of the class
   * calls it. When the unit is reached only from within a cycle of private helpers, so that no
   * caller qualifies, the unit itself is taken as the entry point.
   */
  Set<JavaCodeUnit> entryPointsOf(JavaCodeUnit unit) {
    Set<JavaCodeUnit> roots = new LinkedHashSet<>();
    for (JavaCodeUnit caller : callersOf(unit)) {
      if (isEntryPoint(caller)) {
        roots.add(caller);
      }
    }
    if (roots.isEmpty()) {
      roots.add(unit);
    }
    return roots;
  }
```

### `callsBoundary`

```java
private static boolean callsBoundary(JavaCodeUnit unit) {
  return unit.getMethodCallsFromSelf().stream()
      .anyMatch(call -> call.getTargetOwner().isAssignableTo(TransactionBoundary.class));
}
```

### `IntraClassCalls.reachableThrough`

```java
/**
   * The units reachable from {@code start} on routes that pass only through units satisfying {@code
   * through} - {@code start} included, and only if it satisfies it too. A unit that fails the
   * predicate is not entered, so nothing behind it is reached on that route (it may still be
   * reached on another). Cycle-safe.
   */
  Set<JavaCodeUnit> reachableThrough(JavaCodeUnit start, Predicate<JavaCodeUnit> through) {
    Set<JavaCodeUnit> reached = new LinkedHashSet<>();
    Deque<JavaCodeUnit> pending = new ArrayDeque<>();
    pending.add(start);
    while (!pending.isEmpty()) {
      JavaCodeUnit current = pending.remove();
      if (through.test(current) && reached.add(current)) {
        pending.addAll(callees.getOrDefault(current, Set.of()));
      }
    }
    return reached;
  }
```

### `IntraClassCalls.callersOf`

```java
/** The unit itself and every unit that reaches it through calls within the class. */
  Set<JavaCodeUnit> callersOf(JavaCodeUnit unit) {
    return closure(unit, callers);
  }
```

### `IntraClassCalls.isEntryPoint`

```java
private boolean isEntryPoint(JavaCodeUnit unit) {
  Set<JavaModifier> modifiers = unit.getModifiers();
  boolean externallyCallable =
      !modifiers.contains(JavaModifier.PRIVATE)
          && !modifiers.contains(JavaModifier.SYNTHETIC)
          && !modifiers.contains(JavaModifier.BRIDGE);
  return externallyCallable || callers.getOrDefault(unit, Set.of()).isEmpty();
}
```

### `IntraClassCalls.closure`

```java
private static Set<JavaCodeUnit> closure(
    JavaCodeUnit start, Map<JavaCodeUnit, Set<JavaCodeUnit>> edges) {
  Set<JavaCodeUnit> reached = new LinkedHashSet<>();
  Deque<JavaCodeUnit> pending = new ArrayDeque<>();
  pending.add(start);
  while (!pending.isEmpty()) {
    JavaCodeUnit current = pending.remove();
    if (reached.add(current)) {
      pending.addAll(edges.getOrDefault(current, Set.of()));
    }
  }
  return reached;
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [TransactionBoundary](/marker/application/transactionboundary.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
