---
type: Rule
id: DCA-STR-010
title: "Diagnostic: Event Listeners consuming integration events should use Anti-Corruption Layer"
rule: "Consumed integration events are translated into the consuming context's own language before they reach its domain — verified by code review, not statically."
constraint: "Diagnostic: Event Listeners consuming integration events should use Anti-Corruption Layer."
selects: Informational - selects nothing and never fails; it carries doctrine only.
checks: Nothing is asserted. Whether a consumed integration event is translated into the consuming context's own language before it reaches the domain is a code-review check.
enforced_by: "StrategicPatternRules#DCA-STR-010"
status: informational
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/StrategicPatternRules.cs
---

# Diagnostic: Event Listeners consuming integration events should use Anti-Corruption Layer

## Selection

Informational - selects nothing and never fails; it carries doctrine only.

## Check

Nothing is asserted. Whether a consumed integration event is translated into the consuming context's own language before it reaches the domain is a code-review check.

## Implementation

```java
DcaRule.informational(
        "DCA-STR-010",
        "Diagnostic: Event Listeners consuming integration events should use Anti-Corruption"
            + " Layer",
        "Consumed integration events are translated into the consuming context's own language"
            + " before they reach its domain — verified by code review, not statically",
        arch -> {})
    .selecting("Informational - selects nothing and never fails; it carries doctrine only.")
    .checking(
        "Nothing is asserted. Whether a consumed integration event is translated into the"
            + " consuming context's own language before it reaches the domain is a code-review"
            + " check.")
```

## .NET reading

### C# expression

```csharp
DcaRule.Informational(
        "DCA-STR-010",
        "Diagnostic: Event Listeners consuming integration events should use Anti-Corruption Layer",
        "Consumed integration events are translated into the consuming context's own language before they reach"
            + " its domain — verified by code review, not statically",
        arch => { })
    .Selecting("Informational - selects nothing and never fails; it carries doctrine only.")
    .Checking(
        "Nothing is asserted. Whether a consumed integration event is translated into the"
            + " consuming context's own language before it reaches the domain is a code-review"
            + " check.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
