---
type: Rule
id: DCA-ERR-006
title: "Diagnostic: incoming adapters that drive a use case without translating its failures"
rule: An adapter that knows neither failure type either lets everything escape to a generic handler or catches a generic type and answers every outcome the same way; whether it does is not visible in the import model.
constraint: "Diagnostic: incoming adapters that drive a use case without translating its failures."
selects: "Non-interface classes in <module>.adapter.incoming.. of every module root that depend on a class assignable to InputPort - the adapters that drive the application."
checks: "Informational diagnostic only: lists those that depend on no class assignable to DomainException or UseCaseException and never fails. A central handler elsewhere in the adapter layer is a valid answer, and a caught type is not visible to the import model - this does not establish that an adapter translates nothing."
enforced_by: "ErrorHandlingRules#DCA-ERR-006"
status: informational
rule_set: errors
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Diagnostic: incoming adapters that drive a use case without translating its failures

## Selection

Non-interface classes in <module>.adapter.incoming.. of every module root that depend on a class assignable to InputPort - the adapters that drive the application.

## Check

Informational diagnostic only: lists those that depend on no class assignable to DomainException or UseCaseException and never fails. A central handler elsewhere in the adapter layer is a valid answer, and a caught type is not visible to the import model - this does not establish that an adapter translates nothing.

## .NET reading

**Selection.** Non-interface types under <Module>.Adapter.Incoming of every module root that depend on a type assignable to IInputPort - the adapters that drive the application.

**Check.** Informational diagnostic only: lists those that depend on no type assignable to DomainException or UseCaseException and never fails. A central handler elsewhere in the adapter layer is a valid answer, and a caught type is not visible to the type model - this does not establish that an adapter translates nothing.

## Implementation

```java
DcaRule.informational(
        "DCA-ERR-006",
        "Diagnostic: incoming adapters that drive a use case without translating its failures",
        "An adapter that knows neither failure type either lets everything escape to a generic"
            + " handler or catches a generic type and answers every outcome the same way;"
            + " whether it does is not visible in the import model",
        arch -> {
          for (JavaClass type : arch.classes()) {
            if (type.isInterface()
                || !JavaClass.Predicates.resideInAnyPackage(arch.allIncomingAdapterPatterns())
                    .test(type)
                || !dependsOnAssignableTo(type, InputPort.class)
                || dependsOnAssignableTo(type, DomainException.class)
                || dependsOnAssignableTo(type, UseCaseException.class)) {
              continue;
            }
            System.out.println(
                "[DCA-ERR-006] "
                    + type.getName()
                    + ": drives an input port and names no failure type of the inner layers");
          }
        })
    .selecting(
        "Non-interface classes in <module>.adapter.incoming.. of every module root that depend"
            + " on a class assignable to InputPort - the adapters that drive the application.")
    .checking(
        "Informational diagnostic only: lists those that depend on no class assignable to"
            + " DomainException or UseCaseException and never fails. A central handler"
            + " elsewhere in the adapter layer is a valid answer, and a caught type is not"
            + " visible to the import model - this does not establish that an adapter"
            + " translates nothing.")
```

## Helpers

### `dependsOnAssignableTo`

```java
private static boolean dependsOnAssignableTo(JavaClass type, Class<?> target) {
  return type.getDirectDependenciesFromSelf().stream()
      .anyMatch(dependency -> dependency.getTargetClass().isAssignableTo(target));
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()`, `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Informational(
    "DCA-ERR-006",
    "Diagnostic: incoming adapters that drive a use case without translating its failures",
    "An adapter that knows neither failure type either lets everything escape to a generic handler"
        + " or catches a generic type and answers every outcome the same way; whether it does is not"
        + " visible in the type model",
    arch =>
    {
        var incoming = new Regex(DcaLayout.AnyOf(arch.AllIncomingAdapterPatterns()));
        foreach (var type in arch.Types.Where(t => t is not Interface))
        {
            if (!incoming.IsMatch(type.Namespace?.FullName ?? ""))
            {
                continue;
            }

            var targets = type.Dependencies.Select(d => d.Target).ToList();
            if (!targets.Any(t => IsAssignableTo(t, typeof(IInputPort)))
                || targets.Any(t => IsAssignableTo(t, typeof(DomainException)) || IsAssignableTo(t, typeof(UseCaseException))))
            {
                continue;
            }

            Console.WriteLine(
                $"[DCA-ERR-006] {type.FullName}: drives an input port and names no failure type of the inner layers");
        }
    })
    .Selecting(
        "Non-interface types under <Module>.Adapter.Incoming of every module root that depend on a "
        + "type assignable to IInputPort - the adapters that drive the application.")
    .Checking(
        "Informational diagnostic only: lists those that depend on no type assignable to "
        + "DomainException or UseCaseException and never fails. A central handler elsewhere in the "
        + "adapter layer is a valid answer, and a caught type is not visible to the type model - "
        + "this does not establish that an adapter translates nothing.")
```

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [InputPort](/marker/port-in/inputport.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
