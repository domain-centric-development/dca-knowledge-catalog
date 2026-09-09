---
type: Rule
id: DCA-USE-016
title: Use cases must not invoke other use cases
rule: Ordinary operations do not coordinate other operations; coordination requires explicit transaction and failure semantics.
constraint: Use cases must not invoke other use cases.
selects: Concrete non-nested application classes selected by InputPort marker or configured use-case suffix.
checks: "Reports dependencies on another input port or operation, directly or transitively through same-module application helpers. Own interfaces and base classes are excluded. Messages start Caller -> Target [via Helper], so an anchored caller-side ignore permits configured coordinators without permitting calls to them. Reflection, container lookups and unrelated interfaces are not resolved; CYC-005 still checks coordinator cycles."
enforced_by: "UseCaseRules#DCA-USE-016"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use cases must not invoke other use cases

## Selection

Concrete non-nested application classes selected by InputPort marker or configured use-case suffix.

## Check

Reports dependencies on another input port or operation, directly or transitively through same-module application helpers. Own interfaces and base classes are excluded. Messages start Caller -> Target [via Helper], so an anchored caller-side ignore permits configured coordinators without permitting calls to them. Reflection, container lookups and unrelated interfaces are not resolved; CYC-005 still checks coordinator cycles.

## .NET reading

**Selection.** Concrete non-nested application operations selected by IInputPort marker or configured use-case suffix, with loadable runtime types.

**Check.** Reports dependencies on another input port or operation, directly or through same-module application helpers. Own interfaces/base classes are excluded. Messages start Caller -> Target [via Helper], permitting an anchored caller-side coordinator ignore without permitting calls to the coordinator. Reflection, container lookups and unrelated interfaces are not resolved. CYC-005 still checks cycles.

## Implementation

```java
DcaRule.check(
        "DCA-USE-016",
        "Use cases must not invoke other use cases",
        "Ordinary operations do not coordinate other operations; coordination requires explicit transaction and failure semantics",
        OperationPolicy::invocation)
    .selecting(
        "Concrete non-nested application classes selected by InputPort marker or configured use-case suffix.")
    .checking(
        "Reports dependencies on another input port or operation, directly or transitively through same-module application helpers. Own interfaces and base classes are excluded. Messages start Caller -> Target [via Helper], so an anchored caller-side ignore permits configured coordinators without permitting calls to them. Reflection, container lookups and unrelated interfaces are not resolved; CYC-005 still checks coordinator cycles.")
```
### C# expression

```csharp
DcaRule.Check("DCA-USE-016", "Use cases must not invoke other use cases",
        "Ordinary operations do not coordinate other operations; coordination requires explicit transaction and failure semantics", OperationPolicy.Invocation)
    .Selecting("Concrete non-nested application operations selected by IInputPort marker or configured use-case suffix, with loadable runtime types.")
    .Checking("Reports dependencies on another input port or operation, directly or through same-module application helpers. Own interfaces/base classes are excluded. Messages start Caller -> Target [via Helper], permitting an anchored caller-side coordinator ignore without permitting calls to the coordinator. Reflection, container lookups and unrelated interfaces are not resolved. CYC-005 still checks cycles.")
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

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
