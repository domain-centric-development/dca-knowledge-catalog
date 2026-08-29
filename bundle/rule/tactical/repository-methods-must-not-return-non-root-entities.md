---
type: Rule
id: DCA-TAC-017
title: Repository methods must not return non-root Entities
rule: "A caller receiving an Entity that is not an Aggregate Root could mutate part of an aggregate without passing its root, so the root's invariants would never run."
constraint: Repository methods must not return non-root Entities.
enforced_by: "TacticalPatternRules#DCA-TAC-017"
status: enforced
rule_set: tactical
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-017",
    "Repository methods must not return non-root Entities",
    "A caller receiving an Entity that is not an Aggregate Root could mutate part of an"
        + " aggregate without passing its root, so the root's invariants would never run",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass repository : repositoryInterfaces(arch)) {
        for (JavaMethod method : repository.getMethods()) {
          for (JavaClass type : typesInvolvedIn(method.getReturnType())) {
            if (type.isAssignableTo(Entity.class)
                && !type.isAssignableTo(AggregateRoot.class)) {
              violations.add(
                  repository.getName()
                      + "."
                      + method.getName()
                      + " exposes "
                      + type.getName()
                      + ", an Entity that is not an Aggregate Root");
            }
          }
        }
      }
      fail(
          "Repository methods must not expose an Entity that is not an Aggregate Root: a caller"
              + " could mutate part of an aggregate without passing its root (DDD pattern).",
          violations);
    })
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Entity<T, ID>](/marker/tactical/entity.md)
