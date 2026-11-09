---
type: Reference
title: "Outgoing adapters must not call state-changing methods of aggregate roots — C# expression"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-021.md#c-expression"
---

[Full node and context](/rule/hexagonal/dca-hex-021.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
        "DCA-HEX-021",
        "Outgoing adapters must not call state-changing methods of aggregate roots",
        "An aggregate's state changes through its own methods, each with its guard and its event, and the"
            + " application decides when one runs. An outgoing adapter that calls one changes the aggregate on a"
            + " path no use case owns, outside the transaction the use case draws and without the events it"
            + " publishes. The adapter stores and loads what the aggregate holds",
        arch =>
        {
            var markers = arch.Layout.Markers;
            var vocabularyBase = markers.AggregateRoot.Contains('.')
                ? markers.AggregateRoot[..markers.AggregateRoot.LastIndexOf('.')]
                : "";
            var violations = new SortedSet<string>(StringComparer.Ordinal);
            var verdicts = new Dictionary<MethodBase, string?>();
            foreach (var adapter in arch.RuntimeTypes()
                .Where(t => !t.IsNested && arch.InLayer(t, DcaLayout.Layer.OutgoingAdapter)))
            {
                foreach (var unit in new IntraClassCalls(adapter).Units)
                {
                    foreach (var target in IntraClassCalls.IlCalls(unit))
                    {
                        if (target.DeclaringType is not { } owner || !markers.Is(nameof(DcaMarkers.AggregateRoot), owner)
                            || owner.Namespace == vocabularyBase)
                        {
                            continue;
                        }

                        if (!verdicts.TryGetValue(target, out var change))
                        {
                            verdicts[target] = change = StateChangeOf(target);
                        }

                        if (change is not null)
                        {
                            violations.Add($"{adapter.FullName}.{IntraClassCalls.DisplayName(unit)} calls"
                                + $" {owner.Name.Split('`')[0]}.{target.Name} - {change}");
                        }
                    }
                }
            }

            DcaRule.Fail(
                "Outgoing adapters must not call state-changing methods of aggregate roots",
                violations.ToList(),
                "let a use case load the aggregate, call the method and save it; the adapter only stores what the"
                + " aggregate holds");
        })
    .Experimental()
    .Selecting(
        "Every non-nested type in the outgoing adapter layer of every module root - by default"
            + " <Module>.Adapter.Outgoing - with its runtime type in the loaded assemblies, together with its nested,"
            + " async state-machine and closure types, and the calls their IL makes. Nothing is selected when no type"
            + " carries the aggregate-root role.")
    .Checking(
        "No code unit calls a method of a type carrying the aggregate-root role that changes its state - a"
            + " non-static method that returns void, Task or ValueTask without a result, a property setter, or one"
            + " that sets a field of its own class; the called method is read where it is declared, methods"
            + " inherited from the root's base classes included. An init accessor runs only while the object is"
            + " built and passes. Static methods - factories, reconstitution - and methods that return a value"
            + " without setting a field are queries and pass. A method declared by a type in the namespace of the"
            + " aggregate-root role's own marker - the vocabulary's base, such as its domain-event bookkeeping that a"
            + " publisher clears after publishing - is not the aggregate's behaviour and passes. A change made by"
            + " writing to storage directly, past the aggregate, is not a call and is not seen. An"
            + " empty selection passes.")
```
