---
type: Rule
id: DCA-TAC-012
title: Value Objects must be records or immutable classes with attribute equality
rule: A record grants attribute-based equality for free; a hand-written Value Object class must override equals and hashCode itself to compare by its attributes.
constraint: Value Objects must be records or immutable classes with attribute equality.
selects: "Non-interface, non-record, non-enum classes anywhere under scan assignable to Value."
checks: "The class, or a superclass other than Object, overrides both boolean equals(Object) and int hashCode() with exactly those signatures. An overload such as equals(Money) does not count, and overriding only one of the two is reported."
enforced_by: "TacticalPatternRules#DCA-TAC-012"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Value Objects must be records or immutable classes with attribute equality

## Selection

Non-interface, non-record, non-enum classes anywhere under scan assignable to Value.

## Check

The class, or a superclass other than Object, overrides both boolean equals(Object) and int hashCode() with exactly those signatures. An overload such as equals(Money) does not count, and overriding only one of the two is reported.

## .NET reading

**Selection.** Non-interface types below the root namespace assignable to IValue; enums excluded.

**Check.** The runtime type or a base other than object or ValueType overrides Equals(object) and GetHashCode(). Record-generated equality counts; plain structs must supply both overrides.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-012",
        "Value Objects must be records or immutable classes with attribute equality",
        "A record grants attribute-based equality for free; a hand-written Value Object class must"
            + " override equals and hashCode itself to compare by its attributes",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass valueObject : concreteClassesAssignableTo(arch, Value.class)) {
            if (valueObject.isRecord() || valueObject.isEnum()) {
              continue;
            }
            if (!TypeInspection.declaresAttributeEquality(valueObject)) {
              violations.add(
                  valueObject.getName()
                      + " is a non-record Value Object without its own equals(Object)/hashCode()");
            }
          }
          fail(
              "Value Objects are records by preference; an immutable class is allowed, but it must"
                  + " implement attribute equality itself.",
              violations);
        })
    .selecting(
        "Non-interface, non-record, non-enum classes anywhere under scan assignable to "
            + "Value.")
    .checking(
        "The class, or a superclass other than Object, overrides both boolean "
            + "equals(Object) and int hashCode() with exactly those signatures. An overload "
            + "such as equals(Money) does not count, and overriding only one of the two is "
            + "reported.")
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

### `TypeInspection.declaresAttributeEquality`

```java
/**
   * Whether the class overrides both {@code boolean equals(Object)} and {@code int hashCode()} —
   * exactly those signatures. An overload such as {@code equals(Money)} does not count: the class
   * still compares by identity through the inherited {@code Object.equals(Object)}.
   */
  static boolean declaresAttributeEquality(JavaClass type) {
    return overrides(type, "equals", "boolean", OBJECT) && overrides(type, "hashCode", "int");
  }
```

### `classesMatching`

```java
private static List<JavaClass> classesMatching(
    DcaArchitecture arch, Predicate<JavaClass> filter) {
  return arch.classes().stream().filter(filter).collect(Collectors.toList());
}
```

### `TypeInspection.overrides`

```java
private static boolean overrides(
    JavaClass type, String name, String returnType, String... parameterTypes) {
  return type.getAllMethods().stream()
      .anyMatch(m -> isOverride(m, name, returnType, parameterTypes));
}
```

### `TypeInspection.isOverride`

```java
private static boolean isOverride(
    JavaMethod method, String name, String returnType, String... parameterTypes) {
  if (!method.getName().equals(name)
      || method.getOwner().getName().equals(OBJECT)
      || method.getModifiers().contains(JavaModifier.STATIC)
      || !method.getRawReturnType().getName().equals(returnType)) {
    return false;
  }
  List<String> actual = method.getRawParameterTypes().stream().map(JavaClass::getName).toList();
  return actual.equals(List.of(parameterTypes));
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-TAC-012",
        "Value Objects must be records or immutable classes with attribute equality",
        "A record grants attribute-based equality for free; a hand-written Value Object class must"
        + " override Equals and GetHashCode itself to compare by its attributes",
        arch =>
        {
            var violations = new List<string>();
            foreach (var valueObject in ConcreteTypesAssignableTo(arch, typeof(IValue)))
            {
                if (IsRecord(valueObject) || valueObject is Enum)
                {
                    continue;
                }

                var runtime = arch.RuntimeType(valueObject);
                var overridesEquality = runtime is not null
                    && OverridesOwn(runtime, nameof(Equals), typeof(object))
                    && OverridesOwn(runtime, nameof(GetHashCode));
                if (!overridesEquality)
                {
                    violations.Add($"{valueObject.FullName} is a non-record Value Object without its own Equals/GetHashCode");
                }
            }

            DcaRule.Fail(
                "Value Objects are records by preference; an immutable class is allowed, but it must implement attribute equality itself.",
                violations);
        })
        .Selecting("Non-interface types below the root namespace assignable to IValue; enums excluded.")
    .Checking(
        "The runtime type or a base other than object or ValueType overrides Equals(object) and GetHashCode(). Record-generated equality counts; plain structs must supply both overrides." )
```

## Related mentions (heuristic)

- [Value](/marker/tactical/value.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
