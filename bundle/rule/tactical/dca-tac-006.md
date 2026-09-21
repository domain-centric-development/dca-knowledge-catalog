---
type: Rule
id: DCA-TAC-006
title: Domain model classes must not have public setter methods
rule: "Behavior-rich domain models change state through intention-revealing methods from the ubiquitous language, never through public setters."
constraint: Domain model classes must not have public setter methods.
selects: Non-interface classes anywhere under scan assignable to Entity - aggregate roots included.
checks: "No method - inherited ones included - is a public setter: a name starting with set followed by an upper-case letter, exactly one parameter and return type void. A non-public setter, a fluent setter returning the instance, or a set-prefixed method with zero or two parameters does not count."
enforced_by: "TacticalPatternRules#DCA-TAC-006"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Domain model classes must not have public setter methods

## Selection

Non-interface classes anywhere under scan assignable to Entity - aggregate roots included.

## Check

No method - inherited ones included - is a public setter: a name starting with set followed by an upper-case letter, exactly one parameter and return type void. A non-public setter, a fluent setter returning the instance, or a set-prefixed method with zero or two parameters does not count.

## .NET reading

**Selection.** Non-interface types below the root namespace assignable to IEntity - aggregate roots included.

**Check.** No member - inherited ones included - is a public setter: a property with a public, writable set accessor (an init accessor does not count), or a public method named Set followed by an upper-case letter with exactly one parameter and return type void. A non-public setter, a fluent setter returning the instance, or a Set-prefixed method with zero or two parameters does not count.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-006",
        "Domain model classes must not have public setter methods",
        "Behavior-rich domain models change state through intention-revealing methods from the"
            + " ubiquitous language, never through public setters",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass domainClass :
              concreteClassesAssignableTo(arch, arch.layout().markers().entity())) {
            for (JavaMethod method : domainClass.getAllMethods()) {
              if (isSetter(method) && method.getModifiers().contains(JavaModifier.PUBLIC)) {
                violations.add(
                    domainClass.getName() + " has public setter '" + method.getName() + "'");
              }
            }
          }
          fail(
              "Domain model classes must not expose public setters - use intention-revealing"
                  + " methods from the ubiquitous language.",
              violations);
        })
    .selecting(
        "Non-interface classes anywhere under scan assignable to Entity - aggregate "
            + "roots included.")
    .checking(
        "No method - inherited ones included - is a public setter: a name starting with "
            + "set followed by an upper-case letter, exactly one parameter and return type "
            + "void. A non-public setter, a fluent setter returning the instance, or a "
            + "set-prefixed method with zero or two parameters does not count.")
```

## Helpers

### `concreteClassesAssignableTo`

```java
private static List<JavaClass> concreteClassesAssignableTo(DcaArchitecture arch, String marker) {
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-006",
    "Domain model classes must not have public setter methods",
    "Behavior-rich domain models change state through intention-revealing methods from the"
    + " ubiquitous language, never through public property setters",
    arch =>
    {
        var violations = new List<string>();
        foreach (var domainClass in ConcreteTypesAssignableTo(arch, arch.Layout.Markers.Entity))
        {
            foreach (var setter in Setters(domainClass, publicOnly: true))
            {
                violations.Add($"{domainClass.FullName} has public setter '{setter}'");
            }
        }

        DcaRule.Fail(
            "Domain model classes must not expose public setters - use intention-revealing methods from the ubiquitous language.",
            violations);
    })
    .Selecting(
        "Non-interface types below the root namespace assignable to IEntity - "
        + "aggregate roots included.")
    .Checking(
        "No member - inherited ones included - is a public setter: a property with a "
        + "public, writable set accessor (an init accessor does not count), or a public "
        + "method named Set followed by an upper-case letter with exactly one parameter "
        + "and return type void. A non-public setter, a fluent setter returning the "
        + "instance, or a Set-prefixed method with zero or two parameters does not "
        + "count.")
```

## Related mentions (heuristic)

- [Entity<T, ID>](/marker/tactical/entity.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
