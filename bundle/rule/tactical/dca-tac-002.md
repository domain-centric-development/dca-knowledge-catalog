---
type: Rule
id: DCA-TAC-002
title: Aggregate Roots must not hold references to Repositories or other Output Ports
rule: "Aggregates are persistence-ignorant: use cases retrieve facts; external calculations belong in domain services over supplied snapshots. Review callback parameters manually; this field check cannot prove semantic responsibility."
constraint: Aggregate Roots must not hold references to Repositories or other Output Ports.
selects: "Non-interface classes anywhere under scan assignable to AggregateRoot, abstract ones included."
checks: No field of the class - inherited and static ones included - has a raw type assignable to Repository or to any other OutputPort. Only the raw type is inspected; a port hidden in a generic type argument is not seen. A port passed as a method parameter is not a field and passes.
enforced_by: "TacticalPatternRules#DCA-TAC-002"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Aggregate Roots must not hold references to Repositories or other Output Ports

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
        "Aggregates are persistence-ignorant: use cases retrieve facts; external calculations belong"
            + " in domain services over supplied snapshots. Review callback parameters manually; this field check cannot prove semantic responsibility",
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
              "Aggregates must not have injected repositories or output ports; pass facts instead.",
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
### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-002",
    "Aggregate Roots must not hold references to Repositories or other Output Ports",
    "Aggregates are persistence-ignorant: use cases retrieve facts; external calculations belong"
    + " in domain services over supplied snapshots. Review callback parameters manually; this field check cannot prove semantic responsibility",
    arch =>
    {
        var violations = new List<string>();
        foreach (var aggregate in ConcreteTypesAssignableTo(arch, typeof(IAggregateRoot)))
        {
            foreach (var member in DataMembers(arch, aggregate))
            {
                var fieldType = member.Type;
                if (IsAssignableTo(arch, fieldType, typeof(IRepository)) || IsAssignableTo(arch, fieldType, typeof(IOutputPort)))
                {
                    violations.Add($"{FieldDescription(aggregate, member)} which is a repository/output port");
                }
            }
        }

        DcaRule.Fail(
            "Aggregates must not have injected repositories or output ports; pass facts instead.",
            violations);
    })
    .Selecting(
        "Non-interface types below the root namespace assignable to IAggregateRoot, "
        + "abstract ones included.")
    .Checking(
        "No field or property of the type - inherited and static ones included, "
        + "record plumbing skipped - has a type assignable to IRepository or to any "
        + "other IOutputPort. Only the member's own type is inspected; a port hidden in "
        + "a generic type argument is not seen. A port passed as a method parameter is "
        + "not a member and passes.")
```

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
