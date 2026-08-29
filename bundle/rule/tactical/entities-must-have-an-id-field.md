---
type: Rule
id: DCA-TAC-004
title: Entities must have an ID field
rule: "An Entity is defined by its identity, which is a value object implementing the Id marker."
constraint: Entities must have an ID field.
enforced_by: "TacticalPatternRules#DCA-TAC-004"
status: enforced
rule_set: tactical
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-004",
    "Entities must have an ID field",
    "An Entity is defined by its identity, which is a value object implementing the Id marker",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass entity : concreteClassesAssignableTo(arch, Entity.class)) {
        if (entity.getModifiers().contains(JavaModifier.ABSTRACT)) {
          continue;
        }
        boolean hasIdField =
            entity.getAllFields().stream()
                .anyMatch(f -> f.getRawType().isAssignableTo(Id.class));
        if (!hasIdField) {
          violations.add(
              entity.getName()
                  + " has no field whose type implements "
                  + Id.class.getSimpleName());
        }
      }
      fail(
          "Entities must have an identity field typed as an Id value object (DDD pattern).",
          violations);
    })
```

## Applies to markers

- [Entity<T, ID>](/marker/tactical/entity.md)
- [Id](/marker/tactical/id.md)
