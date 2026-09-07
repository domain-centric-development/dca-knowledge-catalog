---
type: Rule
id: DCA-TAC-012
title: Value Objects must be records or immutable classes with attribute equality
rule: A record grants attribute-based equality for free; a hand-written Value Object class must override equals and hashCode itself to compare by its attributes.
constraint: Value Objects must be records or immutable classes with attribute equality.
enforced_by: "TacticalPatternRules#DCA-TAC-012"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-012",
    "Value Objects must be records or immutable classes with attribute equality",
    "A record grants attribute-based equality for free; a hand-written Value Object class must"
        + " override equals and hashCode itself to compare by its attributes",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass valueObject : concreteClassesAssignableTo(arch, Value.class)) {
        if (valueObject.isRecord() || valueObject.isEnum()) {
          continue;
        }
        if (!TypeInspection.declaresAttributeEquality(valueObject)) {
          violations.add(
              valueObject.getName()
                  + " is a non-record Value Object without its own equals(Object)/hashCode()");
        }
      }
      fail(
          "Value Objects are records by preference; an immutable class is allowed, but it must"
              + " implement attribute equality itself.",
          violations);
    })
```

## Applies to markers

- [Value](/marker/tactical/value.md)
