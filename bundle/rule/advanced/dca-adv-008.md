---
type: Rule
id: DCA-ADV-008
title: Domain Events must have a timestamp field
rule: "An event records something that happened — without a timestamp the fact cannot be ordered, replayed or audited."
constraint: Domain Events must have a timestamp field.
selects: "Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent. IntegrationEvent does not extend DomainEvent, so an integration event is selected only when it also implements DomainEvent."
checks: "At least one field - declared by the class or inherited from a supertype, static or not, of any name - has one of the configured timestamp types, by default java.time.Instant, OffsetDateTime, ZonedDateTime or LocalDateTime; a record component of one of these types counts. LocalDate, long or Date fields do not satisfy it, and a timestamp method without a backing field does not either - which is what the rule is for, because the marker already forces the accessor. A project whose own event vocabulary wraps the timestamp in a value object names that type with withTimestampTypes. Every offender is reported in one violation; an empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-008"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Domain Events must have a timestamp field

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent. IntegrationEvent does not extend DomainEvent, so an integration event is selected only when it also implements DomainEvent.

## Check

At least one field - declared by the class or inherited from a supertype, static or not, of any name - has one of the configured timestamp types, by default java.time.Instant, OffsetDateTime, ZonedDateTime or LocalDateTime; a record component of one of these types counts. LocalDate, long or Date fields do not satisfy it, and a timestamp method without a backing field does not either - which is what the rule is for, because the marker already forces the accessor. A project whose own event vocabulary wraps the timestamp in a value object names that type with withTimestampTypes. Every offender is reported in one violation; an empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainEvent. IIntegrationEvent does not extend IDomainEvent, so an integration event is selected only when it also implements IDomainEvent.

**Check.** At least one field - declared by the type or inherited from a base type, static or not, of any name - has one of the configured timestamp types, by default System.DateTimeOffset or System.DateTime; an auto-property or positional record parameter of one of these types counts through its backing field. DateOnly, TimeSpan, long or string fields do not satisfy it, and a computed property without a backing field does not either - which is what the rule is for, because the marker already forces the accessor; a project whose own event vocabulary wraps the timestamp in a value type names that type with WithTimestampTypes. A type the loader cannot resolve is read through the ArchUnitNET member model instead, which does not carry the backing fields of auto-properties. Every offender is reported in one violation; an empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-ADV-008",
        "Domain Events must have a timestamp field",
        "An event records something that happened — without a timestamp the fact cannot be"
            + " ordered, replayed or audited",
        arch -> {
          List<String> violations =
              violations(
                  arch,
                  c ->
                      c.isAssignableTo(arch.layout().markers().domainEvent())
                          && !c.isInterface(),
                  c -> !hasTimestampField(c, arch.layout().timestampTypes()),
                  c -> c.getName() + " does not have a timestamp field");
          failIfAny(
              violations,
              "Domain Events must have a timestamp field (when did the event occur?):");
        })
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent."
            + " IntegrationEvent does not extend DomainEvent, so an integration event is selected only when it"
            + " also implements DomainEvent.")
    .checking(
        "At least one field - declared by the class or inherited from a supertype, static or not, of any"
            + " name - has one of the configured timestamp types, by default java.time.Instant,"
            + " OffsetDateTime, ZonedDateTime or LocalDateTime; a record component of one of these types"
            + " counts. LocalDate, long or Date fields do not satisfy it, and a timestamp method without a"
            + " backing field does not either - which is what the rule is for, because the marker already"
            + " forces the accessor. A project whose own event vocabulary wraps the timestamp in a value"
            + " object names that type with withTimestampTypes. Every offender is reported in one"
            + " violation; an empty selection passes.")
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

### `hasTimestampField`

```java
private static boolean hasTimestampField(JavaClass eventClass, List<String> timestampTypes) {
  return eventClass.getAllFields().stream()
      .anyMatch(f -> timestampTypes.contains(f.getRawType().getName()));
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
    "DCA-ADV-008",
    "Domain Events must have a timestamp field",
    "An event records something that happened — without a timestamp the fact cannot be"
        + " ordered, replayed or audited",
    arch => DcaRule.Fail(
        "Domain Events must have a timestamp field (when did the event occur?):",
        Violations(
            arch,
            t => t is not Interface && IsDomainEvent(t, arch.Layout.Markers),
            t => !HasTimestampField(arch, t),
            t => $"{t.FullName} does not have a timestamp field")))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to IDomainEvent. "
        + "IIntegrationEvent does not extend IDomainEvent, so an integration event is selected only "
        + "when it also implements IDomainEvent.")
    .Checking(
        "At least one field - declared by the type or inherited from a base type, static or not, "
        + "of any name - has one of the configured timestamp types, by default System.DateTimeOffset "
        + "or System.DateTime; an auto-property or "
        + "positional record parameter of one of these types counts through its backing field. "
        + "DateOnly, TimeSpan, long or string fields do not satisfy it, and a computed property "
        + "without a backing field does not either - which is what the rule is for, because the "
        + "marker already forces the accessor; a project whose own event vocabulary wraps the "
        + "timestamp in a value type names that type with WithTimestampTypes. A type the loader "
        + "cannot resolve is read "
        + "through the ArchUnitNET member model instead, which does not carry the backing fields "
        + "of auto-properties. Every offender is reported in one violation; an empty selection "
        + "passes.")
```

## Related mentions (heuristic)

- [DomainEvent](/marker/tactical/domainevent.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
