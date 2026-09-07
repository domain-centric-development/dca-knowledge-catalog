---
type: Rule
id: DCA-TAC-003
title: Aggregate Roots must not have fields with other Aggregate Root types
rule: "Vernon's Aggregate Design Rule #2: reference other Aggregates by identity to keep aggregate boundaries and transactional consistency intact."
constraint: Aggregate Roots must not have fields with other Aggregate Root types.
enforced_by: "TacticalPatternRules#DCA-TAC-003"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-003",
    "Aggregate Roots must not have fields with other Aggregate Root types",
    "Vernon's Aggregate Design Rule #2: reference other Aggregates by identity to keep"
        + " aggregate boundaries and transactional consistency intact",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass aggregate : concreteClassesAssignableTo(arch, AggregateRoot.class)) {
        for (JavaField field : TypeInspection.instanceFields(aggregate)) {
          for (JavaClass involved : TypeInspection.involvedTypes(field, aggregate)) {
            if (isConcreteAggregateRoot(involved)
                && !isSelfReference(aggregate, field, involved)) {
              violations.add(
                  fieldDescription(aggregate, field, involved)
                      + " which is another aggregate root");
            }
          }
        }
      }
      fail(
          "Aggregates must reference other aggregates by ID only (Vernon's Rule #2).",
          violations);
    })
```

## Applies to markers

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
