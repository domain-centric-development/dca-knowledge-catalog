---
type: Reference
title: "Declaratively transactional use cases must not call remote-capable output ports — C# expression"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-013.md#c-expression"
---

[Full node and context](/rule/usecase/dca-use-013.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check("DCA-USE-013", "Declaratively transactional use cases must not call remote-capable output ports",
        "A declaratively transactional use case holds a database connection for its whole run. Calling an output port"
        + " that may leave the process (another context's API, a payment provider, a mail gateway) inside it blocks"
        + " that connection for the remote round trip; under load the pool runs dry, and a rollback cannot undo the"
        + " remote effect. Awaiting the call does not help: the thread is released, the transaction and its connection"
        + " are not. Only transactional resources belong inside the boundary: IRepository, IStore,"
        + " IDomainEventPublisher, IIntegrationEventPublisher. Everything else is called before the transaction - draw"
        + " the boundary by hand with ITransactionBoundary.InTransactionAsync(...) - or after it, as a reaction to an"
        + " integration event",
        arch => {
            var attribute = layout.FrameworkTypes.TransactionalAttribute;
            var violations = new List<string>();
            if (FrameworkTypes.IsSet(attribute)) {
                foreach (var type in arch.Types.Where(t => OperationPolicy.Operation(t, arch))) {
                    var runtime = arch.RuntimeType(type)!;
                    var graph = new IntraClassCalls(runtime);
                    foreach (var unit in graph.Units) {
                        if (!Transactional(runtime, attribute)
                            && !graph.EntryPointsOf(unit).Any(entry =>
                                Transactional(entry, attribute)
                                || !graph.ReachableThrough(entry, u => !Transactional(u, attribute)).Contains(unit)))
                            continue;
                        var remotePorts = RemotePortsCalledBy(unit, arch).ToList();
                        if (remotePorts.Count == 0) continue;
                        violations.Add(
                            $"{type.FullName}.{IntraClassCalls.DisplayName(unit)} runs under {attribute} and calls "
                            + string.Join(", ", remotePorts)
                            + " inside the transaction - call it before, or draw the boundary with"
                            + " ITransactionBoundary.InTransactionAsync(...)");
                    }
                }
            }

            DcaRule.Fail(
                "Declaratively transactional use cases must not call remote-capable output ports",
                violations.Distinct().ToList(),
                "call the remote port before the transaction, or draw the boundary explicitly with"
                + " ITransactionBoundary.InTransactionAsync(...) around the transactional part only");
        })
    .Selecting("Concrete application operations selected by IInputPort marker or configured use-case suffix, with loadable runtime types. Nothing at all while no transactional attribute is configured, which is the default: neither .NET preset names one, because ASP.NET Core has no ambient transaction attribute.")
    .Checking("Every code unit that runs under the configured transactional attribute - on the class, on itself, or on an entry point that reaches it within the class - calls no output port other than IRepository, IStore, IDomainEventPublisher or IIntegrationEventPublisher. A use case without such an attribute (an explicit ITransactionBoundary, or none) is selected but never reported, and with no attribute configured nothing is ever reported - the rule then carries the id without checking anything, as the Java twin does where no framework annotation is on the class path. What happens inside an InTransactionAsync block is not inspected; the explicit boundary is the developer's own and its extent is visible at the call site.")
```
