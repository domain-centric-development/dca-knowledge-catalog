---
type: Reference
title: "Query use cases must not write or publish — C# expression"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-019.md#c-expression"
---

[Full node and context](/rule/usecase/dca-use-019.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
        "DCA-USE-019",
        "Query use cases must not write or publish",
        "A read never creates. A query has no side effect: it does not create, save or publish, and when"
            + " nothing exists it answers none. Find-or-create is a command, called where the caller is about"
            + " to change state; a caller that only shows what exists asks the query",
        arch =>
        {
            var violations = new List<string>();
            var markers = arch.Layout.Markers;
            foreach (var type in arch.Types.Where(t => OperationPolicy.Operation(t, arch)).OrderBy(t => t.FullName, StringComparer.Ordinal))
            {
                var runtime = arch.RuntimeType(type)!;
                if (!InputTypesOf(runtime, markers).Any(t => markers.Is("Query", t)))
                {
                    continue;
                }

                foreach (var unit in new IntraClassCalls(runtime).Units)
                {
                    foreach (var call in IntraClassCalls.IlCalls(unit))
                    {
                        var effect = WriteEffectOf(call, markers);
                        if (effect is not null)
                        {
                            violations.Add($"{type.FullName}.{IntraClassCalls.DisplayName(unit)} takes a query and {effect}"
                                + $" ({call.DeclaringType!.Name.Split('`')[0]}.{call.Name})");
                        }
                    }
                }
            }

            DcaRule.Fail(
                "Query use cases must not write or publish",
                violations.Distinct().ToList(),
                "answer none when nothing exists, and move the write into a command use case the caller runs where it is about to change state");
        })
    .Experimental()
    .Selecting(
        "Concrete non-nested application operations selected by IInputPort marker or configured use-case"
            + " suffix, with loadable runtime types, whose input the configured query role recognises (by default a"
            + " simple name ending with Query): the input type argument of an"
            + " implemented IUseCase<TInput, TOutput>, or a parameter of a method that implements an"
            + " IInputPort interface.")
    .Checking(
        "No method of the class - async state machines and lambdas included - calls a repository write"
            + " (IRepository.SaveAsync or DeleteByIdAsync, or a method of a repository or store port whose"
            + " name starts with Save, Delete, Remove, Add, Insert, Update, Upsert, Put, Store, Write,"
            + " Create, Append, Archive, Purge, Clear, Set or Mark), or any method of the domain-event or"
            + " integration-event publisher. Only the class's own calls are read: a write reached through"
            + " a helper class or a second port is not seen, and a store write under another verb passes."
            + " An empty selection passes.")
```
