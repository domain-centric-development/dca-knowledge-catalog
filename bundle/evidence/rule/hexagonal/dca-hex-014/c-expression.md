---
type: Reference
title: "GET handlers must not drive an input port that takes a command — C# expression"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#c-expression"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
        "DCA-HEX-014",
        "GET handlers must not drive an input port that takes a command",
        "A state-changing use case is reached only by an unsafe HTTP method, never by GET; links do not"
            + " create state. Prefetching, crawlers and cross-site navigation follow a link without asking,"
            + " and would otherwise trigger the change. A handler that names no HTTP method answers GET as well",
        arch =>
        {
            var roles = arch.Layout.FrameworkTypes;
            var incoming = DcaLayout.AnyOf(arch.AllIncomingAdapterPatterns());
            var violations = new List<string>();
            foreach (var adapter in arch.Classes.Where(c => !c.IsCompilerGenerated && InNamespace(c, incoming)).OrderBy(c => c.FullName, StringComparer.Ordinal))
            {
                var runtime = arch.RuntimeType(adapter);
                if (runtime is null)
                {
                    continue;
                }

                var byPrefix = IsController(adapter, arch.Layout);
                var routesActions = byPrefix && !(FrameworkTypes.IsSet(roles.PageModelBase) && adapter.IsAssignableTo(roles.PageModelBase));
                var graph = new IntraClassCalls(runtime);
                foreach (var handler in graph.Units.OfType<MethodInfo>()
                    .Where(m => m.DeclaringType == runtime && IsGetHandler(m, roles, byPrefix, routesActions)))
                {
                    foreach (var call in graph.ReachableFrom(handler).SelectMany(IntraClassCalls.IlCalls))
                    {
                        var command = CommandTakenBy(call, arch.Layout.Markers);
                        if (command is not null)
                        {
                            violations.Add($"{adapter.FullName}.{handler.Name} handles GET and drives"
                                + $" {call.DeclaringType!.Name.Split('`')[0]}.{call.Name} with the command {command}");
                        }
                    }
                }
            }

            DcaRule.Fail(
                "GET handlers must not drive an input port that takes a command",
                violations.Distinct().ToList(),
                "map the handler to POST, PUT or DELETE, or let the GET handler ask a query");
        })
    .Experimental()
    .Selecting(
        "Methods declared by classes in <module>.Adapter.Incoming of every module root that carry an"
            + " attribute of the configured GET-mapping role (derived attributes included) - for an entry"
            + " that names a property value, an attribute of that type whose property holds the value (a"
            + " general verb attribute restricted to GET); for an entry that names a property without a value,"
            + " a public instance method of a class recognised as a controller, not a page model, that"
            + " carries no attribute of the configured non-action role and none of whose attributes of that"
            + " type holds a value (an action that names no HTTP method) - or - on a"
            + " class recognised as a controller or page model - whose name starts with a configured"
            + " GET-handler prefix. A mapping that names no HTTP method answers every method, GET included,"
            + " and counts as a GET handler. Both roles are empty in the None() preset, which then selects"
            + " nothing.")
    .Checking(
        "No method reached from the handler through calls within the class - async state machines and"
            + " lambdas included - calls a method of a type assignable to IInputPort that takes a"
            + " parameter whose type name ends in Command. A mapping that names no HTTP method is checked like"
            + " a GET handler. A handler mapped by a routing call rather than"
            + " by an attribute or a name is not seen, and a command reached through a second class is"
            + " not followed. An empty selection passes.")
```
