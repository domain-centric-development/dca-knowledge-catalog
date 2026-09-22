---
type: Rule
id: DCA-ERR-006
title: "Diagnostic: incoming adapter packages that drive a use case without translating its failures"
rule: A package that drives the application and knows neither failure type either lets everything escape to a generic handler or catches a generic type and answers every outcome the same way; whether it does is not visible in the import model.
constraint: "Diagnostic: incoming adapter packages that drive a use case without translating its failures."
selects: "Incoming adapter packages of every module root (<module>.adapter.incoming..) that hold at least one non-interface class depending on a class assignable to InputPort - the packages that drive the application."
checks: "Informational diagnostic only: lists a package when no class in it - a central exception handler beside the adapters included - depends on a class assignable to DomainException or UseCaseException, and never fails. A handler in a different package of the same module is not seen, and a caught type is not visible to the import model, so this does not establish that a package translates nothing."
enforced_by: "ErrorHandlingRules#DCA-ERR-006"
status: informational
rule_set: errors
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Diagnostic: incoming adapter packages that drive a use case without translating its failures

## Selection

Incoming adapter packages of every module root (<module>.adapter.incoming..) that hold at least one non-interface class depending on a class assignable to InputPort - the packages that drive the application.

## Check

Informational diagnostic only: lists a package when no class in it - a central exception handler beside the adapters included - depends on a class assignable to DomainException or UseCaseException, and never fails. A handler in a different package of the same module is not seen, and a caught type is not visible to the import model, so this does not establish that a package translates nothing.

## .NET reading

**Selection.** Incoming adapter namespaces of every module root (<Module>.Adapter.Incoming) that hold at least one non-interface type depending on a type assignable to IInputPort - the namespaces that drive the application.

**Check.** Informational diagnostic only: lists a namespace when no type in it - a central exception handler beside the adapters included - depends on a type assignable to DomainException or UseCaseException, and never fails. A handler in a different namespace of the same module is not seen, and a caught type is not visible to the type model, so this does not establish that a namespace translates nothing.

## Implementation

```java
DcaRule.informational(
        "DCA-ERR-006",
        "Diagnostic: incoming adapter packages that drive a use case without translating its"
            + " failures",
        "A package that drives the application and knows neither failure type either lets"
            + " everything escape to a generic handler or catches a generic type and answers"
            + " every outcome the same way; whether it does is not visible in the import model",
        arch -> {
          List<String> observed = new ArrayList<>();
          Map<String, List<JavaClass>> drivingByPackage = new TreeMap<>();
          Set<String> packagesThatName = new HashSet<>();
          for (JavaClass type : arch.classes()) {
            if (!JavaClass.Predicates.resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .test(type)) {
              continue;
            }
            if (dependsOnAssignableTo(type, arch.layout().markers().domainException())
                || dependsOnAssignableTo(type, arch.layout().markers().useCaseException())) {
              packagesThatName.add(type.getPackageName());
            }
            if (!type.isInterface()
                && dependsOnAssignableTo(type, arch.layout().markers().inputPort())) {
              drivingByPackage
                  .computeIfAbsent(type.getPackageName(), pkg -> new ArrayList<>())
                  .add(type);
            }
          }
          drivingByPackage.forEach(
              (pkg, driving) -> {
                if (packagesThatName.contains(pkg)) {
                  return;
                }
                observed.add(
                    pkg
                        + ": drives an input port and names no failure type of the inner layers"
                        + " ("
                        + driving.stream().map(JavaClass::getSimpleName).sorted().toList()
                        + ")");
              });
          return observed;
        })
    .selecting(
        "Incoming adapter packages of every module root (<module>.adapter.incoming..) that hold"
            + " at least one non-interface class depending on a class assignable to InputPort -"
            + " the packages that drive the application.")
    .checking(
        "Informational diagnostic only: lists a package when no class in it - a central"
            + " exception handler beside the adapters included - depends on a class assignable"
            + " to DomainException or UseCaseException, and never fails. A handler in a"
            + " different package of the same module is not seen, and a caught type is not"
            + " visible to the import model, so this does not establish that a package"
            + " translates nothing.")
```

## Helpers

### `dependsOnAssignableTo`

```java
private static boolean dependsOnAssignableTo(JavaClass type, String target) {
  return type.getDirectDependenciesFromSelf().stream()
      .anyMatch(dependency -> dependency.getTargetClass().isAssignableTo(target));
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()`, `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Informational(
    "DCA-ERR-006",
    "Diagnostic: incoming adapter namespaces that drive a use case without translating its failures",
    "A namespace that drives the application and knows neither failure type either lets everything"
        + " escape to a generic handler or catches a generic type and answers every outcome the same"
        + " way; whether it does is not visible in the type model",
    arch =>
    {
        var observed = new List<string>();
        var incoming = new Regex(DcaLayout.AnyOf(arch.AllIncomingAdapterPatterns()));
        var driving = new SortedDictionary<string, List<string>>(StringComparer.Ordinal);
        var namespacesThatName = new HashSet<string>(StringComparer.Ordinal);
        foreach (var type in arch.Types)
        {
            var ns = type.Namespace?.FullName ?? "";
            if (!incoming.IsMatch(ns))
            {
                continue;
            }

            var targets = type.Dependencies.Select(d => d.Target).ToList();
            if (targets.Any(t => IsAssignableTo(t, arch.Layout.Markers.DomainException) || IsAssignableTo(t, arch.Layout.Markers.UseCaseException)))
            {
                namespacesThatName.Add(ns);
            }

            if (type is not Interface && targets.Any(t => IsAssignableTo(t, arch.Layout.Markers.InputPort)))
            {
                if (!driving.TryGetValue(ns, out var names))
                {
                    names = new List<string>();
                    driving[ns] = names;
                }

                names.Add(type.Name);
            }
        }

        foreach (var (ns, names) in driving)
        {
            if (namespacesThatName.Contains(ns))
            {
                continue;
            }

            names.Sort(StringComparer.Ordinal);
            observed.Add(
                $"{ns}: drives an input port and names no failure type of the inner layers ({string.Join(", ", names)})");
        }

        return observed;
    })
    .Selecting(
        "Incoming adapter namespaces of every module root (<Module>.Adapter.Incoming) that hold at "
        + "least one non-interface type depending on a type assignable to IInputPort - the "
        + "namespaces that drive the application.")
    .Checking(
        "Informational diagnostic only: lists a namespace when no type in it - a central exception "
        + "handler beside the adapters included - depends on a type assignable to DomainException or "
        + "UseCaseException, and never fails. A handler in a different namespace of the same module is "
        + "not seen, and a caught type is not visible to the type model, so this does not establish "
        + "that a namespace translates nothing.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [InputPort](/marker/port-in/inputport.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
