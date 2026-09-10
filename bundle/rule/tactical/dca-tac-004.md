---
type: Rule
id: DCA-TAC-004
title: Entities must have an ID field
rule: "An Entity is defined by its identity, which is a value object implementing the Id marker."
constraint: Entities must have an ID field.
selects: "Non-interface, non-abstract classes anywhere under scan assignable to Entity - aggregate roots included, since AggregateRoot extends Entity."
checks: "At least one field - inherited ones included - has a raw type assignable to the Id marker. A String or UUID identity does not count, and the field's name plays no role."
enforced_by: "TacticalPatternRules#DCA-TAC-004"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Entities must have an ID field

## Selection

Non-interface, non-abstract classes anywhere under scan assignable to Entity - aggregate roots included, since AggregateRoot extends Entity.

## Check

At least one field - inherited ones included - has a raw type assignable to the Id marker. A String or UUID identity does not count, and the field's name plays no role.

## .NET reading

**Selection.** Non-interface, non-abstract types below the root namespace assignable to IEntity - aggregate roots included, since IAggregateRoot extends IEntity.

**Check.** At least one field or property - inherited ones included, private fields of base classes seen through reflection - has a type assignable to the IId marker. A string or Guid identity does not count, and the member's name plays no role.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-004",
        "Entities must have an ID field",
        "An Entity is defined by its identity, which is a value object implementing the Id marker",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass entity : concreteClassesAssignableTo(arch, Entity.class)) {
            if (entity.getModifiers().contains(JavaModifier.ABSTRACT)) {
              continue;
            }
            boolean hasIdField =
                entity.getAllFields().stream()
                    .anyMatch(f -> f.getRawType().isAssignableTo(Id.class));
            if (!hasIdField) {
              violations.add(
                  entity.getName()
                      + " has no field whose type implements "
                      + Id.class.getSimpleName());
            }
          }
          fail(
              "Entities must have an identity field typed as an Id value object (DDD pattern).",
              violations);
        })
    .selecting(
        "Non-interface, non-abstract classes anywhere under scan assignable to Entity - "
            + "aggregate roots included, since AggregateRoot extends Entity.")
    .checking(
        "At least one field - inherited ones included - has a raw type assignable to "
            + "the Id marker. A String or UUID identity does not count, and the field's name "
            + "plays no role.")
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
    "DCA-TAC-004",
    "Entities must have an ID field",
    "An Entity is defined by its identity, which is a value object implementing the IId marker",
    arch =>
    {
        var violations = new List<string>();
        foreach (var entity in ConcreteTypesAssignableTo(arch, typeof(IEntity)))
        {
            if (entity is Class { IsAbstract: true })
            {
                continue;
            }

            var hasIdMember = DataMembers(arch, entity).Any(m => IsAssignableTo(arch, m.Type, typeof(IId)))
                || RuntimeDataMemberTypes(arch, entity).Any(t => typeof(IId).IsAssignableFrom(t));
            if (!hasIdMember)
            {
                violations.Add($"{entity.FullName} has no field or property whose type implements {nameof(IId)}");
            }
        }

        DcaRule.Fail("Entities must have an identity field typed as an IId value object (DDD pattern).", violations);
    })
    .Selecting(
        "Non-interface, non-abstract types below the root namespace assignable to "
        + "IEntity - aggregate roots included, since IAggregateRoot extends IEntity.")
    .Checking(
        "At least one field or property - inherited ones included, private fields of "
        + "base classes seen through reflection - has a type assignable to the IId "
        + "marker. A string or Guid identity does not count, and the member's name "
        + "plays no role.")
```

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
- [Id](/marker/tactical/id.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
