---
type: Rule
id: DCA-LAY-001
title: "Diagnostic: The rules of the Layered Architecture should be followed"
rule: "Traditional layering (application accessed only by incoming adapters) contradicts Ports and Adapters, where outgoing adapters implement application-level output ports; the hexagonal rules cover the intended dependency direction."
constraint: "Diagnostic: The rules of the Layered Architecture should be followed."
selects: "Informational - selects nothing. ArchUnit's layered-architecture definition (adapter layer accesses application, application accesses domain, domain accesses nothing) is not built, because in Ports and Adapters outgoing adapters implement application-level output ports."
checks: Informational - selects nothing and never fails; it carries doctrine only. The dependency direction is enforced by the hexagonal rules.
enforced_by: "LayeredRules#DCA-LAY-001"
status: informational
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/LayeredRules.cs
---

# Diagnostic: The rules of the Layered Architecture should be followed

## Selection

Informational - selects nothing. ArchUnit's layered-architecture definition (adapter layer accesses application, application accesses domain, domain accesses nothing) is not built, because in Ports and Adapters outgoing adapters implement application-level output ports.

## Check

Informational - selects nothing and never fails; it carries doctrine only. The dependency direction is enforced by the hexagonal rules.

## .NET reading

**Selection.** Informational - selects nothing. A classic layered-architecture definition (adapter layer accesses application, application accesses domain, domain accesses nothing) is not built, because in Ports and Adapters outgoing adapters implement application-level output ports.

**Check.** Informational - selects nothing and never fails; it carries doctrine only. The dependency direction is enforced by the hexagonal rules.

## Implementation

```java
DcaRule.informational(
        "DCA-LAY-001",
        "Diagnostic: The rules of the Layered Architecture should be followed",
        "Traditional layering (application accessed only by incoming adapters) contradicts Ports"
            + " and Adapters, where outgoing adapters implement application-level output ports;"
            + " the hexagonal rules cover the intended dependency direction",
        arch -> List.of())
    .selecting(
        "Informational - selects nothing. ArchUnit's layered-architecture definition (adapter"
            + " layer accesses application, application accesses domain, domain accesses"
            + " nothing) is not built, because in Ports and Adapters outgoing adapters"
            + " implement application-level output ports.")
    .checking(
        "Informational - selects nothing and never fails; it carries doctrine only. The"
            + " dependency direction is enforced by the hexagonal rules.")
```
### C# expression

```csharp
DcaRule.Informational(
    "DCA-LAY-001",
    "Diagnostic: The rules of the Layered Architecture should be followed",
    "Traditional layering (application accessed only by incoming adapters) contradicts Ports"
        + " and Adapters, where outgoing adapters implement application-level output ports;"
        + " the hexagonal rules cover the intended dependency direction",
    arch => Array.Empty<string>())
    .Selecting(
        "Informational - selects nothing. A classic layered-architecture definition (adapter "
        + "layer accesses application, application accesses domain, domain accesses nothing) is not "
        + "built, because in Ports and Adapters outgoing adapters implement application-level "
        + "output ports.")
    .Checking(
        "Informational - selects nothing and never fails; it carries doctrine only. The "
        + "dependency direction is enforced by the hexagonal rules.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
