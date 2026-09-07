---
type: Rule
id: DCA-TAC-008
title: Value Objects must not contain Aggregate Roots or Entities
rule: A Value Object is defined by its attributes; holding an object with identity would give it a lifecycle it must not have.
constraint: Value Objects must not contain Aggregate Roots or Entities.
enforced_by: "TacticalPatternRules#DCA-TAC-008"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-008",
    "Value Objects must not contain Aggregate Roots or Entities",
    "A Value Object is defined by its attributes; holding an object with identity would give"
        + " it a lifecycle it must not have",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass valueObject : concreteClassesAssignableTo(arch, Value.class)) {
        for (JavaField field : TypeInspection.instanceFields(valueObject)) {
          for (JavaClass involved : TypeInspection.involvedTypes(field, valueObject)) {
            if (isConcreteAggregateRoot(involved)) {
              violations.add(
                  fieldDescription(valueObject, field, involved)
                      + " which is an aggregate root");
            }
            if (isConcreteNonRootEntity(involved)) {
              violations.add(
                  fieldDescription(valueObject, field, involved) + " which is an entity");
            }
          }
        }
      }
      fail(
          "Value Objects must only contain other Value Objects or primitives (Vernon's DDD).",
          violations);
    })
```

## Applies to markers

- [Value](/marker/tactical/value.md)
