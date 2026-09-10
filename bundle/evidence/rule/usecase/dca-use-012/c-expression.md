---
type: Reference
title: "Use cases that publish domain events must have a transaction boundary — C# expression"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#c-expression"
---

[Full node and context](/rule/usecase/dca-use-012.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check("DCA-USE-012", "Use cases that publish domain events must have a transaction boundary",
        "Integration-event capture joins the modeled transaction; publication outside a transaction cannot rely on commit semantics",
        arch => {
            var violations = new List<string>();
            foreach (var type in arch.Types.Where(t => OperationPolicy.Operation(t, arch))) {
                var runtime = arch.RuntimeType(type)!;
                var graph = new IntraClassCalls(runtime);
                foreach (var publisher in graph.Units.Where(u => IntraClassCalls.IlCalls(u).Any(m => m.DeclaringType is not null && typeof(IDomainEventPublisher).IsAssignableFrom(m.DeclaringType)))) {
                    foreach (var entry in graph.EntryPointsOf(publisher)) {
                        if (!Transactional(runtime, layout.FrameworkTypes.TransactionalAttribute)
                            && graph.ReachableThrough(entry, u => !Transactional(u, layout.FrameworkTypes.TransactionalAttribute) && !CallsBoundary(u)).Contains(publisher))
                            violations.Add($"{type.FullName}.{IntraClassCalls.PathName(entry, publisher)} publishes without transaction coverage on every entry path");
                    }
                }
            }
            DcaRule.Fail("Publishing use cases require transaction coverage", violations.Distinct().ToList());
        })
    .Selecting("Concrete application operations selected by IInputPort marker or suffix with loadable runtime types, including closure and async units.")
    .Checking("Every entry path to an IDomainEventPublisher call crosses a unit calling ITransactionBoundary.InTransactionAsync (including its extension overloads) or carrying the configured TransactionalAttribute; a type-level attribute covers all paths. Static limit: a boundary call in the same unit passes even when publication follows an empty boundary block. Runtime rollback containment must be tested separately.")
```
