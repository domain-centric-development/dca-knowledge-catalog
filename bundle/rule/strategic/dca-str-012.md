---
type: Rule
id: DCA-STR-012
title: At least one module owns a DCA layer
rule: Without a discovered module root every rule that selects over the layers matches nothing and reports success over an empty model.
constraint: At least one module owns a DCA layer.
selects: "The packages of the imported classes, as a whole - no individual class is reported. A module root is any package that has a subpackage named after one of the configured layer segments, at any depth below the base package."
checks: At least one module root was discovered. The rule says nothing about how many modules there should be or how they are cut; it only establishes that the layer-selecting rules have something to look at. It is the third guard of the same kind as an empty import and an undeclared bounded context.
enforced_by: "StrategicPatternRules#DCA-STR-012"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/StrategicPatternRules.cs
---

# At least one module owns a DCA layer

## Selection

The packages of the imported classes, as a whole - no individual class is reported. A module root is any package that has a subpackage named after one of the configured layer segments, at any depth below the base package.

## Check

At least one module root was discovered. The rule says nothing about how many modules there should be or how they are cut; it only establishes that the layer-selecting rules have something to look at. It is the third guard of the same kind as an empty import and an undeclared bounded context.

## .NET reading

**Selection.** The namespaces of the imported types, as a whole - no individual type is reported. A module root is any namespace that has a child namespace named after one of the configured layer segments, at any depth below the root namespace.

**Check.** At least one module root was discovered. The rule says nothing about how many modules there should be or how they are cut; it only establishes that the layer-selecting rules have something to look at. It is the third guard of the same kind as an empty import and an undeclared bounded context.

## Implementation

```java
DcaRule.check(
        "DCA-STR-012",
        "At least one module owns a DCA layer",
        "Without a discovered module root every rule that selects over the layers matches"
            + " nothing and reports success over an empty model",
        arch -> {
          if (!arch.moduleRoots().isEmpty()) {
            return;
          }
          List<String> segments = new ArrayList<>(arch.layerSegments());
          Collections.sort(segments);
          List<String> observed =
              arch.classes().stream()
                  .map(JavaClass::getPackageName)
                  .distinct()
                  .sorted()
                  .limit(10)
                  .toList();
          throw new DcaRuleViolation(
              "No package below the base package '"
                  + arch.layout().basePackage()
                  + "' carries one of the configured layer segments "
                  + segments
                  + ", so no module root was discovered and every rule that selects over the"
                  + " layers - the whole use-case set among them - passes without having"
                  + " looked at anything. Packages seen"
                  + (observed.size() < 10 ? "" : " (first ten)")
                  + ": "
                  + observed
                  + ".",
              List.of(
                  "Name the segments this code base uses on the layout:"
                      + " withDomainSubpackage(...), withApplicationSubpackage(...) and"
                      + " withAdapterSubpackage(...).",
                  "Check that the base package passed to DcaLayout.forBasePackage is the one"
                      + " the modules live under, and that the import covers them.",
                  "A code base that deliberately has no layered module switches this rule off"
                      + " with a recorded reason."));
        })
    .selecting(
        "The packages of the imported classes, as a whole - no individual class is reported."
            + " A module root is any package that has a subpackage named after one of the"
            + " configured layer segments, at any depth below the base package.")
    .checking(
        "At least one module root was discovered. The rule says nothing about how many"
            + " modules there should be or how they are cut; it only establishes that the"
            + " layer-selecting rules have something to look at. It is the third guard of the"
            + " same kind as an empty import and an undeclared bounded context.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layerSegments()`, `layout()`, `moduleRoots()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-STR-012",
        "At least one module owns a DCA layer",
        "Without a discovered module root every rule that selects over the layers matches nothing and"
            + " reports success over an empty model",
        arch =>
        {
            if (arch.ModuleRoots().Count > 0)
            {
                return;
            }

            var segments = arch.LayerSegments().OrderBy(x => x, StringComparer.Ordinal).ToList();
            var observed = arch.Types
                .Where(t => t.Namespace is not null)
                .Select(t => t.Namespace!.FullName)
                .Distinct(StringComparer.Ordinal)
                .OrderBy(x => x, StringComparer.Ordinal)
                .Take(10)
                .ToList();

            throw DcaRuleViolationException.Of(
                $"No namespace below the root namespace '{arch.Layout.RootNamespace}' carries one of the "
                    + $"configured layer segments [{string.Join(", ", segments)}], so no module root was "
                    + "discovered and every rule that selects over the layers - the whole use-case set among "
                    + "them - passes without having looked at anything. Namespaces seen"
                    + (observed.Count < 10 ? "" : " (first ten)")
                    + $": [{string.Join(", ", observed)}].",
                new[]
                {
                    "Name the segments this code base uses on the layout: WithDomainSegment(...), "
                        + "WithApplicationSegment(...) and WithAdapterSegment(...).",
                    "Check that the root namespace passed to DcaLayout.ForRootNamespace is the one the modules "
                        + "live under, and that every assembly holding them is passed to Load.",
                    "A code base that deliberately has no layered module switches this rule off with a recorded "
                        + "reason.",
                });
        })
    .Selecting(
        "The namespaces of the imported types, as a whole - no individual type is reported. A module root is"
            + " any namespace that has a child namespace named after one of the configured layer segments, at"
            + " any depth below the root namespace.")
    .Checking(
        "At least one module root was discovered. The rule says nothing about how many modules there should be"
            + " or how they are cut; it only establishes that the layer-selecting rules have something to look"
            + " at. It is the third guard of the same kind as an empty import and an undeclared bounded"
            + " context.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
