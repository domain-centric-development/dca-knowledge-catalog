---
type: Reference
title: "Entities must not be instantiated directly from outside the aggregate — C# expression"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-005.md#c-expression"
---

[Full node and context](/rule/tactical/dca-tac-005.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-005",
    "Entities must not be instantiated directly from outside the aggregate",
    "Entities are created through their aggregate root so that the root can enforce its invariants",
    arch =>
    {
        var violations = new List<string>();
        var entities = NonRootEntities(arch).Select(e => arch.RuntimeType(e)).Where(t => t is not null).ToHashSet();
        foreach (var caller in arch.Types.Where(t => !t.IsCompilerGenerated))
        {
            var runtime = arch.RuntimeType(caller);
            if (runtime is null) continue;
            foreach (var target in new IntraClassCalls(runtime).Units.SelectMany(IntraClassCalls.IlCalls)
                .OfType<ConstructorInfo>().Where(c => entities.Contains(c.DeclaringType)).Distinct())
            {
                var entity = target.DeclaringType!;
                var root = arch.ModuleRootOf(entity.Namespace ?? "");
                var domain = root + "." + arch.Layout.DomainSegment;
                var ns = runtime.Namespace ?? "";
                var sameDomain = root is not null && root == arch.ModuleRootOf(ns)
                    && (ns == domain || ns.StartsWith(domain + ".", StringComparison.Ordinal));
                var role = typeof(IAggregateRoot).IsAssignableFrom(runtime) || typeof(IEntity).IsAssignableFrom(runtime)
                    || typeof(IFactory).IsAssignableFrom(runtime);
                if (runtime != entity && !(sameDomain && role))
                    violations.Add($"{runtime.FullName} constructs entity {entity.FullName} outside its domain construction boundary");
            }
        }
        DcaRule.Fail("Entities are constructed by their own domain aggregate, entity or factory.", violations);
    })
    .Selecting("Constructor calls to non-root IEntity types, records and structs included.")
    .Checking("The caller is the entity itself or an IAggregateRoot, IEntity or IFactory in the same context domain layer. Same aggregate ownership is not decidable: another aggregate in that context passes and needs review. Reconstitution goes through an aggregate or factory; reflection is not inspected.")
```
