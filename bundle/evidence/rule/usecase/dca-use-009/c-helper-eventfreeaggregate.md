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
        var markers = arch.Layout.Markers;
        var owner = save.DeclaringType;
        if (owner is null) return false;
        var repository = owner.GetInterfaces().Append(owner).FirstOrDefault(t => t.IsGenericType && DcaMarkers.IsRole(t.GetGenericTypeDefinition(), markers.Repository));
        var aggregate = repository?.GetGenericArguments()[0];
        if (aggregate is null || aggregate.IsGenericParameter || aggregate.IsInterface) return false;
        var scanned = arch.Types.Select(arch.RuntimeType).Where(t => t is not null).Cast<Type>().ToHashSet();
        if (!scanned.Contains(aggregate)) return false;
        var hierarchy = new HashSet<Type>();
        for (var current = aggregate; current is not null && !Platform(current, markers); current = current.BaseType)
        {
            if (!scanned.Contains(current) || !NoRegistration(current, scanned, new HashSet<Type>(), markers)) return false;
            hierarchy.Add(current);
        }

        return NoExternalRegistration(hierarchy, scanned, markers);
    }

    /// <summary>
    /// A type outside the aggregate's hierarchy that registers an event on it — a neighbouring class
    /// reaching the protected method — is invisible from the aggregate's own code units, so every
    /// scanned type is inspected. The Java twin reads the receiver of the call; IL names the
    /// <em>declaring</em> type instead (the inherited <c>RegisterEvent</c> of the marker's base
    /// class), so the receiver is approximated: a registering type disables the exemption when it
    /// also references a type of the hierarchy. Conservative in the right direction — it exempts
    /// less, never more.
    /// </summary>
    private static bool NoExternalRegistration(HashSet<Type> hierarchy, HashSet<Type> scanned, DcaMarkers markers)
    {
        foreach (var type in scanned)
        {
            if (hierarchy.Contains(type)) continue;
            var registers = new IntraClassCalls(type).Units
                .SelectMany(IntraClassCalls.IlCalls)
                .Any(call => call.Name == "RegisterEvent"
                    && call.DeclaringType is { } owner
                    && DcaMarkers.CarriesRole(owner, markers.AggregateRoot));
            if (registers && References(type, hierarchy))
            {
                return false;
            }
        }

        return true;
    }

    /// <summary>Whether the type names any of the given types in its members or in what it calls.</summary>
    private static bool References(Type type, HashSet<Type> hierarchy)
    {
        const BindingFlags flags = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance
            | BindingFlags.Static | BindingFlags.DeclaredOnly;
        foreach (var nested in type.GetNestedTypes(flags).Append(type))
        {
            if (nested.GetFields(flags).Any(f => hierarchy.Contains(f.FieldType))
                || nested.GetProperties(flags).Any(p => hierarchy.Contains(p.PropertyType)))
            {
                return true;
            }

            foreach (var method in nested.GetMethods(flags).Cast<MethodBase>().Concat(nested.GetConstructors(flags)))
            {
                if (method.GetParameters().Any(parameter => hierarchy.Contains(parameter.ParameterType)))
                {
                    return true;
                }

                if (IntraClassCalls.IlCalls(method).Any(call => call.DeclaringType is { } owner && hierarchy.Contains(owner)))
                {
                    return true;
                }
            }
        }

        return false;
    }

    private static bool NoRegistration(Type type, HashSet<Type> scanned, HashSet<Type> visited, DcaMarkers markers)
    {
        if (!visited.Add(type)) return true;
        foreach (var call in new IntraClassCalls(type).Units.SelectMany(IntraClassCalls.IlCalls))
        {
            var owner = call.DeclaringType;
            if (owner is null) return false;
            if (call.Name == "RegisterEvent" && DcaMarkers.CarriesRole(owner, markers.AggregateRoot)) return false;
            if (Platform(owner, markers)) continue;
            if (!scanned.Contains(owner) || !NoRegistration(owner, scanned, visited, markers)) return false;
        }
        return true;
    }

    /// <summary>
    /// A type the walk does not enter: the platform's own, or one of the vocabulary's — a marker and
    /// the base classes beside it register no event. Derived from the configured roles, so a project's
    /// own vocabulary stops the walk where the library's does; hard-wiring the building-blocks prefix
    /// would leave the exemption unreachable for such a project.
    /// </summary>
    private static bool Platform(Type type, DcaMarkers markers)
    {
        var name = type.FullName ?? "";
        return name.StartsWith("System.", StringComparison.Ordinal)
            || markers.DeclaresTypesIn(type.Namespace ?? "");
    }
}
```
