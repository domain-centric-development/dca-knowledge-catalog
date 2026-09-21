---
type: Rule
id: DCA-ADV-006
title: "Integration events carry the schema version in their type metadata, not in the payload"
rule: "The schema version is a class property (@IntegrationEventType), never per-instance payload data — an explicit schema-version data field duplicates the annotation and can drift from it."
constraint: "Integration events carry the schema version in their type metadata, not in the payload."
selects: Non-interface classes anywhere on the classpath under scan that are assignable to IntegrationEvent.
checks: "Name heuristic: declared or inherited fields named schemaVersion, eventVersion or contractVersion are reported, including record components. A business revision named version is allowed, whatever its type. This does not infer a field's business meaning; an empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-006"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Integration events carry the schema version in their type metadata, not in the payload

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to IntegrationEvent.

## Check

Name heuristic: declared or inherited fields named schemaVersion, eventVersion or contractVersion are reported, including record components. A business revision named version is allowed, whatever its type. This does not infer a field's business meaning; an empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IIntegrationEvent.

**Check.** Name heuristic: schemaVersion, eventVersion and contractVersion fields (case-insensitive), declared or inherited, including auto-property backing fields and record parameters, are reported. A business revision named version is allowed, whatever its type. A type the loader cannot resolve is read through the ArchUnitNET member model instead, which does not carry the backing fields of auto-properties. The heuristic cannot infer business meaning; an empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-ADV-006",
        "Integration events carry the schema version in their type metadata, not in the payload",
        "The schema version is a class property (@IntegrationEventType), never per-instance payload"
            + " data — an explicit schema-version data field duplicates the annotation and can drift from it",
        arch -> {
          List<String> violations =
              violations(
                  arch,
                  c ->
                      c.isAssignableTo(arch.layout().markers().integrationEvent())
                          && !c.isInterface(),
                  AdvancedPatternRules::hasVersionField,
                  c ->
                      c.getName()
                          + " carries an explicit schema-version field — declare the version in"
                          + " @IntegrationEventType instead");
          failIfAny(
              violations,
              "Integration events carry the schema version in their type metadata, not in the payload — @IntegrationEventType is the"
                  + " single source of truth:");
        })
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to"
            + " IntegrationEvent.")
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
    "DCA-ADV-006",
    "Integration events carry the schema version in their type metadata, not in the payload",
    "The schema version is a class property ([IntegrationEventType]), never per-instance payload"
        + " data — an explicit schema-version data field duplicates the attribute and can drift from it",
    arch => DcaRule.Fail(
        "Integration events carry the schema version in their type metadata, not in the payload — [IntegrationEventType] is the"
            + " single source of truth:",
        Violations(
            arch,
            t => t is not Interface && IsIntegrationEvent(t, arch.Layout.Markers),
            t => HasVersionField(arch, t),
            t => $"{t.FullName} carries an explicit schema-version field — declare the version in"
                + " [IntegrationEventType] instead")))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to IIntegrationEvent.")
    .Checking("Name heuristic: schemaVersion, eventVersion and contractVersion fields (case-insensitive), declared or inherited, including auto-property backing fields and record parameters, are reported. A business revision named version is allowed, whatever its type. A type the loader cannot resolve is read through the ArchUnitNET member model instead, which does not carry the backing fields of auto-properties. The heuristic cannot infer business meaning; an empty selection passes.")
```

## Related mentions (heuristic)

- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
