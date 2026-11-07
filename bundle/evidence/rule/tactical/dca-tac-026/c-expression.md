---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — C# expression"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#c-expression"
---

[Full node and context](/rule/tactical/dca-tac-026.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-026",
    "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id",
    "An object loaded by its id alone is reachable by anyone who knows or guesses the id - the insecure direct"
    + " object reference of broken access control (OWASP Top 10, A01). An aggregate marked as owned belongs to"
    + " someone; its repository offers a lookup scoped to the owner, so a use case acting for a caller can load"
    + " it through the caller and an unscoped lookup is never the only way in. Whether the use case calls the"
    + " scoped lookup, and whether it proved the caller's right to a change of owner, is logic the rule does"
    + " not see",
    arch =>
    {
        var violations = new List<string>();
        var repositories = RepositoryInterfaces(arch).ToList();
        foreach (var aggregate in NonInterfaceTypes(arch).OfType<Class>()
                     .Where(c => c.IsAbstract != true
                         && IsRole(arch, c, nameof(DcaMarkers.Owned))
                         && IsRole(arch, c, nameof(DcaMarkers.AggregateRoot))))
        {
            var runtime = arch.RuntimeType(aggregate);
            if (runtime is null)
            {
                continue;
            }

            var ownerId = OwnerIdOf(arch, runtime);
            if (ownerId is null || ownerId.IsGenericParameter)
            {
                violations.Add(
                    $"{aggregate.FullName} is owned but names no owner id type - implement the generic"
                    + $" {SimpleTypeName(arch.Layout.Markers.Owned)}<TOwnerId> with the owner's id type");
                continue;
            }

            foreach (var repository in RepositoriesOf(arch, aggregate, runtime, repositories))
            {
                var repositoryType = arch.RuntimeType(repository);
                if (repositoryType is null)
                {
                    continue;
                }

                var aggregateId = AggregateIdOf(arch, runtime, repositoryType);
                var methods = repositoryType.GetMethods()
                    .Concat(repositoryType.GetInterfaces().SelectMany(i => i.GetMethods()));
                if (!methods.Any(m => IsScopedLookup(arch, m, runtime, aggregateId, ownerId)))
                {
                    violations.Add(
                        $"{repository.FullName} declares no lookup taking {aggregateId?.Name ?? "the aggregate's id"}"
                        + $" and {ownerId.Name} for the owned aggregate {aggregate.FullName}");
                }
            }
        }

        DcaRule.Fail(
            "The repository of an owned aggregate must declare a lookup by the aggregate's id and the owner's id,"
            + " so the aggregate is never reachable by its id alone.",
            violations,
            "add a lookup such as FindByIdForOwnerAsync(id, ownerId) returning the aggregate, and load it through"
            + " that method wherever a caller is known");
    })
    .Experimental()
    .Selecting(
        "Concrete classes below the root namespace assignable to both the owned role (by default IOwned of"
        + " the building blocks) and the aggregate-root role, with their runtime type in the loaded assemblies,"
        + " each with the repository interfaces that bind it: the first type argument of the generic"
        + " repository role, or - where the binding is raw or unresolved - the interface in the same context"
        + " named after the aggregate plus the repository suffix, with or without the leading I. An owned"
        + " aggregate without a repository is not selected.")
    .Checking(
        "The owner id type is the type argument of the generic interface the aggregate implements that carries"
        + " the owned role; an aggregate that implements only the non-generic role, or binds a generic parameter,"
        + " is reported. The aggregate's id type is the second type argument of the repository's binding, or"
        + " else the type of the aggregate's Id property. At least one method of the repository, inherited"
        + " interface methods included, takes a parameter of exactly the aggregate's id type and a further"
        + " parameter of exactly the owner id type - in either position, under any name, other parameters such"
        + " as a cancellation token allowed - and returns a type that involves the aggregate: the aggregate"
        + " itself, nullable, in a Task or ValueTask or another generic container. A method that answers only"
        + " yes or no does not count. Where the id type cannot be resolved, any parameter assignable to the id"
        + " role stands for it. Whether a use case calls the scoped lookup or the unscoped FindByIdAsync is not"
        + " checked; a generic intermediate port whose parameters are generic parameters is not seen through."
        + " An empty selection passes.")
```
