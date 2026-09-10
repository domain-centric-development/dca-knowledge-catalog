---
type: Rule
id: DCA-USE-004
title: "Use Case Commands should be immutable (final or records)"
rule: "Use case commands should be immutable (value objects)."
constraint: "Use Case Commands should be immutable (final or records)."
selects: "Non-interface classes, including records, in <module>.application.. whose simple name ends with Command."
checks: "The type is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter). Referenced objects and collection contents are not inspected."
enforced_by: "UseCaseRules#DCA-USE-004"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use Case Commands should be immutable (final or records)

## Selection

Non-interface classes, including records, in <module>.application.. whose simple name ends with Command.

## Check

The type is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter). Referenced objects and collection contents are not inspected.

## .NET reading

**Selection.** Classes and structs in each module application namespace with the corresponding Command, Query or Result suffix, including record classes and record structs.

**Check.** Classes are sealed or records; structs are allowed. Every inherited instance field is readonly, every property is get-only or init-only and no instance Set*(x): void method exists. Referenced objects and collection contents are not inspected.

## Implementation

```java
DcaRule.of(
        "DCA-USE-004",
        "Use Case Commands should be immutable (final or records)",
        "Use case commands should be immutable (value objects)",
        arch -> immutableApplicationModels(arch, "Command"))
    .selecting(
        "Non-interface classes, including records, in <module>.application.. whose simple name ends with Command.")
    .checking(
        "The type is final or a record with final inherited instance fields and no instance setter methods - a name heuristic: set followed by an upper-case letter, with parameters, returning void (settle(x) is not a setter). Referenced objects and collection contents are not inspected.")
```

## Helpers

### `immutableApplicationModels`

```java
private static com.tngtech.archunit.lang.ArchRule immutableApplicationModels(
    DcaArchitecture arch, String suffix) {
  return classes()
      .that()
      .haveSimpleNameEndingWith(suffix)
      .and()
      .resideInAnyPackage(arch.allApplicationPatterns())
      .and()
      .areNotInterfaces()
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-USE-004",
        "Use Case Commands should be immutable (sealed or records)",
        "Use case commands should be immutable (value objects)",
        arch => ImmutableApplicationModels(arch, "Command"))
    .Selecting("Classes and structs in each module application namespace with the corresponding Command, Query or Result suffix, including record classes and record structs.")
    .Checking(
        "Classes are sealed or records; structs are allowed. Every inherited instance field is readonly, every property is get-only or init-only and no instance Set*(x): void method exists. Referenced objects and collection contents are not inspected." )
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
