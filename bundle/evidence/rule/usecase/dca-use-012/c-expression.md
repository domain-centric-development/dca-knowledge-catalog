---
type: Reference
title: "Use cases that save an aggregate or publish domain events must have a transaction boundary — C# expression"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#c-expression"
---

[Full node and context](/rule/usecase/dca-use-012.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check("DCA-USE-012", "Use cases that save an aggregate or publish domain events must have a transaction boundary",
        "The use case owns the unit of work. Saving an aggregate is one business fact, yet the repository may write it as"
        + " several statements - an aggregate of entities and value objects often spans several tables - and a repository"
        + " adapter draws no boundary of its own; without one, a failure between the statements leaves half an aggregate"
        + " behind. Publishing adds a second effect that must fall with the save: integration-event capture joins the"
        + " modeled transaction, and publication outside a transaction cannot rely on commit semantics. The boundary is"
        + " either the configured transactional attribute (on the class or the executing method) or an explicit"
        + " ITransactionBoundary.InTransactionAsync(...) around load, mutate, save and publish. Checked per entry path,"
        + " following calls within the class: from every entry point - a method callable from outside the class, or one"
        + " nothing in the class calls - no route down to the saving, deleting or publishing method may be free of an"
        + " attribute or a boundary; a covered caller does not cover another route to the same helper, and a boundary on"
        + " one route does not cover a second route",
        arch => {
            var violations = new List<string>();
            foreach (var type in arch.Types.Where(t => OperationPolicy.Operation(t, arch))) {
                var runtime = arch.RuntimeType(type)!;
                var graph = new IntraClassCalls(runtime);
                foreach (var unit in graph.Units) {
                    var effect = TransactionalEffectOf(unit);
                    if (effect is null) continue;
                    foreach (var entry in graph.EntryPointsOf(unit)) {
                        if (!Transactional(runtime, layout.FrameworkTypes.TransactionalAttribute)
                            && graph.ReachableThrough(entry, u => !Transactional(u, layout.FrameworkTypes.TransactionalAttribute) && !CallsBoundary(u)).Contains(unit))
                            violations.Add($"{type.FullName}.{IntraClassCalls.PathName(entry, unit)} {effect} without transaction coverage on every entry path");
                    }
                }
            }
            DcaRule.Fail("Use cases that save, delete or publish require transaction coverage", violations.Distinct().ToList());
        })
    .Selecting("Concrete application operations selected by IInputPort marker or suffix with loadable runtime types, including closure and async units.")
    .Checking("Every entry path to a unit calling IRepository.SaveAsync, IRepository.DeleteByIdAsync or an IDomainEventPublisher crosses a unit calling ITransactionBoundary.InTransactionAsync (including its extension overloads) or carrying the configured TransactionalAttribute; a type-level attribute covers all paths. A use case that neither saves, deletes nor publishes (a query, a Store write) is selected but has nothing to check and passes. Static limit: a boundary call in the same unit passes even when the save or publication follows an empty boundary block. Runtime rollback containment must be tested separately.")
```
