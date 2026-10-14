---
type: Rule
id: DCA-STR-013
title: Interfaces in a module's events package must extend IntegrationEvent
rule: "Everything in the events package is a published event contract. An interface there is one a producer's integration event implements and a consumer receives; delivery is at least once, so the consumer needs the event's identity and occurrence time through that interface, not only the payload."
constraint: Interfaces in a module's events package must extend IntegrationEvent.
selects: "Top-level interfaces in <module>.<events>.. of every module root, the shared kernel's included, excluding package-info. Annotation types and nested interfaces are not selected - a nested interface belongs to its enclosing contract."
checks: "The interface is assignable to IntegrationEvent, directly or through another interface. Which classes implement it and whether they live in another module are not checked; DCA-ADV-005 and DCA-STR-008 cover the implementing class. An empty selection passes."
enforced_by: "StrategicPatternRules#DCA-STR-013"
status: enforced
maturity: released
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/StrategicPatternRules.cs
---

# Interfaces in a module's events package must extend IntegrationEvent

## Selection

Top-level interfaces in <module>.<events>.. of every module root, the shared kernel's included, excluding package-info. Annotation types and nested interfaces are not selected - a nested interface belongs to its enclosing contract.

## Check

The interface is assignable to IntegrationEvent, directly or through another interface. Which classes implement it and whether they live in another module are not checked; DCA-ADV-005 and DCA-STR-008 cover the implementing class. An empty selection passes.

## .NET reading

**Selection.** Top-level interfaces in <module>.Events and below (segment name from the layout) of every module root, the shared kernel's included. Nested interfaces are not selected - a nested interface belongs to its enclosing contract.

**Check.** The interface is assignable to IIntegrationEvent, directly or through another interface. Which classes implement it and whether they live in another module are not checked; DCA-ADV-005 and DCA-STR-008 cover the implementing class. An empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-STR-013",
        "Interfaces in a module's events package must extend IntegrationEvent",
        "Everything in the events package is a published event contract. An interface there is"
            + " one a producer's integration event implements and a consumer receives; delivery"
            + " is at least once, so the consumer needs the event's identity and occurrence time"
            + " through that interface, not only the payload",
        arch -> {
          List<String> violations = new ArrayList<>();
          String marker = arch.layout().markers().integrationEvent();
          for (String root : arch.moduleRoots()) {
            String events = root + "." + layout.eventsSubpackage();
            for (JavaClass type : arch.classes()) {
              boolean inEvents =
                  type.getPackageName().equals(events)
                      || type.getPackageName().startsWith(events + ".");
              if (inEvents
                  && type.isInterface()
                  && !type.isAnnotation()
                  && type.isTopLevelClass()
                  && !type.getSimpleName().equals("package-info")
                  && !type.isAssignableTo(marker)) {
                violations.add(
                    type.getName()
                        + " is an event contract without the integration event identity");
              }
            }
          }
          if (!violations.isEmpty()) {
            throw new DcaRuleViolation(
                "Interfaces in the events package extend IntegrationEvent, so a consumer reads"
                    + " eventId() and occurredOn() from the contract it listens to.",
                violations);
          }
        })
    .selecting(
        "Top-level interfaces in <module>.<events>.. of every module root, the shared kernel's"
            + " included, excluding package-info. Annotation types and nested interfaces are not"
            + " selected - a nested interface belongs to its enclosing contract.")
    .checking(
        "The interface is assignable to IntegrationEvent, directly or through another"
            + " interface. Which classes implement it and whether they live in another module"
            + " are not checked; DCA-ADV-005 and DCA-STR-008 cover the implementing class. An"
            + " empty selection passes.",
        "let the interface extend IntegrationEvent")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `moduleRoots()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
        "DCA-STR-013",
        "Interfaces in a module's events namespace must extend IIntegrationEvent",
        "Everything in the events namespace is a published event contract. An interface there is"
            + " one a producer's integration event implements and a consumer receives; delivery"
            + " is at least once, so the consumer needs the event's identity and occurrence time"
            + " through that interface, not only the payload",
        arch =>
        {
            var violations = new List<string>();
            var marker = arch.Layout.Markers.IntegrationEvent;
            foreach (var root in arch.ModuleRoots())
            {
                var events = root + "." + Layout.EventsSegment;
                foreach (var type in arch.Interfaces)
                {
                    var ns = type.Namespace?.FullName ?? string.Empty;
                    var inEvents = ns == events || ns.StartsWith(events + ".", StringComparison.Ordinal);
                    if (inEvents && !type.IsNested && !type.IsCompilerGenerated && !IsAssignableTo(arch, type, marker))
                    {
                        violations.Add(type.FullName + " is an event contract without the integration event identity");
                    }
                }
            }

            DcaRule.Fail(
                "Interfaces in the events namespace extend IIntegrationEvent, so a consumer reads"
                    + " EventId and OccurredOn from the contract it listens to.",
                violations.Distinct().OrderBy(v => v, StringComparer.Ordinal).ToList(),
                "let the interface extend IIntegrationEvent");
        })
    .Selecting(
        "Top-level interfaces in <module>.Events and below (segment name from the layout) of"
            + " every module root, the shared kernel's included. Nested interfaces are not selected - a nested interface belongs to its"
            + " enclosing contract.")
    .Checking(
        "The interface is assignable to IIntegrationEvent, directly or through another"
            + " interface. Which classes implement it and whether they live in another module"
            + " are not checked; DCA-ADV-005 and DCA-STR-008 cover the implementing class. An"
            + " empty selection passes.")
```

## Related mentions (heuristic)

- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
