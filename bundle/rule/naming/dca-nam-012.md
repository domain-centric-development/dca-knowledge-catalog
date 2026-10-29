---
type: Rule
id: DCA-NAM-012
title: "Diagnostic: use cases and input ports named after a trigger rather than an effect"
rule: "A use case is named after its effect, never after its trigger or its caller. When and by whom it runs is the business of the adapter or the consumer that calls it; the same effect reached from a second trigger is the same use case, and a name that carries the trigger invites a second use case for it."
constraint: "Diagnostic: use cases and input ports named after a trigger rather than an effect."
selects: "Non-nested types in <module>.application.. of every module root that are assignable to the configured input-port role - interfaces and classes - and classes whose simple name ends with the configured use-case suffix."
checks: "Informational diagnostic only: lists a type when its simple name, with the use-case suffix or InputPort removed, contains a trigger word - On, After, When, Upon or Before at the start of the name or after a lower-case letter or digit, followed by an upper-case letter - and never fails. OnboardMember and SignOn are not reported. Whether a name without one of these words names the effect is not decidable here and stays with review."
enforced_by: "NamingRules#DCA-NAM-012"
status: informational
maturity: experimental
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# Diagnostic: use cases and input ports named after a trigger rather than an effect

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Non-nested types in <module>.application.. of every module root that are assignable to the configured input-port role - interfaces and classes - and classes whose simple name ends with the configured use-case suffix.

## Check

Informational diagnostic only: lists a type when its simple name, with the use-case suffix or InputPort removed, contains a trigger word - On, After, When, Upon or Before at the start of the name or after a lower-case letter or digit, followed by an upper-case letter - and never fails. OnboardMember and SignOn are not reported. Whether a name without one of these words names the effect is not decidable here and stays with review.

## .NET reading

**Selection.** Interfaces in <module>.Application of every module root assignable to IInputPort, and concrete application operations selected by IInputPort assignability or the configured use-case suffix. The name is read without the interface's I prefix, the generic arity, and the InputPort and use-case suffixes.

**Check.** Informational diagnostic only: lists a type whose name holds On, After, When, Upon or Before at the start or after a lower-case letter or digit, followed by an upper-case letter, and never fails. A word that only looks like a trigger is listed as well; whether the name describes a trigger stays with review.

## Implementation

```java
DcaRule.informational(
        "DCA-NAM-012",
        "Diagnostic: use cases and input ports named after a trigger rather than an effect",
        "A use case is named after its effect, never after its trigger or its caller. When and"
            + " by whom it runs is the business of the adapter or the consumer that calls it;"
            + " the same effect reached from a second trigger is the same use case, and a name"
            + " that carries the trigger invites a second use case for it",
        arch -> {
          List<String> observed = new ArrayList<>();
          for (JavaClass type : operations(arch, layout)) {
            Matcher trigger = TRIGGER_WORD.matcher(operationName(type, layout));
            if (trigger.find()) {
              observed.add(
                  type.getName()
                      + ": '"
                      + trigger.group(1)
                      + "' names a trigger - name the operation after its effect");
            }
          }
          return observed;
        })
    .experimental()
    .selecting(
        "Non-nested types in <module>.application.. of every module root that are assignable"
            + " to the configured input-port role - interfaces and classes - and classes whose"
            + " simple name ends with the configured use-case suffix.")
    .checking(
        "Informational diagnostic only: lists a type when its simple name, with the use-case"
            + " suffix or InputPort removed, contains a trigger word - On, After, When, Upon or"
            + " Before at the start of the name or after a lower-case letter or digit, followed"
            + " by an upper-case letter - and never fails."
            + " OnboardMember and SignOn are not reported. Whether a name without one of these"
            + " words names the effect is not decidable here and stays with review.")
```

## Helpers

### `operations`

```java
/** The input ports and use cases of every module, nested types left out. */
  private static List<JavaClass> operations(DcaArchitecture arch, DcaLayout layout) {
    List<JavaClass> operations = new ArrayList<>();
    for (JavaClass type : arch.classes()) {
      if (!type.isNestedClass()
          && !type.isAnonymousClass()
          && JavaClass.Predicates.resideInAnyPackage(arch.allApplicationPatterns()).test(type)
          && (type.isAssignableTo(layout.markers().inputPort())
              || (!type.isInterface() && type.getSimpleName().endsWith(layout.useCaseSuffix())))) {
        operations.add(type);
      }
    }
    return operations;
  }
```

### `operationName`

```java
/** The simple name without the use-case suffix, the input-port suffix or {@code InputPort}. */
  private static String operationName(JavaClass type, DcaLayout layout) {
    String name = type.getSimpleName();
    for (String suffix :
        List.of(layout.useCaseSuffix(), layout.inputPortSuffix(), "InputPort").stream()
            .distinct()
            .toList()) {
      if (name.endsWith(suffix) && name.length() > suffix.length()) {
        return name.substring(0, name.length() - suffix.length());
      }
    }
    return name;
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Informational(
    "DCA-NAM-012",
    "Diagnostic: use cases and input ports named after a trigger rather than an effect",
    "A use case is named after its effect, never after its trigger or its caller. When and by whom it"
        + " runs is the business of the adapter or the consumer that calls it; the same effect reached"
        + " from a second trigger is the same use case",
    arch => OperationNames(arch)
        .Select(o => (o.Type, Match: TriggerWord.Match(o.Name)))
        .Where(o => o.Match.Success)
        .Select(o => $"{o.Type} carries the trigger word '{o.Match.Value}' - name it after its effect")
        .Distinct()
        .OrderBy(v => v, StringComparer.Ordinal)
        .ToList())
    .Experimental()
    .Selecting(
        "Interfaces in <module>.Application of every module root assignable to IInputPort, and"
        + " concrete application operations selected by IInputPort assignability or the configured"
        + " use-case suffix. The name is read without the interface's I prefix, the generic arity, and"
        + " the InputPort and use-case suffixes.")
    .Checking(
        "Informational diagnostic only: lists a type whose name holds On, After, When, Upon or Before"
        + " at the start or after a lower-case letter or digit, followed by an upper-case letter,"
        + " and never fails. A word that only looks like a trigger is listed as well; whether the"
        + " name describes a trigger stays with review.")
```

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
