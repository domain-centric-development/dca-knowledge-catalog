---
type: Reference
title: Repositories must only exist for Aggregate Roots — Overview
tags: [reference]
evidence_for: /rule/tactical/dca-tac-016.md
---

[Full node and context](/rule/tactical/dca-tac-016.md). This is an evidence excerpt; retain the parent selection and caveats.

# Repositories must only exist for Aggregate Roots

## Selection

Interfaces anywhere under scan assignable to Repository whose simple name ends with Repository, the marker Repository itself excluded.

## Check

The aggregate is read from the type argument the interface binds: the first argument of the parameterised Repository marker it extends, or of an intermediate port that is itself assignable to the marker. That type must be assignable to AggregateRoot, and the interface's simple name must be that type's simple name plus 'Repository' - so a repository bound to one aggregate and named after another is reported. An unresolved type argument is skipped: a generic intermediate port such as AuditedRepository<T, ID> binds no aggregate of its own. When the marker is not generic or is used raw, the aggregate is resolved by name instead: among all classes under scan with the interface's simple name minus 'Repository' and in the same context - the nearest enclosing package annotated with @BoundedContext or @SharedKernel, falling back to the first segment below the base package; anywhere when the interface lies outside the base package - at least one must exist and every one must be assignable to AggregateRoot. The interface's methods play no role.

## .NET reading

**Selection.** Interfaces below the root namespace assignable to IRepository whose name ends with Repository; an interface named exactly Repository excluded.

**Check.** The aggregate is read from the type argument the interface binds: the first argument of the generic repository role it implements. That type must be assignable to IAggregateRoot, and the interface's name - minus a leading I followed by an upper-case letter - must be that type's name plus 'Repository', so a repository bound to one aggregate and named after another is reported. An unresolved type argument is skipped: a generic intermediate port such as IAuditedRepository<TAggregate, TId> binds no aggregate of its own. When the role is not generic, is used raw, or the runtime type cannot be resolved, the aggregate is resolved by name instead: among all non-interface types below the root with the interface's name minus 'Repository' and in the same context - the nearest enclosing namespace carrying a [BoundedContext] or [SharedKernel] marker class, falling back to the first segment below the root namespace - at least one must exist and every one must be assignable to IAggregateRoot. The interface's methods play no role.

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
            if (!repoName.endsWith(arch.layout().repositorySuffix())) {
              continue;
            }
            Optional<JavaType> bound =
                boundAggregateArgument(repository, arch.layout().markers().repository());
            if (bound.isPresent()) {
              if (bound.get() instanceof JavaTypeVariable) {
                // A generic intermediate port binds no aggregate of its own.
                continue;
              }
              JavaClass aggregate = bound.get().toErasure();
              if (!aggregate.isAssignableTo(arch.layout().markers().aggregateRoot())) {
                violations.add(
                    repository.getName()
                        + " binds "
                        + aggregate.getName()
                        + " which does not implement AggregateRoot");
              } else if (!repoName.equals(
                  aggregate.getSimpleName() + arch.layout().repositorySuffix())) {
                violations.add(
                    repository.getName()
                        + " binds "
                        + aggregate.getName()
                        + " but is named "
                        + repoName
                        + " - name it "
                        + aggregate.getSimpleName()
                        + arch.layout().repositorySuffix());
              }
              continue;
            }
            String aggregateName =
                repoName.substring(
                    0, repoName.length() - arch.layout().repositorySuffix().length());
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
              if (!candidate.isAssignableTo(arch.layout().markers().aggregateRoot())) {
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
        "The aggregate is read from the type argument the interface binds: the first argument"
            + " of the parameterised Repository marker it extends, or of an intermediate port"
            + " that is itself assignable to the marker. That type must be assignable to"
            + " AggregateRoot, and the interface's simple name must be that type's simple name"
            + " plus 'Repository' - so a repository bound to one aggregate and named after"
            + " another is reported. An unresolved type argument is skipped: a generic"
            + " intermediate port such as AuditedRepository<T, ID> binds no aggregate of its"
            + " own. When the marker is not generic or is used raw, the aggregate is resolved"
            + " by name instead: among all classes under scan with the interface's simple name"
            + " minus 'Repository' and in the same context - the nearest enclosing package"
            + " annotated with @BoundedContext or @SharedKernel, falling back to the first"
            + " segment below the base package; anywhere when the interface lies outside the"
            + " base package - at least one must exist and every one must be assignable to"
            + " AggregateRoot. The interface's methods play no role.",
        "name the repository after the aggregate root it binds")
```

## Helpers
