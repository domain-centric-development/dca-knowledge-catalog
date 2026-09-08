---
type: Rule
id: DCA-TAC-016
title: Repositories must only exist for Aggregate Roots
rule: A repository is the collection of one aggregate type; a repository for an entity would let callers bypass the root that guards the aggregate's invariants.
constraint: Repositories must only exist for Aggregate Roots.
selects: "Interfaces anywhere under scan assignable to Repository whose simple name ends with Repository, the marker Repository itself excluded."
checks: "The aggregate name is the interface's simple name minus 'Repository'. Among all classes under scan with exactly that simple name and in the same context - the nearest enclosing package annotated with @BoundedContext or @SharedKernel, falling back to the first segment below the base package; anywhere when the interface lies outside the base package - at least one must exist and every one must be assignable to AggregateRoot. No such class and a class that is not an aggregate root are both reported; the interface's methods play no role."
enforced_by: "TacticalPatternRules#DCA-TAC-016"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Interfaces anywhere under scan assignable to Repository whose simple name ends with Repository, the marker Repository itself excluded.

## Check

The aggregate name is the interface's simple name minus 'Repository'. Among all classes under scan with exactly that simple name and in the same context - the nearest enclosing package annotated with @BoundedContext or @SharedKernel, falling back to the first segment below the base package; anywhere when the interface lies outside the base package - at least one must exist and every one must be assignable to AggregateRoot. No such class and a class that is not an aggregate root are both reported; the interface's methods play no role.

## .NET reading

**Selection.** Interfaces below the root namespace assignable to IRepository whose name ends with Repository; an interface named exactly Repository excluded.

**Check.** The aggregate name is the interface's name minus a leading I followed by an upper-case letter and minus 'Repository'. Among all non-interface types below the root with exactly that name and in the same context - the nearest enclosing namespace carrying a [BoundedContext] or [SharedKernel] marker class, falling back to the first segment below the root namespace - at least one must exist and every one must be assignable to IAggregateRoot. No such type and a type that is not an aggregate root are both reported; the interface's methods play no role.

## Implementation

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
    .selecting(
        "Interfaces anywhere under scan assignable to Repository whose simple name ends "
            + "with Repository, the marker Repository itself excluded.")
    .checking(
        "The aggregate name is the interface's simple name minus 'Repository'. Among "
            + "all classes under scan with exactly that simple name and in the same context - "
            + "the nearest enclosing package annotated with @BoundedContext or @SharedKernel, "
            + "falling back to the first segment below the base package; anywhere when the "
            + "interface lies outside the base package - at least one must exist and every "
            + "one must be assignable to AggregateRoot. No such class and a class that is not "
            + "an aggregate root are both reported; the interface's methods play no role.")
```

## Helpers

### `repositoryInterfaces`

```java
private static List<JavaClass> repositoryInterfaces(DcaArchitecture arch) {
  return classesMatching(
      arch,
      c ->
          c.isAssignableTo(Repository.class)
              && c.isInterface()
              && !c.getSimpleName().equals(REPOSITORY_SUFFIX));
}
```

### `fail`

```java
private static void fail(String message, List<String> violations) {
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(message, violations);
  }
}
```

### `classesMatching`

```java
private static List<JavaClass> classesMatching(
    DcaArchitecture arch, Predicate<JavaClass> filter) {
  return arch.classes().stream().filter(filter).collect(Collectors.toList());
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `rootContextPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
