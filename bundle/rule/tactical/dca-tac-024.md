---
type: Rule
id: DCA-TAC-024
title: Value Objects must not declare a neutral factory beside an origin factory with the same parameters
rule: "A value built from input and a value rebuilt from storage are two origins with different checks - validated and derived on the way in, taken as given on the way back - and each has its own named factory. A second factory that takes the same parameters, such as a neutral of(...) beside them, leaves the caller to guess which checks run."
constraint: Value Objects must not declare a neutral factory beside an origin factory with the same parameters.
selects: "Non-interface classes anywhere under scan assignable to Value - records, enums and hand-written classes alike - and their public static methods whose raw return type is the class itself."
checks: "No factory named of takes the same raw parameter types, in the same sequence, as another of these factories. Two named factories with equal parameters (fromInput(String), fromStored(String)) name their origins and pass; factories with different parameters pass, as do constructors, which are not factories by this rule, static methods returning another type, and the valueOf(String) the language declares on an enum. Whether a factory's name says its origin is not checked. An empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-024"
status: enforced
maturity: experimental
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Value Objects must not declare a neutral factory beside an origin factory with the same parameters

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Non-interface classes anywhere under scan assignable to Value - records, enums and hand-written classes alike - and their public static methods whose raw return type is the class itself.

## Check

No factory named of takes the same raw parameter types, in the same sequence, as another of these factories. Two named factories with equal parameters (fromInput(String), fromStored(String)) name their origins and pass; factories with different parameters pass, as do constructors, which are not factories by this rule, static methods returning another type, and the valueOf(String) the language declares on an enum. Whether a factory's name says its origin is not checked. An empty selection passes.

## .NET reading

**Selection.** Concrete classes, records and structs below the root namespace assignable to IValue, with their runtime type in the loaded assemblies.

**Check.** No public static method named Of, declared by the type itself and returning exactly that type, sits beside another such method that takes the same parameter types in the same sequence. Two named factories with equal parameters (FromInput, FromStored) pass, and so does an Of that is the only factory for its parameters. Operators, generic methods, inherited methods and factories that return a wrapper (a nullable struct, a task, a result type) are not counted - a nullable reference return is the type itself and counts; constructors are not factories in this sense. An empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-TAC-024",
        "Value Objects must not declare a neutral factory beside an origin factory with the same parameters",
        "A value built from input and a value rebuilt from storage are two origins with"
            + " different checks - validated and derived on the way in, taken as given on the"
            + " way back - and each has its own named factory. A second factory that takes the"
            + " same parameters, such as a neutral of(...) beside them, leaves the caller to"
            + " guess which checks run",
        arch -> {
          List<String> violations = new ArrayList<>();
          for (JavaClass value :
              concreteClassesAssignableTo(arch, arch.layout().markers().is("value"))) {
            java.util.Map<List<String>, List<String>> bySignature =
                new java.util.LinkedHashMap<>();
            for (JavaMethod method : value.getMethods()) {
              Set<JavaModifier> modifiers = method.getModifiers();
              if (modifiers.contains(JavaModifier.PUBLIC)
                  && modifiers.contains(JavaModifier.STATIC)
                  && !modifiers.contains(JavaModifier.SYNTHETIC)
                  && method.getRawReturnType().equals(value)
                  && !isEnumValueOf(value, method)) {
                List<String> signature =
                    method.getRawParameterTypes().stream().map(JavaClass::getName).toList();
                bySignature
                    .computeIfAbsent(signature, key -> new ArrayList<>())
                    .add(method.getName());
              }
            }
            bySignature.forEach(
                (signature, factories) -> {
                  if (factories.size() > 1 && factories.contains("of")) {
                    violations.add(
                        value.getName()
                            + " has "
                            + factories.size()
                            + " factories taking ("
                            + String.join(", ", signature)
                            + "): "
                            + String.join(", ", factories.stream().sorted().toList()));
                  }
                });
          }
          fail(
              "Value Objects must not declare a neutral factory beside an origin factory with the same parameters. Fix: remove the neutral of(...) and"
                  + " keep one named factory for each origin - from input, from storage.",
              violations);
        })
    .experimental()
    .selecting(
        "Non-interface classes anywhere under scan assignable to Value - records, enums and"
            + " hand-written classes alike - and their public static methods whose raw return"
            + " type is the class itself.")
    .checking(
        "No factory named of takes the same raw parameter types, in the same sequence, as"
            + " another of these factories. Two named factories with equal parameters"
            + " (fromInput(String), fromStored(String)) name their origins and pass; factories"
            + " with different parameters pass, as do constructors, which are not"
            + " factories by this rule, static methods returning another type, and the"
            + " valueOf(String) the language declares on an enum. Whether a"
            + " factory's name says its origin is not checked. An empty selection passes.",
        "remove the neutral of(...) and keep one named factory for each origin - from input,"
            + " from storage")
```

## Helpers

### `concreteClassesAssignableTo`

```java
private static List<JavaClass> concreteClassesAssignableTo(
    DcaArchitecture arch, DescribedPredicate<JavaClass> role) {
  return classesMatching(arch, c -> role.test(c) && !c.isInterface());
}
```

### `isEnumValueOf`

```java
/**
   * The {@code valueOf(String)} the language declares on every enum - not a factory of the model.
   */
  private static boolean isEnumValueOf(JavaClass type, JavaMethod method) {
    return type.isEnum()
        && method.getName().equals("valueOf")
        && method.getRawParameterTypes().size() == 1
        && method.getRawParameterTypes().get(0).getName().equals("java.lang.String");
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
    "DCA-TAC-024",
    "Value Objects must not declare a neutral factory beside an origin factory with the same parameters",
    "A value built from input and a value rebuilt from storage are two origins with different checks,"
        + " and each has its own named factory. A neutral factory beside them that takes the same"
        + " parameters leaves the caller to guess which checks run; a value with one origin keeps its"
        + " one factory",
    arch =>
    {
        var violations = new List<string>();
        foreach (var value in ConcreteTypesAssignableTo(arch, nameof(DcaMarkers.Value))
            .Where(t => ResidesInAny(t, DcaLayout.Below(arch.Layout.RootNamespace)))
            .OrderBy(t => t.FullName, StringComparer.Ordinal))
        {
            var runtime = arch.RuntimeType(value);
            if (runtime is null || runtime.IsAbstract)
            {
                continue;
            }

            var factories = runtime
                .GetMethods(BindingFlags.Public | BindingFlags.Static | BindingFlags.DeclaredOnly)
                .Where(m => !m.IsSpecialName && !m.IsGenericMethodDefinition && m.ReturnType == runtime)
                .ToList();
            foreach (var neutral in factories.Where(m => m.Name == NeutralFactoryName))
            {
                var signature = Signature(neutral);
                var beside = factories
                    .Where(m => m.Name != NeutralFactoryName && Signature(m) == signature)
                    .Select(m => m.Name)
                    .OrderBy(n => n, StringComparer.Ordinal)
                    .ToList();
                if (beside.Count > 0)
                {
                    violations.Add($"{value.FullName} declares the neutral factory {NeutralFactoryName}({signature})"
                        + $" beside {string.Join(", ", beside)} with the same parameters");
                }
            }
        }

        DcaRule.Fail(
            "Value Objects must not declare a neutral factory beside an origin factory with the same parameters",
            violations,
            "remove the neutral factory and let each caller name the origin - the factory that validates input or the one that takes a stored value as given");
    })
    .Experimental()
    .Selecting(
        "Concrete classes, records and structs below the root namespace assignable to IValue, with"
        + " their runtime type in the loaded assemblies.")
    .Checking(
        "No public static method named Of, declared by the type itself and returning exactly that"
        + " type, sits beside another such method that takes the same parameter types in the same"
        + " sequence. Two named factories with equal parameters (FromInput, FromStored) pass, and so"
        + " does an Of that is the only factory for its parameters. Operators, generic methods,"
        + " inherited methods and factories that return a wrapper (a nullable struct, a task, a"
        + " result type) are not counted - a nullable reference return is the type itself and"
        + " counts; constructors are not factories in this sense. An empty selection passes.")
```

## Related mentions (heuristic)

- [Value](/marker/tactical/value.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
