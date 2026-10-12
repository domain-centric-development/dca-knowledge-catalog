---
type: Rule
id: DCA-TAC-023
title: Aggregate Roots must not declare public constructors
rule: "An aggregate comes into being in two ways - created as a business fact or reconstituted from storage - and each is a named factory method. A public constructor is a third, unnamed way that skips the creation invariants and the event creation raises."
constraint: Aggregate Roots must not declare public constructors.
selects: "Concrete, non-record classes anywhere under scan assignable to AggregateRoot. Abstract base classes are not selected - their constructors are reachable only from a subclass. Records are not selected: the language fixes a record's canonical constructor at the record's own visibility, so a record root guards its invariants in that constructor instead."
checks: "No constructor declared by the class itself is public. Private, package-private and protected constructors pass - a persistence framework that needs a no-argument constructor gets a non-public one. Who calls the factory methods is not checked. An empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-023"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Aggregate Roots must not declare public constructors

## Selection

Concrete, non-record classes anywhere under scan assignable to AggregateRoot. Abstract base classes are not selected - their constructors are reachable only from a subclass. Records are not selected: the language fixes a record's canonical constructor at the record's own visibility, so a record root guards its invariants in that constructor instead.

## Check

No constructor declared by the class itself is public. Private, package-private and protected constructors pass - a persistence framework that needs a no-argument constructor gets a non-public one. Who calls the factory methods is not checked. An empty selection passes.

## .NET reading

**Selection.** Concrete, non-record classes below the root namespace assignable to IAggregateRoot. Abstract base classes are not selected - their constructors are reachable only from a subclass. Records are not selected: a positional record's primary constructor is public by the language, so a record root guards its invariants in that constructor instead. Structs are not selected either - a struct's parameterless constructor is always public.

**Check.** No instance constructor declared by the class itself is public. Private, internal, protected and private protected constructors pass - a persistence framework that needs a parameterless constructor gets a non-public one. Static constructors are not constructors in this sense. Who calls the factory methods is not checked. An empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-023",
        "Aggregate Roots must not declare public constructors",
        "An aggregate comes into being in two ways - created as a business fact or reconstituted"
            + " from storage - and each is a named factory method. A public constructor is a"
            + " third, unnamed way that skips the creation invariants and the event creation"
            + " raises",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass root : aggregateRootClasses(arch)) {
            for (var constructor : root.getConstructors()) {
              if (constructor.getModifiers().contains(JavaModifier.PUBLIC)) {
                violations.add(
                    root.getName()
                        + " declares public constructor "
                        + constructor.getFullName());
              }
            }
          }
          fail(
              "Aggregate Roots are created and reconstituted through named factory methods."
                  + " Fix: make the constructor private and add a static create(...) for a new"
                  + " aggregate and a static reconstitute(...) for the outgoing adapter that"
                  + " loads one.",
              violations);
        })
    .selecting(
        "Concrete, non-record classes anywhere under scan assignable to AggregateRoot. Abstract"
            + " base classes are not selected - their constructors are reachable only from a"
            + " subclass. Records are not selected: the language fixes a record's canonical"
            + " constructor at the record's own visibility, so a record root guards its"
            + " invariants in that constructor instead.")
    .checking(
        "No constructor declared by the class itself is public. Private, package-private and"
            + " protected constructors pass - a persistence framework that needs a no-argument"
            + " constructor gets a non-public one. Who calls the factory methods is not"
            + " checked. An empty selection passes.")
```

## Helpers

### `aggregateRootClasses`

```java
private static List<JavaClass> aggregateRootClasses(DcaArchitecture arch) {
  return classesMatching(
      arch,
      c ->
          c.isAssignableTo(arch.layout().markers().aggregateRoot())
              && !c.isInterface()
              && !c.getModifiers().contains(JavaModifier.ABSTRACT)
              && !c.isRecord());
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-023",
    "Aggregate Roots must not declare public constructors",
    "An aggregate comes into being in two ways - created as a business fact or reconstituted"
        + " from storage - and each is a named factory method. A public constructor is a"
        + " third, unnamed way that skips the creation invariants and the event creation"
        + " raises",
    arch =>
    {
        var violations = new List<string>();
        foreach (var root in AggregateRootClasses(arch))
        {
            foreach (var constructor in PublicInstanceConstructors(arch, root))
            {
                violations.Add($"{root.FullName} declares public constructor {constructor}");
            }
        }

        DcaRule.Fail(
            "Aggregate Roots are created and reconstituted through named factory methods.",
            violations,
            "make the constructor private and add a static Create(...) for a new aggregate and a"
                + " static Reconstitute(...) for the outgoing adapter that loads one.");
    })
    .Selecting(
        "Concrete, non-record classes below the root namespace assignable to IAggregateRoot."
        + " Abstract base classes are not selected - their constructors are reachable only from a"
        + " subclass. Records are not selected: a positional record's primary constructor is public"
        + " by the language, so a record root guards its invariants in that constructor instead."
        + " Structs are not selected either - a struct's parameterless constructor is always public.")
    .Checking(
        "No instance constructor declared by the class itself is public. Private, internal,"
        + " protected and private protected constructors pass - a persistence framework that needs"
        + " a parameterless constructor gets a non-public one. Static constructors are not"
        + " constructors in this sense. Who calls the factory methods is not checked. An empty"
        + " selection passes.")
```

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
