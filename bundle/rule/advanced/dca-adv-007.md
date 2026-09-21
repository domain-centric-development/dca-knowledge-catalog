---
type: Rule
id: DCA-ADV-007
title: Domain events that are not integration events carry no schema version
rule: Versioning is a contract concern of integration events — a purely internal domain event has no wire contract to version.
constraint: Domain events that are not integration events carry no schema version.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent but not to IntegrationEvent. A class assignable to both is not selected.
checks: "Name heuristic: declared or inherited fields named schemaVersion, eventVersion or contractVersion are reported, including record components. A business revision named version is allowed, whatever its type. This does not infer a field's business meaning; an empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-007"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Domain events that are not integration events carry no schema version

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent but not to IntegrationEvent. A class assignable to both is not selected.

## Check

Name heuristic: declared or inherited fields named schemaVersion, eventVersion or contractVersion are reported, including record components. A business revision named version is allowed, whatever its type. This does not infer a field's business meaning; an empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainEvent but not to IIntegrationEvent. A type assignable to both is not selected.

**Check.** Name heuristic: schemaVersion, eventVersion and contractVersion fields (case-insensitive), declared or inherited, including auto-property backing fields and record parameters, are reported. A business revision named version is allowed, whatever its type. A type the loader cannot resolve is read through the ArchUnitNET member model instead, which does not carry the backing fields of auto-properties. The heuristic cannot infer business meaning; an empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-ADV-007",
        "Domain events that are not integration events carry no schema version",
        "Versioning is a contract concern of integration events — a purely internal domain event"
            + " has no wire contract to version",
        arch -> {
          List<String> violations =
              violations(
                  arch,
                  c ->
                      c.isAssignableTo(arch.layout().markers().domainEvent())
                          && !c.isAssignableTo(arch.layout().markers().integrationEvent())
                          && !c.isInterface(),
                  AdvancedPatternRules::hasVersionField,
                  c ->
                      c.getName()
                          + " has an explicit schema-version field but is not an IntegrationEvent — only"
                          + " IntegrationEvents need schema versioning");
          failIfAny(
              violations,
              "Domain Events (non-IntegrationEvent) must not have an explicit schema-version field — schema versioning is"
                  + " only for IntegrationEvents:");
        })
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent"
            + " but not to IntegrationEvent. A class assignable to both is not selected.")
    .checking(
        "Name heuristic: declared or inherited fields named schemaVersion, eventVersion or contractVersion are reported, including record components. A business revision named version is allowed, whatever its type. This does not infer a field's business meaning; an empty selection passes.")
```

## Helpers

### `violations`

```java
private static List<String> violations(
    DcaArchitecture arch,
    Predicate<JavaClass> candidate,
    Predicate<JavaClass> violates,
    java.util.function.Function<JavaClass, String> message) {
  List<String> violations = new ArrayList<>();
  for (JavaClass javaClass : arch.classes()) {
    if (candidate.test(javaClass) && violates.test(javaClass)) {
      violations.add(message.apply(javaClass));
    }
  }
  return violations;
}
```

### `failIfAny`

```java
private static void failIfAny(List<String> violations, String header) {
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(header, violations);
  }
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ADV-007",
    "Domain events that are not integration events carry no schema version",
    "Versioning is a contract concern of integration events — a purely internal domain event"
        + " has no wire contract to version",
    arch => DcaRule.Fail(
        "Domain Events (non-IIntegrationEvent) must not have an explicit schema-version field — schema versioning is"
            + " only for IIntegrationEvents:",
        Violations(
            arch,
            t => t is not Interface && IsDomainEvent(t, arch.Layout.Markers) && !IsIntegrationEvent(t, arch.Layout.Markers),
            t => HasVersionField(arch, t),
            t => $"{t.FullName} has an explicit schema-version field but is not an IIntegrationEvent — only"
                + " IIntegrationEvents need schema versioning")))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to IDomainEvent but not to "
        + "IIntegrationEvent. A type assignable to both is not selected.")
    .Checking("Name heuristic: schemaVersion, eventVersion and contractVersion fields (case-insensitive), declared or inherited, including auto-property backing fields and record parameters, are reported. A business revision named version is allowed, whatever its type. A type the loader cannot resolve is read through the ArchUnitNET member model instead, which does not carry the backing fields of auto-properties. The heuristic cannot infer business meaning; an empty selection passes.")
```

## Related mentions (heuristic)

- [DomainEvent](/marker/tactical/domainevent.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
