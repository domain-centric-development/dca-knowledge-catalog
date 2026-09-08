---
type: Rule
id: DCA-ADV-006
title: Integration Events must not have a version field
rule: "The schema version is a class property (@IntegrationEventType), never per-instance payload data — a version data field duplicates the annotation and can drift from it."
constraint: Integration Events must not have a version field.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to IntegrationEvent.
checks: "No field named exactly version - declared by the class or inherited from a supertype, static or not, of any type. A record component named version counts as a field. Every offender is reported in one violation; an empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-006"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to IntegrationEvent.

## Check

No field named exactly version - declared by the class or inherited from a supertype, static or not, of any type. A record component named version counts as a field. Every offender is reported in one violation; an empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IIntegrationEvent.

**Check.** No field named version, compared case-insensitively - declared by the type or inherited from a base type, static or not, of any type. An auto-property named Version counts through its backing field, and so does a positional record parameter. Every offender is reported in one violation; an empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-ADV-006",
        "Integration Events must not have a version field",
        "The schema version is a class property (@IntegrationEventType), never per-instance payload"
            + " data — a version data field duplicates the annotation and can drift from it",
        arch -> {
          List<String> violations =
              violations(
                  arch,
                  c -> c.isAssignableTo(IntegrationEvent.class) && !c.isInterface(),
                  AdvancedPatternRules::hasVersionField,
                  c ->
                      c.getName()
                          + " carries a version data field — declare the version in"
                          + " @IntegrationEventType instead");
          failIfAny(
              violations,
              "Integration Events must not have a version field — @IntegrationEventType is the"
                  + " single source of truth:");
        })
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to"
            + " IntegrationEvent.")
    .checking(
        "No field named exactly version - declared by the class or inherited from a supertype, static or"
            + " not, of any type. A record component named version counts as a field. Every offender is"
            + " reported in one violation; an empty selection passes.")
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)
- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
