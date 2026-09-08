---
type: Rule
id: DCA-TAC-002
title: Aggregate Roots must not hold references to Repositories or other Output Ports
rule: "Aggregates are persistence-ignorant: repositories and services are passed as method parameters by the use case, never injected as fields."
constraint: Aggregate Roots must not hold references to Repositories or other Output Ports.
selects: "Non-interface classes anywhere under scan assignable to AggregateRoot, abstract ones included."
checks: No field of the class - inherited and static ones included - has a raw type assignable to Repository or to any other OutputPort. Only the raw type is inspected; a port hidden in a generic type argument is not seen. A port passed as a method parameter is not a field and passes.
enforced_by: "TacticalPatternRules#DCA-TAC-002"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Non-interface classes anywhere under scan assignable to AggregateRoot, abstract ones included.

## Check

No field of the class - inherited and static ones included - has a raw type assignable to Repository or to any other OutputPort. Only the raw type is inspected; a port hidden in a generic type argument is not seen. A port passed as a method parameter is not a field and passes.

## .NET reading

**Selection.** Non-interface types below the root namespace assignable to IAggregateRoot, abstract ones included.

**Check.** No field or property of the type - inherited and static ones included, record plumbing skipped - has a type assignable to IRepository or to any other IOutputPort. Only the member's own type is inspected; a port hidden in a generic type argument is not seen. A port passed as a method parameter is not a member and passes.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-002",
        "Aggregate Roots must not hold references to Repositories or other Output Ports",
        "Aggregates are persistence-ignorant: repositories and services are passed as method"
            + " parameters by the use case, never injected as fields",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass aggregate : concreteClassesAssignableTo(arch, AggregateRoot.class)) {
            for (JavaField field : aggregate.getAllFields()) {
              JavaClass fieldType = field.getRawType();
              if (fieldType.isAssignableTo(Repository.class)
                  || fieldType.isAssignableTo(OutputPort.class)) {
                violations.add(
                    aggregate.getName()
                        + " has field '"
                        + field.getName()
                        + "' of type "
                        + fieldType.getName()
                        + " which is a repository/output port");
              }
            }
          }
          fail(
              "Aggregates must not have injected repositories or output ports - pass dependencies"
                  + " as method parameters.",
              violations);
        })
    .selecting(
        "Non-interface classes anywhere under scan assignable to AggregateRoot, "
            + "abstract ones included.")
    .checking(
        "No field of the class - inherited and static ones included - has a raw type "
            + "assignable to Repository or to any other OutputPort. Only the raw type is "
            + "inspected; a port hidden in a generic type argument is not seen. A port passed "
            + "as a method parameter is not a field and passes.")
```

## Helpers

### `concreteClassesAssignableTo`

```java
private static List<JavaClass> concreteClassesAssignableTo(
    DcaArchitecture arch, Class<?> marker) {
  return classesMatching(arch, c -> c.isAssignableTo(marker) && !c.isInterface());
}
```

### `fail`

```java
private static void fail(String message, List<String> violations) {
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(message, violations);
  }
}
```

### `classesMatching`

```java
private static List<JavaClass> classesMatching(
    DcaArchitecture arch, Predicate<JavaClass> filter) {
  return arch.classes().stream().filter(filter).collect(Collectors.toList());
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
