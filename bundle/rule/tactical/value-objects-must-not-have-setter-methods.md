---
type: Rule
id: DCA-TAC-011
title: Value Objects must not have setter methods
rule: Value Objects are immutable; state changes produce a new instance instead of mutating.
constraint: Value Objects must not have setter methods.
enforced_by: "TacticalPatternRules#DCA-TAC-011"
status: enforced
rule_set: tactical
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-011",
    "Value Objects must not have setter methods",
    "Value Objects are immutable; state changes produce a new instance instead of mutating",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass valueObject : concreteClassesAssignableTo(arch, Value.class)) {
        for (JavaMethod method : valueObject.getAllMethods()) {
          if (isSetter(method)) {
            violations.add(
                valueObject.getName() + " has setter method '" + method.getName() + "'");
          }
        }
      }
      fail("Value Objects must be immutable and should not have setter methods.", violations);
    })
```

## Applies to markers

- [Value](/marker/tactical/value.md)
