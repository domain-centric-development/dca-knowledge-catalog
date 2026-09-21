---
type: Rule
id: DCA-HEX-012
title: Incoming Adapters must not depend on domain services
rule: "An incoming adapter translates external input, calls an input port and formats its result. Injecting or invoking a domain service bypasses the application boundary; the use case owns that collaboration and puts its outcome into the result. Outgoing adapters are outside this rule - repositories and other driven adapters may construct or reconstitute domain objects while implementing output ports."
constraint: Incoming Adapters must not depend on domain services.
selects: "Classes in <module>.adapter.incoming.. of every module root, event consumers included. Outgoing adapters are not selected."
checks: "No dependency on a class assignable to DomainService - the building-block marker interface, any sub-interface of it and every class implementing one. A domain class without the marker is not a domain service by this rule. Injecting it, calling it or naming it in a signature all count as a dependency. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-012"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Incoming Adapters must not depend on domain services

## Selection

Classes in <module>.adapter.incoming.. of every module root, event consumers included. Outgoing adapters are not selected.

## Check

No dependency on a class assignable to DomainService - the building-block marker interface, any sub-interface of it and every class implementing one. A domain class without the marker is not a domain service by this rule. Injecting it, calling it or naming it in a signature all count as a dependency. An empty selection passes.

## .NET reading

**Selection.** Classes in <module>.Adapter.Incoming of every module root, event consumers included. Outgoing adapters are not selected.

**Check.** No dependency on a type assignable to IDomainService - the building-block marker interface, any sub-interface of it and every class implementing one. A domain class without the marker is not a domain service by this rule. Injecting it, calling it or naming it in a signature all count as a dependency; constructor parameters are read from the runtime type as well, so a service injected into an adapter whose members are all async is still found. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-012",
        "Incoming Adapters must not depend on domain services",
        "An incoming adapter translates external input, calls an input port and formats its result."
            + " Injecting or invoking a domain service bypasses the application boundary; the use"
            + " case owns that collaboration and puts its outcome into the result. Outgoing adapters"
            + " are outside this rule - repositories and other driven adapters may construct or"
            + " reconstitute domain objects while implementing output ports",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .should()
                .dependOnClassesThat()
                .areAssignableTo(arch.layout().markers().domainService())
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.adapter.incoming.. of every module root, event consumers"
            + " included. Outgoing adapters are not selected.")
    .checking(
        "No dependency on a class assignable to DomainService - the building-block marker"
            + " interface, any sub-interface of it and every class implementing one. A domain"
            + " class without the marker is not a domain service by this rule. Injecting it,"
            + " calling it or naming it in a signature all count as a dependency. An empty"
            + " selection passes.",
        "move the collaboration into the use case and carry its outcome in the result")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-HEX-012",
        "Incoming Adapters must not depend on domain services",
        "An incoming adapter translates external input, calls an input port and formats its result."
            + " Injecting or invoking a domain service bypasses the application boundary; the use case owns"
            + " that collaboration and puts its outcome into the result. Outgoing adapters are outside this"
            + " rule - repositories and other driven adapters may construct or reconstitute domain objects"
            + " while implementing output ports",
        arch =>
        {
            var incoming = DcaLayout.AnyOf(arch.AllIncomingAdapterPatterns());
            var violations = new List<string>();
            foreach (var adapter in arch.Classes.Where(c => InNamespace(c, incoming)))
            {
                var services = adapter.Dependencies
                    .Select(d => d.Target)
                    .Where(t => !t.IsGenericParameter && IsAssignableTo(arch, t, arch.Layout.Markers.DomainService))
                    .Select(t => t.FullName);
                var runtime = arch.RuntimeType(adapter);
                if (runtime is not null)
                {
                    services = services.Concat(runtime
                        .GetConstructors(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)
                        .SelectMany(c => c.GetParameters())
                        .Select(p => p.ParameterType)
                        .Where(t => DcaMarkers.IsAssignableToByName(t, arch.Layout.Markers.DomainService))
                        .Select(t => t.FullName!));
                }

                violations.AddRange(services.Distinct()
                    .Select(s => $"{adapter.FullName} depends on the domain service {s}"));
            }

            DcaRule.Fail(
                "Incoming Adapters must not depend on domain services",
                violations.Distinct().OrderBy(v => v, StringComparer.Ordinal).ToList(),
                "move the collaboration into the use case and carry its outcome in the result");
        })
    .Selecting(
        "Classes in <module>.Adapter.Incoming of every module root, event consumers"
            + " included. Outgoing adapters are not selected.")
    .Checking(
        "No dependency on a type assignable to IDomainService - the building-block marker"
            + " interface, any sub-interface of it and every class implementing one. A domain"
            + " class without the marker is not a domain service by this rule. Injecting it,"
            + " calling it or naming it in a signature all count as a dependency; constructor"
            + " parameters are read from the runtime type as well, so a service injected into an"
            + " adapter whose members are all async is still found. An empty selection passes.")
```

## Related mentions (heuristic)

- [DomainService](/marker/tactical/domainservice.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
