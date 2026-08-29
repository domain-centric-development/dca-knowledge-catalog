---
type: Rule
id: DCA-TAC-005
title: Entities must not be instantiated directly from outside the aggregate
rule: Entities are created through their aggregate root so that the root can enforce its invariants.
constraint: Entities must not be instantiated directly from outside the aggregate.
enforced_by: "TacticalPatternRules#DCA-TAC-005"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-005",
    "Entities must not be instantiated directly from outside the aggregate",
    "Entities are created through their aggregate root so that the root can enforce its"
        + " invariants",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass entity : nonRootEntities(arch)) {
        if (entity.isRecord()) {
          continue;
        }
        entity.getConstructors().stream()
            .filter(c -> c.getModifiers().contains(JavaModifier.PUBLIC))
            .forEach(
                c ->
                    violations.add(
                        entity.getName()
                            + " has public constructor - should be package-private or"
                            + " protected"));
      }
      fail(
          "Entities should not have public constructors (access only through aggregate root).\n"
              + "Note: Records are excluded from this rule.",
          violations);
    })
```
