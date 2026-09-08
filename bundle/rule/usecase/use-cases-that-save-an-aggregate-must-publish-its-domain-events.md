---
type: Rule
id: DCA-USE-009
title: Use cases that save an aggregate must publish its domain events
rule: "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the instance they may later be published out of context. Publishing belongs after the save, in the use case that owns the unit of work - even when the action raised no event. Checked per entry path, following calls within the use case class: every entry point that reaches a save - a method callable from outside the class, or one nothing in the class calls - must also reach a publication; a wrapper that publishes does not cover a direct call of the public method it wraps, and a helper two methods share does not connect them. That the publication follows the save and concerns the same aggregate is not established statically. Only DomainEventPublisher.publishAndClearEvents counts as a publication: iterating domainEvents() and calling publish(event), even followed by clearDomainEvents(), separates dispatch from acknowledgement and is not accepted."
constraint: Use cases that save an aggregate must publish its domain events.
selects: "Non-interface classes in <module>.application.. whose simple name ends with the configured use-case suffix."
checks: "For every method of the class that calls Repository.save, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of DomainEventPublisher.publishAndClearEvents. Only publishAndClearEvents counts - publish(event), even followed by clearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes."
enforced_by: "UseCaseRules#DCA-USE-009"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

## Selection

Non-interface classes in <module>.application.. whose simple name ends with the configured use-case suffix.

## Check

For every method of the class that calls Repository.save, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of DomainEventPublisher.publishAndClearEvents. Only publishAndClearEvents counts - publish(event), even followed by clearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes.

## .NET reading

**Selection.** Classes in <module>.Application of every module root whose name ends with the configured use-case suffix and whose runtime type is in the loaded assemblies.

**Check.** For every method of the class that calls IRepository.SaveAsync, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of IDomainEventPublisher.PublishAndClearEventsAsync. Calls are read from the IL of the class and its nested state-machine and closure types, so async methods and lambdas are followed. Only PublishAndClearEventsAsync counts - PublishAsync(event), even followed by ClearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes.

## Implementation

```java
DcaRule.of(
        "DCA-USE-009",
        "Use cases that save an aggregate must publish its domain events",
        "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the"
            + " instance they may later be published out of context. Publishing belongs after the"
            + " save, in the use case that owns the unit of work - even when the action raised no"
            + " event. Checked per entry path, following calls within the use case class: every"
            + " entry point that reaches a save - a method callable from outside the class, or one"
            + " nothing in the class calls - must also reach a publication; a wrapper that publishes"
            + " does not cover a direct call of the public method it wraps, and a helper two methods"
            + " share does not connect them. That the"
            + " publication follows the save and concerns the same aggregate is not established"
            + " statically. Only DomainEventPublisher.publishAndClearEvents counts as a publication:"
            + " iterating domainEvents() and calling publish(event), even followed by"
            + " clearDomainEvents(), separates dispatch from acknowledgement and is not accepted",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .haveSimpleNameEndingWith(layout.useCaseSuffix())
                .and()
                .areNotInterfaces()
                .should(publishAfterSaving())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. whose simple name ends with the configured use-case suffix.")
    .checking(
        "For every method of the class that calls Repository.save, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of DomainEventPublisher.publishAndClearEvents. Only publishAndClearEvents counts - publish(event), even followed by clearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes.")
```

## Helpers

### `publishAfterSaving`

```java
private static ArchCondition<JavaClass> publishAfterSaving() {
  return new ArchCondition<>("publish the aggregate's domain events after saving it") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        if (!calls(unit, Repository.class, "save")) {
          continue;
        }
        for (JavaCodeUnit entry : calls.entryPointsOf(unit)) {
          boolean publishes =
              calls.reachableFrom(entry).stream()
                  .anyMatch(u -> calls(u, DomainEventPublisher.class, "publishAndClearEvents"));
          if (!publishes) {
            events.add(
                SimpleConditionEvent.violated(
                    item,
                    item.getSimpleName()
                        + "."
                        + pathName(entry, unit)
                        + " saves an aggregate without publishing its domain events - no"
                        + " method reached from there calls publishAndClearEvents"));
          }
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

### `pathName`

```java
/** {@code execute} for the unit itself, {@code execute (via persist)} when reached through it. */
  private static String pathName(JavaCodeUnit entry, JavaCodeUnit unit) {
    return entry.equals(unit) ? entry.getName() : entry.getName() + " (via " + unit.getName() + ")";
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

### `IntraClassCalls.reachableFrom`

```java
/** The unit itself and every unit it reaches through calls within the class. */
  Set<JavaCodeUnit> reachableFrom(JavaCodeUnit unit) {
    return closure(unit, callees);
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

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
