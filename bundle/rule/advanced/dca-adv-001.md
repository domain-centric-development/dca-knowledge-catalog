---
type: Rule
id: DCA-ADV-001
title: Domain Events must implement DomainEvent and have immutable shape
rule: "Domain events should have immutable state implementing DomainEvent (named in past tense, e.g., ProductCreated, CartCleared)."
constraint: Domain Events must implement DomainEvent and have immutable shape.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent - directly or through a supertype.
checks: "The class is final or a record with final inherited instance fields and no instance set*(x): void methods. Referenced objects and collection contents are not inspected. Interfaces are excluded."
enforced_by: "AdvancedPatternRules#DCA-ADV-001"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Domain Events must implement DomainEvent and have immutable shape

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent - directly or through a supertype.

## Check

The class is final or a record with final inherited instance fields and no instance set*(x): void methods. Referenced objects and collection contents are not inspected. Interfaces are excluded.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainEvent - directly or through a supertype.

**Check.** Classes are sealed or records; structs are allowed. Every inherited instance field is readonly, every property is get-only or init-only and no instance Set*(x): void method exists. Referenced objects and collection contents are not inspected.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-001",
        "Domain Events must implement DomainEvent and have immutable shape",
        "Domain events should have immutable state implementing DomainEvent (named in past tense,"
            + " e.g., ProductCreated, CartCleared)",
        arch ->
            classes()
                .that()
                .implement(DomainEvent.class)
                .and()
                .areNotInterfaces()
                .should(TypeInspection.haveImmutableShape())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent"
            + " - directly or through a supertype.")
    .checking(
        "The class is final or a record with final inherited instance fields and no instance set*(x): void methods."
            + " Referenced objects and collection contents are not inspected. Interfaces are excluded.")
```

## Helpers

### `TypeInspection.haveImmutableShape`

```java
static com.tngtech.archunit.lang.ArchCondition<JavaClass> haveImmutableShape() {
  return new com.tngtech.archunit.lang.ArchCondition<>("have shallow immutable instance state") {
    @Override
    public void check(JavaClass item, com.tngtech.archunit.lang.ConditionEvents events) {
      if (!isImmutableShape(item)) {
        events.add(
            com.tngtech.archunit.lang.SimpleConditionEvent.violated(
                item,
                item.getName()
                    + " must be final or a record with final instance fields and no setter methods"));
      }
    }
  };
}
```

### `TypeInspection.isImmutableShape`

```java
/** Shallow immutable state, including inherited state; referenced contents are not inspected. */
  static boolean isImmutableShape(JavaClass type) {
    return (type.isRecord() || type.getModifiers().contains(JavaModifier.FINAL))
        && instanceFields(type).stream()
            .allMatch(f -> f.getModifiers().contains(JavaModifier.FINAL))
        && type.getAllMethods().stream()
            .noneMatch(
                m ->
                    !m.getModifiers().contains(JavaModifier.STATIC)
                        && m.getName().startsWith("set")
                        && !m.getRawParameterTypes().isEmpty()
                        && m.getRawReturnType().getName().equals("void"));
  }
```

### `TypeInspection.instanceFields`

```java
/**
   * The instance fields of a class, inherited ones included, sorted by name so that reports are
   * stable across runs. Static fields — constants, counters — are not part of an object's state.
   */
  static List<JavaField> instanceFields(JavaClass type) {
    return type.getAllFields().stream()
        .filter(field -> !field.getModifiers().contains(JavaModifier.STATIC))
        .sorted(Comparator.comparing(JavaField::getName))
        .toList();
  }
```
### C# expression

```csharp
DcaRule.Check(
    "DCA-ADV-001",
    "Domain Events must implement IDomainEvent and have immutable shape",
    "Domain events should be immutable records implementing IDomainEvent (named in past tense,"
        + " e.g., ProductCreated, CartCleared)",
    arch => DcaRule.Fail(
        "Domain Events must have immutable instance state:",
        Violations(
            arch,
            t => t is not Interface && IsDomainEvent(t),
            t => !TacticalPatternRules.IsImmutableShape(t),
            t => $"{t.FullName} implements IDomainEvent but has mutable shape")))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to IDomainEvent - directly "
        + "or through a supertype.")
    .Checking(
    "Classes are sealed or records; structs are allowed. Every inherited instance field is readonly, every property is get-only or init-only and no instance Set*(x): void method exists. Referenced objects and collection contents are not inspected." )
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
