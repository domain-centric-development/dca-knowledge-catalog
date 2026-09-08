---
type: Rule
id: DCA-TAC-010
title: "Value Object fields must be final (deep immutability)"
rule: Records have implicitly final fields and enums are immutable by design; a hand-written value class must make every instance field final itself.
constraint: "Value Object fields must be final (deep immutability)."
selects: "Non-interface, non-record, non-enum classes anywhere under scan assignable to Value."
checks: Every field - inherited ones included - is final or static. A non-final instance field is reported; static fields are not part of the object's state and pass.
enforced_by: "TacticalPatternRules#DCA-TAC-010"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Non-interface, non-record, non-enum classes anywhere under scan assignable to Value.

## Check

Every field - inherited ones included - is final or static. A non-final instance field is reported; static fields are not part of the object's state and pass.

## .NET reading

**Selection.** Non-interface types below the root namespace assignable to IValue that are neither record classes, structs nor enums.

**Check.** Every non-static instance field - inherited ones included, compiler-generated ones skipped - is readonly, and every property that has a set accessor is init-only rather than writable. A get-only property passes; static fields are not part of the object's state and pass.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-010",
        "Value Object fields must be final (deep immutability)",
        "Records have implicitly final fields and enums are immutable by design; a hand-written"
            + " value class must make every instance field final itself",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass valueObject : concreteClassesAssignableTo(arch, Value.class)) {
            if (valueObject.isRecord() || valueObject.isEnum()) {
              continue;
            }
            for (JavaField field : valueObject.getAllFields()) {
              Set<JavaModifier> modifiers = field.getModifiers();
              if (!modifiers.contains(JavaModifier.FINAL)
                  && !modifiers.contains(JavaModifier.STATIC)) {
                violations.add(
                    valueObject.getName() + " has non-final field '" + field.getName() + "'");
              }
            }
          }
          fail(
              "Value Object fields must be final for deep immutability (Vernon's DDD).",
              violations);
        })
    .selecting(
        "Non-interface, non-record, non-enum classes anywhere under scan assignable to "
            + "Value.")
    .checking(
        "Every field - inherited ones included - is final or static. A non-final "
            + "instance field is reported; static fields are not part of the object's state "
            + "and pass.")
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

- [Value](/marker/tactical/value.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
