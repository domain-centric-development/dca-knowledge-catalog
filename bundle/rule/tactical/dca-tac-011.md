---
type: Rule
id: DCA-TAC-011
title: Value Objects must not have setter methods
rule: Value Objects are immutable; state changes produce a new instance instead of mutating.
constraint: Value Objects must not have setter methods.
selects: Non-interface classes anywhere under scan assignable to Value - records and enums included.
checks: "No method - inherited ones included - is a setter: a name starting with set followed by an upper-case letter, exactly one parameter and return type void, regardless of visibility. A wither that returns a new instance is not a setter."
enforced_by: "TacticalPatternRules#DCA-TAC-011"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Value Objects must not have setter methods

## Selection

Non-interface classes anywhere under scan assignable to Value - records and enums included.

## Check

No method - inherited ones included - is a setter: a name starting with set followed by an upper-case letter, exactly one parameter and return type void, regardless of visibility. A wither that returns a new instance is not a setter.

## .NET reading

**Selection.** Non-interface types below the root namespace assignable to IValue - records, structs and enums included.

**Check.** No member - inherited ones included - is a setter, regardless of visibility: a property with a writable (non-init) set accessor, or a method named Set followed by an upper-case letter with exactly one parameter and return type void. A wither that returns a new instance is not a setter; a record's init-only properties pass.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-011",
        "Value Objects must not have setter methods",
        "Value Objects are immutable; state changes produce a new instance instead of mutating",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass valueObject : concreteClassesAssignableTo(arch, Value.class)) {
            for (JavaMethod method : valueObject.getAllMethods()) {
              if (isSetter(method)) {
                violations.add(
                    valueObject.getName() + " has setter method '" + method.getName() + "'");
              }
            }
          }
          fail(
              "Value Objects must be immutable and should not have setter methods.",
              violations);
        })
    .selecting(
        "Non-interface classes anywhere under scan assignable to Value - records and "
            + "enums included.")
    .checking(
        "No method - inherited ones included - is a setter: a name starting with set "
            + "followed by an upper-case letter, exactly one parameter and return type void, "
            + "regardless of visibility. A wither that returns a new instance is not a "
            + "setter.")
```

## Helpers

### `concreteClassesAssignableTo`

```java
private static List<JavaClass> concreteClassesAssignableTo(
    DcaArchitecture arch, Class<?> marker) {
  return classesMatching(arch, c -> c.isAssignableTo(marker) && !c.isInterface());
}
```

### `isSetter`

```java
private static boolean isSetter(JavaMethod method) {
  String name = method.getName();
  return name.startsWith("set")
      && name.length() > 3
      && Character.isUpperCase(name.charAt(3))
      && method.getRawParameterTypes().size() == 1
      && method.getRawReturnType().getName().equals("void");
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
    "DCA-TAC-011",
    "Value Objects must not have setter methods",
    "Value Objects are immutable; state changes produce a new instance instead of mutating",
    arch =>
    {
        var violations = new List<string>();
        foreach (var valueObject in ConcreteTypesAssignableTo(arch, typeof(IValue)))
        {
            foreach (var setter in Setters(valueObject, publicOnly: false))
            {
                violations.Add($"{valueObject.FullName} has setter '{setter}'");
            }
        }

        DcaRule.Fail("Value Objects must be immutable and should not have setter methods.", violations);
    })
    .Selecting(
        "Non-interface types below the root namespace assignable to IValue - records, "
        + "structs and enums included.")
    .Checking(
        "No member - inherited ones included - is a setter, regardless of visibility: "
        + "a property with a writable (non-init) set accessor, or a method named Set "
        + "followed by an upper-case letter with exactly one parameter and return type "
        + "void. A wither that returns a new instance is not a setter; a record's "
        + "init-only properties pass.")
```

## Applies to markers

- [Value](/marker/tactical/value.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
