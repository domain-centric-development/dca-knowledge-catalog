---
type: Rule
id: DCA-TAC-010
title: "Value Object fields must be final (deep immutability)"
rule: Records have implicitly final fields and enums are immutable by design; a hand-written value class must make every instance field final itself.
constraint: "Value Object fields must be final (deep immutability)."
enforced_by: "TacticalPatternRules#DCA-TAC-010"
status: enforced
rule_set: tactical
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-010",
    "Value Object fields must be final (deep immutability)",
    "Records have implicitly final fields and enums are immutable by design; a hand-written"
        + " value class must make every instance field final itself",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass valueObject : concreteClassesAssignableTo(arch, Value.class)) {
        if (valueObject.isRecord() || valueObject.isEnum()) {
          continue;
        }
        for (JavaField field : valueObject.getAllFields()) {
          Set<JavaModifier> modifiers = field.getModifiers();
          if (!modifiers.contains(JavaModifier.FINAL)
              && !modifiers.contains(JavaModifier.STATIC)) {
            violations.add(
                valueObject.getName() + " has non-final field '" + field.getName() + "'");
          }
        }
      }
      fail(
          "Value Object fields must be final for deep immutability (Vernon's DDD).",
          violations);
    })
```

## Applies to markers

- [Value](/marker/tactical/value.md)
