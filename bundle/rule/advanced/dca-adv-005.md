---
type: Rule
id: DCA-ADV-005
title: Integration Events must be annotated with IntegrationEventType
rule: "@IntegrationEventType(name, version) is the contract identity of every integration event — the serializer keys (name, version) to the class and stamps both onto the wire envelope."
constraint: Integration Events must be annotated with IntegrationEventType.
selects: "Non-interface classes anywhere on the classpath under scan that are assignable to IntegrationEvent - records, enums and abstract classes included."
checks: "The class itself is annotated with @IntegrationEventType. An annotation on a supertype does not count; the annotation's name and version values are not checked. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-005"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Integration Events must be annotated with IntegrationEventType

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to IntegrationEvent - records, enums and abstract classes included.

## Check

The class itself is annotated with @IntegrationEventType. An annotation on a supertype does not count; the annotation's name and version values are not checked. An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IIntegrationEvent - records, structs and abstract classes included.

**Check.** The type itself carries [IntegrationEventType]. An attribute on a supertype does not count; the attribute's name and version values are not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-005",
        "Integration Events must be annotated with IntegrationEventType",
        "@IntegrationEventType(name, version) is the contract identity of every integration event"
            + " — the serializer keys (name, version) to the class and stamps both onto the wire"
            + " envelope",
        arch ->
            classes()
                .that()
                .areAssignableTo(arch.layout().markers().integrationEvent())
                .and()
                .areNotInterfaces()
                .should()
                .beAnnotatedWith(IntegrationEventType.class)
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to"
            + " IntegrationEvent - records, enums and abstract classes included.")
    .checking(
        "The class itself is annotated with @IntegrationEventType. An annotation on a supertype does not"
            + " count; the annotation's name and version values are not checked. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ADV-005",
    "Integration Events must be annotated with IntegrationEventType",
    "[IntegrationEventType(name, Version)] is the contract identity of every integration event"
        + " — the serializer keys (name, version) to the class and stamps both onto the wire"
        + " envelope",
    arch => DcaRule.Fail(
        "Integration Events must be annotated with [IntegrationEventType]:",
        Violations(
            arch,
            t => t is not Interface && IsIntegrationEvent(t, arch.Layout.Markers),
            t => !t.HasAttribute(typeof(IntegrationEventTypeAttribute).FullName!),
            t => $"{t.FullName} is not annotated with [IntegrationEventType]")))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to IIntegrationEvent - "
        + "records, structs and abstract classes included.")
    .Checking(
        "The type itself carries [IntegrationEventType]. An attribute on a supertype does not "
        + "count; the attribute's name and version values are not checked. An empty selection "
        + "passes.")
```

## Related mentions (heuristic)

- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
