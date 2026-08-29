---
type: Rule
id: DCA-TAC-008
title: Value Objects must not contain Aggregate Roots or Entities
rule: A Value Object is defined by its attributes; holding an object with identity would give it a lifecycle it must not have.
constraint: Value Objects must not contain Aggregate Roots or Entities.
enforced_by: "TacticalPatternRules#DCA-TAC-008"
status: enforced
rule_set: tactical
implementations: [java]
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
        for (JavaField field : valueObject.getAllFields()) {
          JavaClass fieldType = field.getRawType();
          if (isConcreteAggregateRoot(fieldType)) {
            violations.add(
                fieldDescription(valueObject, field, fieldType)
                    + " which is an aggregate root");
          }
          if (isConcreteNonRootEntity(fieldType)) {
            violations.add(
                fieldDescription(valueObject, field, fieldType) + " which is an entity");
          }
          for (JavaClass element : collectionElementTypes(field)) {
            if (isConcreteAggregateRoot(element)) {
              violations.add(
                  containsDescription(valueObject, field, element)
                      + " which is an aggregate root");
            }
            if (isConcreteNonRootEntity(element)) {
              violations.add(
                  containsDescription(valueObject, field, element) + " which is an entity");
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
