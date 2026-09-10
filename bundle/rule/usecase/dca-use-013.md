---
type: Rule
id: DCA-USE-013
title: Declaratively transactional use cases must not call remote-capable output ports
rule: "A declaratively transactional use case holds a database connection for its whole run. Calling an output port that may leave the process (another context's API, a payment provider, a mail gateway) inside it blocks that connection for the remote round trip; under load the pool runs dry, and a rollback cannot undo the remote effect. Only transactional resources belong inside the boundary: Repository, Store, DomainEventPublisher, IntegrationEventPublisher. Everything else is called before the transaction - draw the boundary by hand with TransactionBoundary.inTransaction(...) - or after it, as a reaction to an integration event."
constraint: Declaratively transactional use cases must not call remote-capable output ports.
selects: "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix."
checks: "Every method that runs under one of the configured transactional annotations - on the class, on itself, or on a method that reaches it within the class - calls no OutputPort other than Repository, Store, DomainEventPublisher or IntegrationEventPublisher. A use case without such an annotation (explicit TransactionBoundary or none) is selected but never reported; with an empty role nothing is ever reported."
enforced_by: "UseCaseRules#DCA-USE-013"
status: enforced
rule_set: usecase
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
not_applicable_dotnet: "Remote-call containment in explicit delegate boundaries cannot be established by this declaration-anchored rule. USE-012 checks publication entry-path coverage, not runtime block containment; review remote effects manually"
---

# Declaratively transactional use cases must not call remote-capable output ports

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

Every method that runs under one of the configured transactional annotations - on the class, on itself, or on a method that reaches it within the class - calls no OutputPort other than Repository, Store, DomainEventPublisher or IntegrationEventPublisher. A use case without such an annotation (explicit TransactionBoundary or none) is selected but never reported; with an empty role nothing is ever reported.

## Implementation

```java
DcaRule.of(
        "DCA-USE-013",
        "Declaratively transactional use cases must not call remote-capable output ports",
        "A declaratively transactional use case holds a database connection for its whole run."
            + " Calling an"
            + " output port that may leave the process (another context's API, a payment provider,"
            + " a mail gateway) inside it blocks that connection for the remote round trip; under"
            + " load the pool runs dry, and a rollback cannot undo the remote effect. Only"
            + " transactional resources belong inside the boundary: Repository, Store,"
            + " DomainEventPublisher, IntegrationEventPublisher. Everything else is called before"
            + " the transaction - draw the boundary by hand with TransactionBoundary.inTransaction(...)"
            + " - or after it, as a reaction to an integration event",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .haveSimpleNameEndingWith(layout.useCaseSuffix())
                .or()
                .areAssignableTo(InputPort.class)
                .and()
                .areNotInterfaces()
                .should(
                    notCallRemotePortsWhenTransactional(
                        layout.frameworkAnnotations().transactional()))
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.")
    .checking(
        "Every method that runs under one of the configured transactional annotations - on the"
            + " class, on itself, or on a method that reaches it within the class - calls no"
            + " OutputPort other than Repository, Store, DomainEventPublisher or"
            + " IntegrationEventPublisher. A use case without such an annotation (explicit"
            + " TransactionBoundary or none) is selected but never reported; with an empty role"
            + " nothing is ever reported.")
```

## Helpers

### `notCallRemotePortsWhenTransactional`

```java
private static ArchCondition<JavaClass> notCallRemotePortsWhenTransactional(
    List<String> transactional) {
  return new ArchCondition<>("not call remote-capable output ports while transactional") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        if (!isTransactional(item, unit, calls, transactional)) {
          continue;
        }
        List<String> remotePorts =
            unit.getMethodCallsFromSelf().stream()
                .map(call -> call.getTargetOwner())
                .filter(owner -> owner.isAssignableTo(OutputPort.class))
                .filter(owner -> !isTransactionalResource(owner))
                .map(JavaClass::getSimpleName)
                .distinct()
                .sorted()
                .toList();
        if (!remotePorts.isEmpty()) {
          events.add(
              SimpleConditionEvent.violated(
                  item,
                  item.getSimpleName()
                      + "."
                      + unit.getName()
                      + " runs under "
                      + FrameworkAnnotations.describe(transactional, "a transaction annotation")
                      + " and calls "
                      + String.join(", ", remotePorts)
                      + " inside the transaction - call it before, or draw the boundary with"
                      + " TransactionBoundary.inTransaction(...)"));
        }
      }
    }
  };
}
```

### `isTransactional`

```java
/**
   * Whether the unit may run inside declared transaction metadata: the class is annotated, the unit
   * is, or a unit that reaches it through calls within the class is. Used where one covered path is
   * enough to matter (a remote call inside a transaction).
   */
  private static boolean isTransactional(
      JavaClass item, JavaCodeUnit unit, IntraClassCalls calls, List<String> transactional) {
    return AnnotationRoles.isMetaAnnotatedWithAny(item, transactional)
        || calls.callersOf(unit).stream()
            .anyMatch(u -> AnnotationRoles.isMetaAnnotatedWithAny(u, transactional));
  }
```

### `isTransactionalResource`

```java
/**
   * Output ports that live inside the transaction; every other output port may leave the process.
   */
  private static boolean isTransactionalResource(JavaClass owner) {
    return owner.isAssignableTo(Repository.class)
        || owner.isAssignableTo(Store.class)
        || owner.isAssignableTo(DomainEventPublisher.class)
        || owner.isAssignableTo(IntegrationEventPublisher.class);
  }
```

### `AnnotationRoles.isMetaAnnotatedWithAny`

```java
/** Meta-annotated with any annotation of the role; false for an empty role. */
  static boolean isMetaAnnotatedWithAny(CanBeAnnotated item, List<String> role) {
    for (String fqn : role) {
      if (item.isMetaAnnotatedWith(fqn)) {
        return true;
      }
    }
    return false;
  }
```

### `IntraClassCalls.callersOf`

```java
/** The unit itself and every unit that reaches it through calls within the class. */
  Set<JavaCodeUnit> callersOf(JavaCodeUnit unit) {
    return closure(unit, callers);
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

## Related mentions (heuristic)

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [InputPort](/marker/port-in/inputport.md)
- [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)
- [TransactionBoundary](/marker/application/transactionboundary.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
