---
type: Rule
id: DCA-STR-007
title: Integration Events must be in events or adapter outgoing event packages
rule: "Integration Events must be in events/ packages (published named interface) or adapter.outgoing.event/ packages."
constraint: Integration Events must be in events or adapter outgoing event packages.
selects: Non-interface classes assignable to IntegrationEvent - directly or through a sub-interface - anywhere on the classpath under scan. Interfaces that extend IntegrationEvent are not selected.
checks: "Each resides in a package whose path contains the configured events segment (..events..) or in ..adapter.outgoing.event.. - the trailing event segment is fixed, not configurable. An integration event in a domain or application package is reported."
enforced_by: "StrategicPatternRules#DCA-STR-007"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

## Selection

Non-interface classes assignable to IntegrationEvent - directly or through a sub-interface - anywhere on the classpath under scan. Interfaces that extend IntegrationEvent are not selected.

## Check

Each resides in a package whose path contains the configured events segment (..events..) or in ..adapter.outgoing.event.. - the trailing event segment is fixed, not configurable. An integration event in a domain or application package is reported.

## .NET reading

**Selection.** Non-interface types below the root namespace whose implemented interfaces include IIntegrationEvent - directly or through a derived interface; records and record structs included, interfaces extending IIntegrationEvent not.

**Check.** Each resides in a namespace whose path contains the configured Events segment or Adapter.Outgoing.Event - the trailing Event segment is fixed, not configurable. An integration event in a Domain or Application namespace is reported.

## Implementation

```java
DcaRule.of(
        "DCA-STR-007",
        "Integration Events must be in events or adapter outgoing event packages",
        "Integration Events must be in events/ packages (published named interface) or"
            + " adapter.outgoing.event/ packages",
        arch ->
            classes()
                .that()
                .implement(IntegrationEvent.class)
                .should()
                .resideInAnyPackage(
                    ".." + layout.eventsSubpackage() + "..", outgoingEventAdapterPattern())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes assignable to IntegrationEvent - directly or through a"
            + " sub-interface - anywhere on the classpath under scan. Interfaces that extend"
            + " IntegrationEvent are not selected.")
    .checking(
        "Each resides in a package whose path contains the configured events segment"
            + " (..events..) or in ..adapter.outgoing.event.. - the trailing event segment is"
            + " fixed, not configurable. An integration event in a domain or application"
            + " package is reported.")
```

## Helpers

### `outgoingEventAdapterPattern`

```java
private String outgoingEventAdapterPattern() {
  return ".." + layout.adapterSubpackage() + "." + layout.outgoingSubpackage() + ".event..";
}
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
