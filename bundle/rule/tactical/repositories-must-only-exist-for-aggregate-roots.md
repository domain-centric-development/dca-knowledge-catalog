---
type: Rule
id: DCA-TAC-016
title: Repositories must only exist for Aggregate Roots
rule: A repository is the collection of one aggregate type; a repository for an entity would let callers bypass the root that guards the aggregate's invariants.
constraint: Repositories must only exist for Aggregate Roots.
enforced_by: "TacticalPatternRules#DCA-TAC-016"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.check(
    "DCA-TAC-016",
    "Repositories must only exist for Aggregate Roots",
    "A repository is the collection of one aggregate type; a repository for an entity would"
        + " let callers bypass the root that guards the aggregate's invariants",
    arch -> {
      List<String> violations = new ArrayList<>();
      for (JavaClass repository : repositoryInterfaces(arch)) {
        String repoName = repository.getSimpleName();
        if (!repoName.endsWith(REPOSITORY_SUFFIX)) {
          continue;
        }
        String aggregateName =
            repoName.substring(0, repoName.length() - REPOSITORY_SUFFIX.length());
        String context = arch.rootContextPackage(repository.getPackageName());
        List<JavaClass> candidates =
            arch.classes().stream()
                .filter(c -> c.getSimpleName().equals(aggregateName))
                .filter(
                    c ->
                        context == null
                            || context.equals(arch.rootContextPackage(c.getPackageName())))
                .collect(Collectors.toList());
        if (candidates.isEmpty()) {
          violations.add(
              repository.getName()
                  + " refers to '"
                  + aggregateName
                  + "' which cannot be resolved in its bounded context ("
                  + (context == null ? "outside base package" : context)
                  + ") - name the repository after the aggregate root it manages");
          continue;
        }
        for (JavaClass candidate : candidates) {
          if (!candidate.isAssignableTo(AggregateRoot.class)) {
            violations.add(
                repository.getName()
                    + " exists for "
                    + candidate.getName()
                    + " which does not implement AggregateRoot");
          }
        }
      }
      fail(
          "Repositories should only exist for Aggregate Roots, not for Entities (DDD pattern).",
          violations);
    })
```

## Applies to markers

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
