---
type: Rule
id: DCA-STR-008
title: Integration Events should have immutable shape
rule: "Integration Events must be immutable to ensure event integrity across contexts (Event Sourcing best practice)."
constraint: Integration Events should have immutable shape.
selects: Non-interface classes assignable to IntegrationEvent - directly or through a sub-interface - anywhere on the classpath under scan.
checks: "The class is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter). Referenced objects and collection contents are not inspected. Interfaces are excluded."
enforced_by: "StrategicPatternRules#DCA-STR-008"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/StrategicPatternRules.cs
---

# Integration Events should have immutable shape

## Selection

Non-interface classes assignable to IntegrationEvent - directly or through a sub-interface - anywhere on the classpath under scan.

## Check

The class is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter). Referenced objects and collection contents are not inspected. Interfaces are excluded.

## .NET reading

**Selection.** Non-interface types below the root namespace whose implemented interfaces include IIntegrationEvent - directly or through a derived interface; classes, records and structs alike, compiler-generated types excluded.

**Check.** Classes are sealed or records; structs are allowed. Every inherited instance field is readonly, every property is get-only or init-only and no instance Set*(x): void method exists. Referenced objects and collection contents are not inspected.

## Implementation

```java
DcaRule.of(
        "DCA-STR-008",
        "Integration Events should have immutable shape",
        "Integration Events must be immutable to ensure event integrity across contexts (Event"
            + " Sourcing best practice)",
        arch ->
            classes()
                .that()
                .implement(IntegrationEvent.class)
                .should(TypeInspection.haveImmutableShape())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes assignable to IntegrationEvent - directly or through a"
            + " sub-interface - anywhere on the classpath under scan.")
    .checking(
        "The class is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter)."
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
                        && SETTER_NAME.matcher(m.getName()).matches()
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
        "DCA-STR-008",
        "Integration Events should have immutable shape",
        "Integration Events must be immutable to ensure event integrity across contexts (Event Sourcing best practice)",
        arch =>
        {
            var violations = arch.Types
                .Where(t => t is not Interface && !t.IsCompilerGenerated)
                .Where(t => t.ImplementedInterfaces.Any(i => i.FullName == typeof(IIntegrationEvent).FullName))
                .Where(t => !TacticalPatternRules.IsImmutableShape(t))
                .Select(t => "Integration event " + t.FullName + " has mutable shape")
                .ToList();
            DcaRule.Fail(
                "Integration Events should have immutable shape",
                violations,
                "declare the event as a sealed record (or record struct)");
        })
    .Selecting(
        "Non-interface types below the root namespace whose implemented interfaces include"
            + " IIntegrationEvent - directly or through a derived interface; classes, records and structs"
            + " alike, compiler-generated types excluded.")
    .Checking(
        "Classes are sealed or records; structs are allowed. Every inherited instance field is readonly, every property is get-only or init-only and no instance Set*(x): void method exists. Referenced objects and collection contents are not inspected." )
```

## Related mentions (heuristic)

- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
