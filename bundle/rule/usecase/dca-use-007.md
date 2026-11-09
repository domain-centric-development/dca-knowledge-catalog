---
type: Rule
id: DCA-USE-007
title: "Use Case Result Models should be immutable (final or records)"
rule: "Use case result models should be immutable (value objects)."
constraint: "Use Case Result Models should be immutable (final or records)."
selects: "Non-interface, non-enum classes, including records, in <module>.application.. whose simple name ends with Result."
checks: "The type is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter). Referenced objects and collection contents are not inspected."
enforced_by: "UseCaseRules#DCA-USE-007"
status: enforced
maturity: released
rule_set: usecase
implementations: [java, dotnet, rust]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use Case Result Models should be immutable (final or records)

## Selection

Non-interface, non-enum classes, including records, in <module>.application.. whose simple name ends with Result.

## Check

The type is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter). Referenced objects and collection contents are not inspected.

## .NET reading

**Selection.** Classes and structs in each module application namespace with the corresponding Command, Query or Result suffix, including record classes and record structs.

**Check.** Classes are sealed or records; structs are allowed. Every inherited instance field is readonly, every property is get-only or init-only and no instance Set*(x): void method exists. Referenced objects and collection contents are not inspected.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a test, reformulated for Rust (source-test).

**Selection.** Structs in application crates whose name ends with Result.

**Check.** No method takes &mut self and no field type is an interior-mutability type.

## Implementation

```java
DcaRule.of(
        "DCA-USE-007",
        "Use Case Result Models should be immutable (final or records)",
        "Use case result models should be immutable (value objects)",
        arch ->
            immutableApplicationModels(
                arch, JavaClass.Predicates.simpleNameEndingWith("Result")))
    .selecting(
        "Non-interface, non-enum classes, including records, in <module>.application.. whose simple name ends with Result.")
    .checking(
        "The type is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter). Referenced objects and collection contents are not inspected.")
```

## Helpers

### `immutableApplicationModels`

```java
private static com.tngtech.archunit.lang.ArchRule immutableApplicationModels(
    DcaArchitecture arch, DescribedPredicate<JavaClass> model) {
  // An enum is immutable by construction; on recent platforms its inherited state carries a
  // non-final cache field, which the shape check would report.
  return classes()
      .that(model)
      .and(arch.inApplication())
      .and()
      .areNotInterfaces()
      .and()
      .areNotEnums()
      .should(TypeInspection.haveImmutableShape())
      .allowEmptyShould(true);
}
```

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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-007",
        "Use Case Result Models should be immutable (sealed or records)",
        "Use case result models should be immutable (value objects)",
        arch => ImmutableApplicationModels(arch, "Result", t => t.Name.EndsWith("Result", StringComparison.Ordinal)))
    .Selecting("Classes and structs in each module application namespace with the corresponding Command, Query or Result suffix, including record classes and record structs.")
    .Checking(
        "Classes are sealed or records; structs are allowed. Every inherited instance field is readonly, every property is get-only or init-only and no instance Set*(x): void method exists. Referenced objects and collection contents are not inspected.",
        "declare *Result types with immutable instance state")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
