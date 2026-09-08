---
type: Rule
id: DCA-TAC-005
title: Entities must not be instantiated directly from outside the aggregate
rule: Entities are created through their aggregate root so that the root can enforce its invariants.
constraint: Entities must not be instantiated directly from outside the aggregate.
selects: "Non-interface, non-record classes anywhere under scan assignable to Entity but not to AggregateRoot; abstract ones included."
checks: "The class declares no public constructor; package-private, protected and private constructors pass. Records are skipped entirely, and aggregate roots are not selected."
enforced_by: "TacticalPatternRules#DCA-TAC-005"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Non-interface, non-record classes anywhere under scan assignable to Entity but not to AggregateRoot; abstract ones included.

## Check

The class declares no public constructor; package-private, protected and private constructors pass. Records are skipped entirely, and aggregate roots are not selected.

## .NET reading

**Selection.** Non-interface classes below the root namespace assignable to IEntity but not to IAggregateRoot; abstract ones included, records and structs excluded.

**Check.** The class declares no public constructor; internal, protected and private constructors pass. Records and structs are skipped entirely, and aggregate roots are not selected.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-005",
        "Entities must not be instantiated directly from outside the aggregate",
        "Entities are created through their aggregate root so that the root can enforce its"
            + " invariants",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass entity : nonRootEntities(arch)) {
            if (entity.isRecord()) {
              continue;
            }
            entity.getConstructors().stream()
                .filter(c -> c.getModifiers().contains(JavaModifier.PUBLIC))
                .forEach(
                    c ->
                        violations.add(
                            entity.getName()
                                + " has public constructor - should be package-private or"
                                + " protected"));
          }
          fail(
              "Entities should not have public constructors (access only through aggregate root).\n"
                  + "Note: Records are excluded from this rule.",
              violations);
        })
    .selecting(
        "Non-interface, non-record classes anywhere under scan assignable to Entity but "
            + "not to AggregateRoot; abstract ones included.")
    .checking(
        "The class declares no public constructor; package-private, protected and "
            + "private constructors pass. Records are skipped entirely, and aggregate roots "
            + "are not selected.")
```

## Helpers

### `nonRootEntities`

```java
private static List<JavaClass> nonRootEntities(DcaArchitecture arch) {
  return classesMatching(
      arch,
      c ->
          c.isAssignableTo(Entity.class)
              && !c.isAssignableTo(AggregateRoot.class)
              && !c.isInterface());
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

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
