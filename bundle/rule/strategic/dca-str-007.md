---
type: Rule
id: DCA-STR-007
title: Integration event contracts reside in the configured events segment
rule: Integration contracts are published separately from translators and transport adapters.
constraint: Integration event contracts reside in the configured events segment.
selects: Non-interface classes assignable to IntegrationEvent - directly or through a sub-interface - anywhere on the classpath under scan. Interfaces that extend IntegrationEvent are not selected.
checks: Every integration-event contract resides in a package containing the configured events segment. Adapter outgoing event packages are not an alternative; move contracts to events or exclude STR-007 during migration. Translators and transport adapters stay separate.
enforced_by: "StrategicPatternRules#DCA-STR-007"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/StrategicPatternRules.cs
---

# Integration event contracts reside in the configured events segment

## Selection

Non-interface classes assignable to IntegrationEvent - directly or through a sub-interface - anywhere on the classpath under scan. Interfaces that extend IntegrationEvent are not selected.

## Check

Every integration-event contract resides in a package containing the configured events segment. Adapter outgoing event packages are not an alternative; move contracts to events or exclude STR-007 during migration. Translators and transport adapters stay separate.

## .NET reading

**Selection.** Non-interface types below the root namespace whose implemented interfaces include IIntegrationEvent - directly or through a derived interface; records and record structs included, interfaces extending IIntegrationEvent not.

**Check.** Every integration-event contract resides in a namespace containing the configured Events segment. Adapter.Outgoing.Event is not an alternative; move contracts to Events or exclude STR-007 during migration. Translators and transport adapters stay separate.

## Implementation

```java
DcaRule.of(
        "DCA-STR-007",
        "Integration event contracts reside in the configured events segment",
        "Integration contracts are published separately from translators and transport adapters",
        arch ->
            classes()
                .that()
                .implement(IntegrationEvent.class)
                .should()
                .resideInAnyPackage(".." + layout.eventsSubpackage() + "..")
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes assignable to IntegrationEvent - directly or through a"
            + " sub-interface - anywhere on the classpath under scan. Interfaces that extend"
            + " IntegrationEvent are not selected.")
    .checking(
        "Every integration-event contract resides in a package containing the configured events segment. Adapter outgoing event packages are not an alternative; move contracts to events or exclude STR-007 during migration. Translators and transport adapters stay separate.")
```
### C# expression

```csharp
DcaRule.Of(
        "DCA-STR-007",
        "Integration event contracts reside in the configured Events segment",
        "Integration contracts are published separately from translators and transport adapters",
        arch =>
            Types().That().ImplementInterface(typeof(IIntegrationEvent)).And().AreNot(Interfaces())
                .Should().ResideInNamespaceMatching(AnySegment(Layout.EventsSegment)))
    .Selecting(
        "Non-interface types below the root namespace whose implemented interfaces include"
            + " IIntegrationEvent - directly or through a derived interface; records and record"
            + " structs included, interfaces extending IIntegrationEvent not.")
    .Checking("Every integration-event contract resides in a namespace containing the configured Events segment. Adapter.Outgoing.Event is not an alternative; move contracts to Events or exclude STR-007 during migration. Translators and transport adapters stay separate.")
```

## Related mentions (heuristic)

- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
