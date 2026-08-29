---
type: Rule
id: DCA-TAC-021
title: Store interfaces must not declare findById or save methods
rule: "findById/save are Repository semantics; a Store that has them is a Repository wearing the wrong name, and the stored object should then be an Aggregate Root."
constraint: Store interfaces must not declare findById or save methods.
enforced_by: "TacticalPatternRules#DCA-TAC-021"
status: enforced
rule_set: tactical
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-021",
    "Store interfaces must not declare findById or save methods",
    "findById/save are Repository semantics; a Store that has them is a Repository wearing the"
        + " wrong name, and the stored object should then be an Aggregate Root",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass store : storeInterfaces(arch)) {
        for (JavaMethod method : store.getMethods()) {
          if (REPOSITORY_METHOD_NAMES.contains(method.getName())) {
            violations.add(
                store.getFullName()
                    + "."
                    + method.getName()
                    + "() - Repository semantics on a Store");
          }
        }
      }
      if (!violations.isEmpty()) {
        throw new AssertionError(
            "Store interfaces use record/count/exists semantics, not findById/save.\n"
                + "Violations:\n"
                + String.join("\n", violations)
                + "\n\nFix: rename to *Repository if the stored object is an Aggregate Root,"
                + " otherwise rename the methods to record(...), count(...), exists(...).");
      }
    })
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
