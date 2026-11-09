---
type: Rule
id: DCA-STR-008
title: Integration Events should have immutable shape
rule: "An integration event is a published contract: once another context has read it, its shape may only grow, never change under an existing reader. A mutable event cannot make that promise - any holder can rewrite what a second consumer will read."
constraint: Integration Events should have immutable shape.
selects: Non-interface classes assignable to IntegrationEvent - directly or through a sub-interface - anywhere on the classpath under scan.
checks: "The class is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter). Referenced objects and collection contents are not inspected. Interfaces are excluded."
enforced_by: "StrategicPatternRules#DCA-STR-008"
status: enforced
maturity: released
rule_set: strategic
implementations: [java, dotnet, rust]
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

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a test, reformulated for Rust (source-test).

**Selection.** Types that implement IntegrationEvent.

**Check.** No method takes &mut self and no field type is an interior-mutability type.

## Implementation

```java
DcaRule.of(
        "DCA-STR-008",
        "Integration Events should have immutable shape",
        "An integration event is a published contract: once another context has read it, its"
            + " shape may only grow, never change under an existing reader. A mutable event"
            + " cannot make that promise - any holder can rewrite what a second consumer will"
            + " read",
        arch ->
            classes()
                .that(arch.layout().markers().is("integrationEvent"))
                .and()
                .areNotInterfaces()
                .should(TypeInspection.haveImmutableShape())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes assignable to IntegrationEvent - directly or through a"
            + " sub-interface - anywhere on the classpath under scan.")
    .checking(
        "The class is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter)."
            + " Referenced objects and collection contents are not inspected. Interfaces are excluded.",
        "declare the event as a final record")
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

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-STR-008",
        "Integration Events should have immutable shape",
        "An integration event is a published contract: once another context has read it, its shape may only grow, never change under an existing reader. A mutable event cannot make that promise - any holder can rewrite what a second consumer will read",
        arch => SelectionArchRule.ForEach(
            "integration events should have immutable shape",
            () => arch.Types
                .Where(t => t is not Interface && !t.IsCompilerGenerated)
                .Where(t => arch.Layout.Markers.Is(nameof(DcaMarkers.IntegrationEvent), t)),
            t => TacticalPatternRules.IsImmutableShape(t) ? [] : ["Integration event " + t.FullName + " has mutable shape"]))
    .Selecting(
        "Non-interface types below the root namespace whose implemented interfaces include"
            + " IIntegrationEvent - directly or through a derived interface; classes, records and structs"
            + " alike, compiler-generated types excluded.")
    .Checking(
        "Classes are sealed or records; structs are allowed. Every inherited instance field is readonly, every property is get-only or init-only and no instance Set*(x): void method exists. Referenced objects and collection contents are not inspected.",
        "declare the event as a sealed record (or record struct)")
```

## Related mentions (heuristic)

- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
