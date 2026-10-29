---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — C# expression"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#c-expression"
---

[Full node and context](/rule/tactical/dca-tac-025.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-025",
    "Domain types must not hold bare primitives, strings or time types",
    "A value with rules of its own - a postal code, a quantity, a status, a moment - is a value object;"
        + " held as a bare string, int, bool or DateTimeOffset its validation is repeated at every use or"
        + " missing. A value object with several components holds value objects too; only a wrapper - a"
        + " value of exactly one component - holds the primitive it wraps",
    arch =>
    {
        var markers = arch.Layout.Markers;
        var blockNamespaces = new[]
            {
                markers.AggregateRoot, markers.Entity, markers.Value, markers.Id, markers.DomainEvent,
                markers.IntegrationEvent, markers.DomainService, markers.Factory, markers.Specification,
                markers.DomainException, markers.OutputPort, markers.Repository, markers.Store,
            }
            .Where(m => m.Contains('.'))
            .Select(m => m[..m.LastIndexOf('.')])
            .ToHashSet(StringComparer.Ordinal);
        var violations = new List<string>();
        foreach (var type in arch.Types
            .Where(t => !t.IsCompilerGenerated && ResidesInAny(t, arch.AllDomainPatterns()))
            .OrderBy(t => t.FullName, StringComparer.Ordinal))
        {
            var runtime = arch.RuntimeType(type);
            if (runtime is null || IsWrapperValue(runtime, markers))
            {
                continue;
            }

            var exempt = BuildingBlockMemberNames(runtime, blockNamespaces);
            const BindingFlags declared = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance
                | BindingFlags.Static | BindingFlags.DeclaredOnly;
            var bare = new List<string>();
            foreach (var field in runtime.GetFields(declared & ~BindingFlags.Static))
            {
                if (field.IsDefined(typeof(System.Runtime.CompilerServices.CompilerGeneratedAttribute))
                    || runtime.IsEnum)
                {
                    continue;
                }

                var found = BareTypesIn(field.FieldType);
                if (found.Length > 0)
                {
                    bare.Add($"field {field.Name} is {found}");
                }
            }

            foreach (var property in runtime.GetProperties(declared & ~BindingFlags.Static))
            {
                if (exempt.Contains(property.Name) || property.GetIndexParameters().Length > 0
                    || property.Name == "EqualityContract")
                {
                    continue;
                }

                var found = BareTypesIn(property.PropertyType);
                if (found.Length > 0)
                {
                    bare.Add($"property {property.Name} is {found}");
                }
            }

            foreach (var method in runtime.GetMethods(declared))
            {
                if (method.IsSpecialName || PlatformMethods.Contains(method.Name) || exempt.Contains(method.Name)
                    || method.IsDefined(typeof(System.Runtime.CompilerServices.CompilerGeneratedAttribute)))
                {
                    continue;
                }

                var predicate = method.ReturnType == typeof(bool) || method.ReturnType == typeof(bool?);
                var returned = BareTypesIn(method.ReturnType);
                if (returned.Length > 0 && !predicate)
                {
                    bare.Add($"{method.Name}() returns {returned}");
                }

                var parameters = method.GetParameters();
                for (var i = 0; i < parameters.Length; i++)
                {
                    var taken = BareTypesIn(parameters[i].ParameterType);
                    if (taken.Length > 0)
                    {
                        bare.Add($"{method.Name}(...) takes {taken} as parameter {i + 1}");
                    }
                }
            }

            if (bare.Count > 0)
            {
                violations.Add($"{type.FullName}: {string.Join("; ", bare.OrderBy(b => b, StringComparer.Ordinal))}");
            }
        }

        DcaRule.Fail(
            "Domain types must not hold bare primitives, strings or time types",
            violations,
            "wrap each in a value object that carries its rules - a value of one component may hold the primitive it wraps");
    })
    .Experimental()
    .Selecting(
        "Classes, records, structs, enums and interfaces in <Module>.Domain of every module root, the shared"
        + " kernel's domain included, with their runtime type in the loaded assemblies - their declared"
        + " instance fields and properties and their declared methods, private ones included; constructors"
        + " are not selected, the members they fill are. Not selected: a wrapper value - a type assignable"
        + " to IValue or IId with exactly one instance field - with everything it declares; compiler-"
        + " generated members (a property's backing field, a record's EqualityContract, Deconstruct,"
        + " PrintMembers); property accessors and operators; Equals, GetHashCode, ToString and CompareTo; an"
        + " enum's members; a member that implements a building block's, such as a domain event's OccurredOn"
        + " and EventId. A bool return is a question to the object - a predicate - and passes; a bool field,"
        + " property or parameter does not.")
    .Checking(
        "No selected field, property, return type or parameter type involves string, bool, a numeric"
        + " primitive or char, a point in time (DateTime, DateTimeOffset, DateOnly, TimeOnly), or a bare Guid -"
        + " an identifier says whose it is through a typed id - nullable"
        + " and generic arguments and arrays included, so IReadOnlyList<string> counts. decimal, TimeSpan"
        + " and the project's own types pass. A value object with several components is checked like"
        + " any other type: each component is a value object itself. An empty selection passes.")
```
