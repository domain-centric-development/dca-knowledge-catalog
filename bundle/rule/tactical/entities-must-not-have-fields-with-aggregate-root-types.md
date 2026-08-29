---
type: Rule
id: DCA-TAC-007
title: Entities must not have fields with Aggregate Root types
rule: "An entity inside an aggregate references other aggregates by identity only, otherwise the aggregate boundary leaks."
constraint: Entities must not have fields with Aggregate Root types.
enforced_by: "TacticalPatternRules#DCA-TAC-007"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-007",
    "Entities must not have fields with Aggregate Root types",
    "An entity inside an aggregate references other aggregates by identity only, otherwise the"
        + " aggregate boundary leaks",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass entity : nonRootEntities(arch)) {
        for (JavaField field : entity.getAllFields()) {
          JavaClass fieldType = field.getRawType();
          if (isConcreteAggregateRoot(fieldType)) {
            violations.add(
                fieldDescription(entity, field, fieldType) + " which is an aggregate root");
          }
          for (JavaClass element : collectionElementTypes(field)) {
            if (isConcreteAggregateRoot(element)) {
              violations.add(
                  containsDescription(entity, field, element) + " which is an aggregate root");
            }
          }
        }
      }
      fail(
          "Entities must not contain references to aggregate roots (reference by ID only).",
          violations);
    })
```
