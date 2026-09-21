---
type: Rule
id: DCA-TAC-010
title: "Value Object fields must be final (shallow immutability)"
rule: Records have implicitly final fields and enums are immutable by design; a hand-written value class must make every instance field final itself.
constraint: "Value Object fields must be final (shallow immutability)."
selects: "Non-interface, non-record, non-enum classes anywhere under scan assignable to Value."
checks: Every field - inherited ones included - is final or static. A non-final instance field is reported; static fields are not part of the object's state and pass.
enforced_by: "TacticalPatternRules#DCA-TAC-010"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Value Object fields must be final (shallow immutability)

## Selection

Non-interface, non-record, non-enum classes anywhere under scan assignable to Value.

## Check

Every field - inherited ones included - is final or static. A non-final instance field is reported; static fields are not part of the object's state and pass.

## .NET reading

**Selection.** Classes, record classes and structs below the root namespace assignable to IValue; enums excluded.

**Check.** Instance fields, inherited ones included, are readonly; auto-property backing fields are inspected through their get-only or init-only property. Static state, referenced objects and collection contents are not inspected.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-010",
        "Value Object fields must be final (shallow immutability)",
        "Records have implicitly final fields and enums are immutable by design; a hand-written"
            + " value class must make every instance field final itself",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass valueObject :
              concreteClassesAssignableTo(arch, arch.layout().markers().value())) {
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
              "Value Object fields must be final for shallow immutability (Vernon's DDD).",
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
private static List<JavaClass> concreteClassesAssignableTo(DcaArchitecture arch, String marker) {
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-TAC-010",
        "Value Object fields must be readonly (shallow immutability)",
        "Records have implicitly init-only state and enums are immutable by design; a hand-written"
        + " value class must make every instance field readonly and every property get-only or init-only itself",
        arch =>
        {
            var violations = new List<string>();
            foreach (var valueObject in ConcreteTypesAssignableTo(arch, arch.Layout.Markers.Value))
            {
                if (valueObject is Enum)
                {
                    continue;
                }

                foreach (var field in AllMembers(valueObject).OfType<FieldMember>())
                {
                    if (field.IsCompilerGenerated || field.IsStatic == true)
                    {
                        continue;
                    }

                    if (field.Writability != Writability.ReadOnly)
                    {
                        violations.Add($"{valueObject.FullName} has non-readonly field '{field.Name}'");
                    }
                }

                foreach (var property in AllMembers(valueObject).OfType<PropertyMember>())
                {
                    if (property.IsCompilerGenerated || property.IsStatic == true || property.Setter is null)
                    {
                        continue;
                    }

                    if (property.Writability == Writability.Writable)
                    {
                        violations.Add($"{valueObject.FullName} has writable property '{property.Name}'");
                    }
                }
            }

            DcaRule.Fail("Value Object fields must be readonly for shallow immutability (Vernon's DDD).", violations);
        })
        .Selecting("Classes, record classes and structs below the root namespace assignable to IValue; enums excluded.")
    .Checking(
        "Instance fields, inherited ones included, are readonly; auto-property backing fields are inspected through their get-only or init-only property. Static state, referenced objects and collection contents are not inspected." )
```

## Applies to markers

- [Value](/marker/tactical/value.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
