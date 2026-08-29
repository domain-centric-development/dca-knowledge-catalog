---
type: Rule
id: DCA-TAC-006
title: Domain model classes must not have public setter methods
rule: "Behavior-rich domain models change state through intention-revealing methods from the ubiquitous language, never through public setters."
constraint: Domain model classes must not have public setter methods.
enforced_by: "TacticalPatternRules#DCA-TAC-006"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-006",
    "Domain model classes must not have public setter methods",
    "Behavior-rich domain models change state through intention-revealing methods from the"
        + " ubiquitous language, never through public setters",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass domainClass : concreteClassesAssignableTo(arch, Entity.class)) {
        for (JavaMethod method : domainClass.getAllMethods()) {
          if (isSetter(method) && method.getModifiers().contains(JavaModifier.PUBLIC)) {
            violations.add(
                domainClass.getName() + " has public setter '" + method.getName() + "'");
          }
        }
      }
      fail(
          "Domain model classes must not expose public setters - use intention-revealing"
              + " methods from the ubiquitous language.",
          violations);
    })
```

## Applies to markers

- [Entity<T, ID>](/marker/tactical/entity.md)
