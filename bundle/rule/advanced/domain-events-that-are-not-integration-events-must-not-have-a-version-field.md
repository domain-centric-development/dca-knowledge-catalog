---
type: Rule
id: DCA-ADV-007
title: Domain Events that are not Integration Events must not have a version field
rule: Versioning is a contract concern of integration events — a purely internal domain event has no wire contract to version.
constraint: Domain Events that are not Integration Events must not have a version field.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent but not to IntegrationEvent. A class assignable to both is not selected.
checks: "No field named exactly version - declared by the class or inherited from a supertype, static or not, of any type. Every offender is reported in one violation; an empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-007"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent but not to IntegrationEvent. A class assignable to both is not selected.

## Check

No field named exactly version - declared by the class or inherited from a supertype, static or not, of any type. Every offender is reported in one violation; an empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainEvent but not to IIntegrationEvent. A type assignable to both is not selected.

**Check.** No field named version, compared case-insensitively - declared by the type or inherited from a base type, static or not, of any type; an auto-property or positional record parameter named Version counts. Every offender is reported in one violation; an empty selection passes.

## Implementation

```java
DcaRule.check(
        "DCA-ADV-007",
        "Domain Events that are not Integration Events must not have a version field",
        "Versioning is a contract concern of integration events — a purely internal domain event"
            + " has no wire contract to version",
        arch -> {
          List<String> violations =
              violations(
                  arch,
                  c ->
                      c.isAssignableTo(DomainEvent.class)
                          && !c.isAssignableTo(IntegrationEvent.class)
                          && !c.isInterface(),
                  AdvancedPatternRules::hasVersionField,
                  c ->
                      c.getName()
                          + " has a version field but is not an IntegrationEvent — only"
                          + " IntegrationEvents need versioning");
          failIfAny(
              violations,
              "Domain Events (non-IntegrationEvent) must not have a version field — versioning is"
                  + " only for IntegrationEvents:");
        })
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent"
            + " but not to IntegrationEvent. A class assignable to both is not selected.")
    .checking(
        "No field named exactly version - declared by the class or inherited from a supertype, static or"
            + " not, of any type. Every offender is reported in one violation; an empty selection passes.")
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

- [DomainEvent](/marker/tactical/domainevent.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
