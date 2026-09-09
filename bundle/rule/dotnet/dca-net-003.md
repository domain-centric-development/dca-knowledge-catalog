---
type: Rule
id: DCA-NET-003
title: "Use cases implement IUseCase<TIn,TOut>.ExecuteAsync(input, CancellationToken) returning Task<T>"
rule: The generic asynchronous input contract supports host cancellation.
constraint: "Use cases implement IUseCase<TIn,TOut>.ExecuteAsync(input, CancellationToken) returning Task<T>."
selects: "Concrete application operations selected by marker or suffix, plus concrete IUseCase<TIn,TOut> implementations anywhere under scan, with loadable runtime types."
checks: "An IUseCase<TIn,TOut> interface map supplies ExecuteAsync(input, CancellationToken) returning Task<T>. Explicit, inherited and ordinary implementations pass. A plain Task method without the generic contract fails; other public members are checked by USE-017, not counted here."
enforced_by: "DotnetRules#DCA-NET-003"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---

## Selection

Concrete application operations selected by marker or suffix, plus concrete IUseCase<TIn,TOut> implementations anywhere under scan, with loadable runtime types.

## Check

An IUseCase<TIn,TOut> interface map supplies ExecuteAsync(input, CancellationToken) returning Task<T>. Explicit, inherited and ordinary implementations pass. A plain Task method without the generic contract fails; other public members are checked by USE-017, not counted here.

### C# expression

```csharp
DcaRule.Check("DCA-NET-003", "Use cases implement IUseCase<TIn,TOut>.ExecuteAsync(input, CancellationToken) returning Task<T>",
        "The generic asynchronous input contract supports host cancellation",
        arch => {
            var violations = new List<string>();
            foreach (var type in arch.Classes) {
                var runtime = arch.RuntimeType(type);
                if (runtime is null || runtime.IsAbstract || !(OperationPolicy.Operation(type, arch) || ImplementsUseCase(runtime))) continue;
                var contracts = runtime.GetInterfaces().Where(i => i.IsGenericType && i.GetGenericTypeDefinition() == typeof(IUseCase<,>)).ToArray();
                if (contracts.Length == 0) violations.Add($"{type.FullName} must implement IUseCase<TIn,TOut>; a plain Task ExecuteAsync does not satisfy the contract");
                foreach (var contract in contracts) {
                    var map = runtime.GetInterfaceMap(contract);
                    foreach (var method in map.TargetMethods) {
                        var parameters = method.GetParameters();
                        if (!method.ReturnType.IsGenericType || method.ReturnType.GetGenericTypeDefinition() != typeof(Task<>)
                            || parameters.Length != 2 || parameters[1].ParameterType != typeof(CancellationToken))
                            violations.Add($"{type.FullName}.{method.Name} must accept input and CancellationToken and return Task<T>");
                    }
                }
            }
            DcaRule.Fail("Use cases implement the generic asynchronous input contract", violations);
        })
    .Selecting("Concrete application operations selected by marker or suffix, plus concrete IUseCase<TIn,TOut> implementations anywhere under scan, with loadable runtime types.")
    .Checking("An IUseCase<TIn,TOut> interface map supplies ExecuteAsync(input, CancellationToken) returning Task<T>. Explicit, inherited and ordinary implementations pass. A plain Task method without the generic contract fails; other public members are checked by USE-017, not counted here.")
```

### C# helper OperationPolicy

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using ArchUnitNET.Domain;
using ArchUnitNET.Domain.Extensions;
using DomainCentric.BuildingBlocks.Hexagonal.Ports.In;

namespace DomainCentric.ArchRules.Rules;

internal static class OperationPolicy
{
    internal static bool Operation(IType type, DcaArchitecture arch) => type is Class { IsAbstract: false }
        && arch.RuntimeType(type) is { IsNested: false }
        && Regex.IsMatch(type.Namespace?.FullName ?? "", DcaLayout.AnyOf(arch.AllApplicationPatterns()))
        && (type.IsAssignableTo(typeof(IInputPort).FullName!) || type.Name.EndsWith(arch.Layout.UseCaseSuffix, StringComparison.Ordinal));

    internal static void Invocation(DcaArchitecture arch)
    {
        var violations = new List<string>();
        foreach (var caller in arch.Types.Where(t => Operation(t, arch)))
        {
            var runtime = arch.RuntimeType(caller)!;
            var own = runtime.GetInterfaces().SelectMany(t => new[] {t.FullName, t.IsGenericType ? t.GetGenericTypeDefinition().FullName : t.FullName}).ToHashSet();
            for (var parent = runtime; parent is not null; parent = parent.BaseType) own.Add(parent.FullName);
            Walk(caller, caller, arch, own, new HashSet<IType>(), new List<string>(), violations);
        }
        DcaRule.Fail("Use cases must not invoke other use cases", violations.Distinct().ToList());
    }

    private static void Walk(IType caller, IType current, DcaArchitecture arch, HashSet<string?> own,
        HashSet<IType> seen, List<string> via, List<string> violations)
    {
        if (!seen.Add(current)) return;
        foreach (var target in current.Dependencies.Select(d => d.Target).Distinct())
        {
            if (own.Contains(target.FullName)) continue;
            if (target.IsAssignableTo(typeof(IInputPort).FullName!) || Operation(target, arch))
                violations.Add($"{caller.FullName} -> {target.FullName}" + (via.Count == 0 ? "" : $" [via {string.Join(" -> ", via)}]"));
            else if (target is not Interface && Regex.IsMatch(target.Namespace?.FullName ?? "", DcaLayout.AnyOf(arch.AllApplicationPatterns()))
                && arch.ModuleRootOf(caller.Namespace.FullName) == arch.ModuleRootOf(target.Namespace?.FullName ?? ""))
                Walk(caller, target, arch, own, seen, via.Concat(new[] { target.FullName }).ToList(), violations);
        }
    }

    internal static void Surface(DcaArchitecture arch)
    {
        var violations = new List<string>();
        foreach (var type in arch.Types.Where(t => Operation(t, arch)))
        {
            var runtime = arch.RuntimeType(type)!;
            var methods = runtime.GetInterfaces().Where(i => typeof(IInputPort).IsAssignableFrom(i))
                .SelectMany(i => runtime.GetInterfaceMap(i).TargetMethods).ToHashSet();
            foreach (var method in runtime.GetMethods(BindingFlags.Public | BindingFlags.Instance))
            {
                if (method.DeclaringType == typeof(object) || method.DeclaringType == typeof(ValueType)
                    || method.GetBaseDefinition().DeclaringType == typeof(object)
                    || method.IsDefined(typeof(CompilerGeneratedAttribute), false) || methods.Contains(method)) continue;
                // Auto-property accessors have CompilerGeneratedAttribute too; the property's public
                // surface is user-defined and must still belong to an input port.
                violations.Add($"{type.FullName} exposes {method} outside its input port");
            }
            foreach (var property in runtime.GetProperties(BindingFlags.Public | BindingFlags.Instance))
                foreach (var accessor in property.GetAccessors().Where(a => !methods.Contains(a)))
                    violations.Add($"{type.FullName} exposes property {property.Name} ({accessor.Name}) outside its input port");
        }
        DcaRule.Fail("Use cases expose no public operation outside their input port", violations.Distinct().ToList());
    }
}
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
