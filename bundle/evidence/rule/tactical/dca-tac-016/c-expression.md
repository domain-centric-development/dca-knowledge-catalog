---
type: Reference
title: "Repositories must only exist for Aggregate Roots — C# expression"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-016.md#c-expression"
---

[Full node and context](/rule/tactical/dca-tac-016.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

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
