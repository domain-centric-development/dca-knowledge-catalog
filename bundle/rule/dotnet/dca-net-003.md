---
type: Rule
id: DCA-NET-003
title: The use-case contract takes an input and a CancellationToken and answers with a Task
rule: "A use case orchestrates output ports — persistence, messaging, remote systems — which are I/O-bound in .NET, so its contract is awaitable; and a host that shuts down, a cancelled request or an expired deadline must be able to stop the work, which needs a CancellationToken on the contract itself. A synchronous or non-cancellable use-case contract blocks a thread pool thread and cannot be stopped."
constraint: The use-case contract takes an input and a CancellationToken and answers with a Task.
selects: "Concrete classes under scan with loadable runtime types that implement the configured use-case role, directly, inherited or explicitly. A class that implements no such contract is not selected — which name it gives its own operations is not this rule's subject."
checks: "Every operation the use-case contract maps onto takes the input and a CancellationToken and returns Task<T>; explicit, inherited and ordinary implementations pass. With the library's own vocabulary the C# compiler already enforces the signature of IUseCase<TIn,TOut>, so the rule has something to report only where a project points the use-case role at a contract of its own. Whether a class exposes public members beyond the contract is DCA-USE-017's subject, not this one's."
enforced_by: "DotnetRules#DCA-NET-003"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---

## Selection

Concrete classes under scan with loadable runtime types that implement the configured use-case role, directly, inherited or explicitly. A class that implements no such contract is not selected — which name it gives its own operations is not this rule's subject.

## Check

Every operation the use-case contract maps onto takes the input and a CancellationToken and returns Task<T>; explicit, inherited and ordinary implementations pass. With the library's own vocabulary the C# compiler already enforces the signature of IUseCase<TIn,TOut>, so the rule has something to report only where a project points the use-case role at a contract of its own. Whether a class exposes public members beyond the contract is DCA-USE-017's subject, not this one's.

### C# expression

```csharp
DcaRule.Check("DCA-NET-003", "The use-case contract takes an input and a CancellationToken and answers with a Task",
        "A use case orchestrates output ports — persistence, messaging, remote systems — which are I/O-bound in .NET, "
        + "so its contract is awaitable; and a host that shuts down, a cancelled request or an expired deadline must be "
        + "able to stop the work, which needs a CancellationToken on the contract itself. A synchronous or "
        + "non-cancellable use-case contract blocks a thread pool thread and cannot be stopped",
        arch => {
            var violations = new List<string>();
            foreach (var type in arch.Classes) {
                var runtime = arch.RuntimeType(type);
                if (runtime is null || runtime.IsAbstract) continue;
                foreach (var contract in runtime.GetInterfaces().Where(i => DcaMarkers.CarriesRole(i, arch.Layout.Markers.UseCase))) {
                    var map = runtime.GetInterfaceMap(contract);
                    foreach (var method in map.TargetMethods) {
                        var parameters = method.GetParameters();
                        if (!method.ReturnType.IsGenericType || method.ReturnType.GetGenericTypeDefinition() != typeof(Task<>)
                            || parameters.Length != 2 || parameters[1].ParameterType != typeof(CancellationToken))
                            violations.Add($"{type.FullName}.{method.Name} must accept input and CancellationToken and return Task<T>");
                    }
                }
            }
            DcaRule.Fail(
                "The use-case contract takes an input and a CancellationToken and answers with a Task",
                violations,
                "declare the operation as Task<TOutput> <Name>(TInput input, CancellationToken cancellationToken)");
        })
    .Selecting("Concrete classes under scan with loadable runtime types that implement the configured use-case role, directly, inherited or explicitly. A class that implements no such contract is not selected — which name it gives its own operations is not this rule's subject.")
    .Checking("Every operation the use-case contract maps onto takes the input and a CancellationToken and returns Task<T>; explicit, inherited and ordinary implementations pass. With the library's own vocabulary the C# compiler already enforces the signature of IUseCase<TIn,TOut>, so the rule has something to report only where a project points the use-case role at a contract of its own. Whether a class exposes public members beyond the contract is DCA-USE-017's subject, not this one's.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
