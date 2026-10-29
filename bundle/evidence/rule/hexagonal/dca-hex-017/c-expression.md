---
type: Reference
title: "Event listeners that drive an input port must run after the commit in their own transaction — C# expression"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-017.md#c-expression"
---

[Full node and context](/rule/hexagonal/dca-hex-017.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
        "DCA-HEX-017",
        "Event listeners that drive an input port must run after the commit in their own transaction",
        "A reaction to an event changes state or performs an external effect through a use case. Run inside"
            + " the transaction that raised the event, it changes a second aggregate in the first one's"
            + " transaction, a failure in the reaction rolls back the fact that caused it, and a retry of the"
            + " request runs the reaction again. A listener that only translates or measures calls output ports"
            + " and may run in that transaction",
        arch =>
        {
            var roles = arch.Layout.FrameworkTypes;
            var violations = new List<string>();
            if (roles.EventListenerTypes.Count > 0 && roles.TransactionalEventListenerTypes.Count > 0)
            {
                foreach (var listener in arch.Classes
                    .Where(c => !c.IsCompilerGenerated && roles.EventListenerTypes.Any(t => c.IsAssignableTo(t)))
                    .OrderBy(c => c.FullName, StringComparer.Ordinal))
                {
                    if (roles.TransactionalEventListenerTypes.Any(t => listener.IsAssignableTo(t)))
                    {
                        continue;
                    }

                    var runtime = arch.RuntimeType(listener);
                    if (runtime is null)
                    {
                        continue;
                    }

                    var ports = new IntraClassCalls(runtime).Units
                        .SelectMany(IntraClassCalls.IlCalls)
                        .Where(call => call.DeclaringType is not null && arch.Layout.Markers.Is(nameof(DcaMarkers.InputPort), call.DeclaringType))
                        .Select(call => $"{call.DeclaringType!.Name.Split('`')[0]}.{call.Name}")
                        .Distinct()
                        .OrderBy(name => name, StringComparer.Ordinal)
                        .ToList();
                    if (ports.Count > 0)
                    {
                        violations.Add($"{listener.FullName} drives {string.Join(", ", ports)} inside the transaction that raised the event");
                    }
                }
            }

            DcaRule.Fail(
                "Event listeners that drive an input port must run after the commit in their own transaction",
                violations,
                "deliver the reaction after the commit in its own transaction - a transactional listener backed"
                    + " by an outbox - or let the listener call only output ports");
        })
    .Experimental()
    .Selecting(
        "Classes of every module root assignable to a type of the configured event-listener role and to none"
            + " of the configured transactional-event-listener role. With either role empty - both are empty in"
            + " every preset - nothing is selected and the rule passes.")
    .Checking(
        "No method of such a class - async state machines and lambdas included - calls a method of a type"
            + " assignable to IInputPort. The rule reads the listener's kind, not whether an outbox backs it; an"
            + " input port reached through a second class is not followed. An empty selection passes.")
```
