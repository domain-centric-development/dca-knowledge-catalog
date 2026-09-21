---
type: Rule
id: DCA-TAC-016
title: Repositories must only exist for Aggregate Roots
rule: A repository is the collection of one aggregate type; a repository for an entity would let callers bypass the root that guards the aggregate's invariants.
constraint: Repositories must only exist for Aggregate Roots.
selects: "Interfaces anywhere under scan assignable to Repository whose simple name ends with Repository, the marker Repository itself excluded."
checks: "The aggregate is read from the type argument the interface binds: the first argument of the parameterised Repository marker it extends, or of an intermediate port that is itself assignable to the marker. That type must be assignable to AggregateRoot, and the interface's simple name must be that type's simple name plus 'Repository' - so a repository bound to one aggregate and named after another is reported. An unresolved type argument is skipped: a generic intermediate port such as AuditedRepository<T, ID> binds no aggregate of its own. When the marker is not generic or is used raw, the aggregate is resolved by name instead: among all classes under scan with the interface's simple name minus 'Repository' and in the same context - the nearest enclosing package annotated with @BoundedContext or @SharedKernel, falling back to the first segment below the base package; anywhere when the interface lies outside the base package - at least one must exist and every one must be assignable to AggregateRoot. The interface's methods play no role."
enforced_by: "TacticalPatternRules#DCA-TAC-016"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

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

### `repositoryInterfaces`

```java
private static List<JavaClass> repositoryInterfaces(DcaArchitecture arch) {
  return classesMatching(
      arch,
      c ->
          c.isAssignableTo(arch.layout().markers().repository())
              && c.isInterface()
              && !c.getSimpleName().equals(arch.layout().repositorySuffix()));
}
```

### `boundAggregateArgument`

```java
/**
   * The aggregate type a repository interface binds: the first type argument of the parameterised
   * repository marker it extends, or of an intermediate port that is itself assignable to the
   * marker. Empty when the marker is not generic, when it is used raw, or when the binding only
   * becomes concrete further up a chain that substitutes type parameters - the rule then falls back
   * to resolving the aggregate by name.
   */
  private static Optional<JavaType> boundAggregateArgument(JavaClass type, String markerName) {
    for (JavaType candidate : type.getInterfaces()) {
      JavaClass erasure = candidate.toErasure();
      boolean isMarker = erasure.getName().equals(markerName) || erasure.isAssignableTo(markerName);
      if (isMarker
          && candidate instanceof JavaParameterizedType parameterized
          && !parameterized.getActualTypeArguments().isEmpty()) {
        return Optional.of(parameterized.getActualTypeArguments().get(0));
      }
    }
    return Optional.empty();
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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `rootContextPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-016",
    "Repositories must only exist for Aggregate Roots",
    "A repository is the collection of one aggregate type; a repository for an entity would"
    + " let callers bypass the root that guards the aggregate's invariants",
    arch =>
    {
        var violations = new List<string>();
        foreach (var repository in RepositoryInterfaces(arch))
        {
            var repoName = repository.Name.StartsWith("I", StringComparison.Ordinal) && repository.Name.Length > 1 && char.IsUpper(repository.Name[1])
                ? repository.Name.Substring(1)
                : repository.Name;
            if (!repoName.EndsWith(arch.Layout.RepositorySuffix, StringComparison.Ordinal))
            {
                continue;
            }

            var binding = BoundAggregateArgument(arch, repository);
            if (binding is { } bound)
            {
                if (bound.IsGenericParameter)
                {
                    // A generic intermediate port binds no aggregate of its own.
                    continue;
                }

                var boundType = arch.Types.FirstOrDefault(t => t.FullName == bound.FullName);
                if (boundType is null || !IsAssignableTo(arch, boundType, arch.Layout.Markers.AggregateRoot))
                {
                    violations.Add($"{repository.FullName} binds {bound.FullName} which does not implement {nameof(IAggregateRoot)}");
                }
                else if (repoName != bound.Name + arch.Layout.RepositorySuffix)
                {
                    violations.Add(
                        $"{repository.FullName} binds {bound.FullName} but is named {repoName}"
                        + $" - name it {bound.Name}{arch.Layout.RepositorySuffix}");
                }

                continue;
            }

            var aggregateName = repoName.Substring(0, repoName.Length - arch.Layout.RepositorySuffix.Length);
            var context = arch.RootContextNamespace(NamespaceOf(repository));
            var candidates = NonInterfaceTypes(arch)
                .Where(c => c.Name == aggregateName)
                .Where(c => context is null || context == arch.RootContextNamespace(NamespaceOf(c)))
                .ToList();
            if (candidates.Count == 0)
            {
                violations.Add(
                    $"{repository.FullName} refers to '{aggregateName}' which cannot be resolved in its bounded context"
                    + $" ({context ?? "outside root namespace"}) - name the repository after the aggregate root it manages");
                continue;
            }

            foreach (var candidate in candidates)
            {
                if (!IsAssignableTo(arch, candidate, arch.Layout.Markers.AggregateRoot))
                {
                    violations.Add($"{repository.FullName} exists for {candidate.FullName} which does not implement {nameof(IAggregateRoot)}");
                }
            }
        }

        DcaRule.Fail(
            "Repositories should only exist for Aggregate Roots, not for Entities (DDD pattern).",
            violations,
            "name the repository after the aggregate root it binds");
    })
    .Selecting(
        "Interfaces below the root namespace assignable to IRepository whose name "
        + "ends with Repository; an interface named exactly Repository excluded.")
    .Checking(
        "The aggregate is read from the type argument the interface binds: the first argument "
        + "of the generic repository role it implements. That type must be assignable to "
        + "IAggregateRoot, and the interface's name - minus a leading I followed by an "
        + "upper-case letter - must be that type's name plus 'Repository', so a repository "
        + "bound to one aggregate and named after another is reported. An unresolved type "
        + "argument is skipped: a generic intermediate port such as "
        + "IAuditedRepository<TAggregate, TId> binds no aggregate of its own. When the role is "
        + "not generic, is used raw, or the runtime type cannot be resolved, the aggregate is "
        + "resolved by name instead: among all non-interface types below the root with the "
        + "interface's name minus 'Repository' and in the same context - the nearest enclosing "
        + "namespace carrying a [BoundedContext] or [SharedKernel] marker class, falling back "
        + "to the first segment below the root namespace - at least one must exist and every "
        + "one must be assignable to IAggregateRoot. The interface's methods play no role.")
```

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [@SharedKernel](/marker/strategic/sharedkernel.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/tactical/dca-tac-016/overview.md)
- [`repositoryInterfaces`](/evidence/rule/tactical/dca-tac-016/repositoryinterfaces.md)
- [`boundAggregateArgument`](/evidence/rule/tactical/dca-tac-016/boundaggregateargument.md)
- [`fail`](/evidence/rule/tactical/dca-tac-016/fail.md)
- [`classesMatching`](/evidence/rule/tactical/dca-tac-016/classesmatching.md)
- [C# expression](/evidence/rule/tactical/dca-tac-016/c-expression.md)
