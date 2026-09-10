---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — C# helper EventFreeAggregate"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#c-helper-eventfreeaggregate"
---

[Full node and context](/rule/usecase/dca-use-009.md#c-helper-eventfreeaggregate). This is an evidence excerpt; retain the parent selection and caveats.

### C# helper EventFreeAggregate

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using DomainCentric.BuildingBlocks.Ddd.Tactical;
using DomainCentric.BuildingBlocks.Hexagonal.Ports.Out;

namespace DomainCentric.ArchRules.Rules;

internal static class EventFreeAggregate
{
    internal static bool Repository(MethodBase save, DcaArchitecture arch)
    {
        var owner = save.DeclaringType;
        if (owner is null) return false;
        var repository = owner.GetInterfaces().Append(owner).FirstOrDefault(t => t.IsGenericType && t.GetGenericTypeDefinition() == typeof(IRepository<,>));
        var aggregate = repository?.GetGenericArguments()[0];
        if (aggregate is null || aggregate.IsGenericParameter || aggregate.IsInterface) return false;
        var scanned = arch.Types.Select(arch.RuntimeType).Where(t => t is not null).Cast<Type>().ToHashSet();
        if (!scanned.Contains(aggregate)) return false;
        for (var current = aggregate; current is not null && !Platform(current); current = current.BaseType)
            if (!scanned.Contains(current) || !NoRegistration(current, scanned, new HashSet<Type>())) return false;
        return true;
    }

    private static bool NoRegistration(Type type, HashSet<Type> scanned, HashSet<Type> visited)
    {
        if (!visited.Add(type)) return true;
        foreach (var call in new IntraClassCalls(type).Units.SelectMany(IntraClassCalls.IlCalls))
        {
            var owner = call.DeclaringType;
            if (owner is null) return false;
            if (call.Name == "RegisterEvent" && typeof(IAggregateRoot).IsAssignableFrom(owner)) return false;
            if (Platform(owner)) continue;
            if (!scanned.Contains(owner) || !NoRegistration(owner, scanned, visited)) return false;
        }
        return true;
    }

    private static bool Platform(Type type) => (type.FullName ?? "").StartsWith("System.", StringComparison.Ordinal)
        || (type.FullName ?? "").StartsWith("DomainCentric.BuildingBlocks.", StringComparison.Ordinal);
}
```
