---
type: Rule
id: DCA-NET-002
title: Port methods returning Task must end with Async
rule: The Async suffix is the .NET convention that tells callers a method is awaitable; ports are the contract other layers program against.
constraint: Port methods returning Task must end with Async.
selects: Interfaces under the root namespace that are assignable to IInputPort or IOutputPort and whose runtime type is in the loaded assemblies.
checks: "Every public method declared on the interface itself (inherited members, property accessors and operators excluded) returns Task, Task<T>, ValueTask or ValueTask<T> exactly when its name ends with Async. Both directions are reported: an awaitable method without the suffix and a suffixed method that returns something else. An empty selection passes."
enforced_by: "DotnetRules#DCA-NET-002"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---

## Selection

Interfaces under the root namespace that are assignable to IInputPort or IOutputPort and whose runtime type is in the loaded assemblies.

## Check

Every public method declared on the interface itself (inherited members, property accessors and operators excluded) returns Task, Task<T>, ValueTask or ValueTask<T> exactly when its name ends with Async. Both directions are reported: an awaitable method without the suffix and a suffixed method that returns something else. An empty selection passes.

### C# expression

```csharp
DcaRule.Check(
        "DCA-NET-002",
        "Port methods returning Task must end with Async",
        "The Async suffix is the .NET convention that tells callers a method is awaitable; ports are the contract other layers program against",
        arch =>
        {
            var violations = new List<string>();
            foreach (var port in arch.Interfaces)
            {
                var runtime = arch.RuntimeType(port);
                if (runtime is null || !(IsPort(runtime, arch.Layout.Markers.InputPort) || IsPort(runtime, arch.Layout.Markers.OutputPort)))
                {
                    continue;
                }

                foreach (var method in DeclaredMethods(runtime))
                {
                    var awaitable = IsAsyncReturnType(method.ReturnType);
                    var suffixed = method.Name.EndsWith("Async", StringComparison.Ordinal);
                    if (awaitable && !suffixed)
                    {
                        violations.Add($"{runtime.FullName}.{method.Name} returns {method.ReturnType.Name} but does not end with Async");
                    }
                    else if (!awaitable && suffixed)
                    {
                        violations.Add($"{runtime.FullName}.{method.Name} ends with Async but returns {method.ReturnType.Name}");
                    }
                }
            }

            DcaRule.Fail(
                "Port methods returning Task must end with Async\nbecause the Async suffix tells callers a method is awaitable",
                violations,
                "Name every Task/ValueTask-returning port method *Async and make every *Async method return Task or ValueTask.");
        })
    .Selecting(
        "Interfaces under the root namespace that are assignable to IInputPort or"
            + " IOutputPort and whose runtime type is in the loaded assemblies.")
    .Checking(
        "Every public method declared on the interface itself (inherited members, property"
            + " accessors and operators excluded) returns Task, Task<T>, ValueTask or ValueTask<T>"
            + " exactly when its name ends with Async. Both directions are reported: an awaitable"
            + " method without the suffix and a suffixed method that returns something else. An"
            + " empty selection passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
