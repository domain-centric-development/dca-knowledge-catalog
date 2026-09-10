---
type: Reference
title: "Use cases that publish domain events must have a transaction boundary — C# helper OperationPolicy"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#c-helper-operationpolicy"
---

[Full node and context](/rule/usecase/dca-use-012.md#c-helper-operationpolicy). This is an evidence excerpt; retain the parent selection and caveats.

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
                // Property accessors (auto or computed) are reported once, as their property, below.
                if (method.IsSpecialName && (method.Name.StartsWith("get_", StringComparison.Ordinal) || method.Name.StartsWith("set_", StringComparison.Ordinal))) continue;
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
