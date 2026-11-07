---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate — C# expression"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#c-expression"
---

[Full node and context](/rule/tactical/dca-tac-025.md#c-expression). This is an evidence excerpt; retain the parent selection and caveats.

### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-025",
    "Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate",
    "A value with rules of its own - a postal code, a quantity, a moment, an identifier - is a value object;"
        + " held as a bare string, int, DateTimeOffset or Guid its validation is repeated at every use or"
        + " missing. A value object with several components holds value objects too; only a wrapper - a"
        + " value of exactly one component - holds the primitive it wraps. A single yes/no fact may stay a"
        + " bool field: the type is told (Complete()) and answers (IsCompleted). A bool parameter is a flag"
        + " argument - SetCompleted(true) lets the caller set the state instead of triggering the behaviour -"
        + " and three or more states, or transitions with rules, are an enum or a value",
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
            .Where(t => !t.IsCompilerGenerated && arch.InDomain(t))
            .OrderBy(t => t.FullName, StringComparer.Ordinal))
        {
            var runtime = arch.RuntimeType(type);
            if (runtime is null || IsWrapperValue(runtime, markers) || IsFailure(runtime, markers)
                || NestedInWrapperOrValue(runtime, markers))
            {
                continue;
            }

            var exempt = BuildingBlockMemberNames(runtime, blockNamespaces);
            const BindingFlags declared = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance
                | BindingFlags.Static | BindingFlags.DeclaredOnly;
            var bare = new List<string>();
            var stateReported = false;
            foreach (var field in runtime.GetFields(declared & ~BindingFlags.Static))
            {
                if (field.IsDefined(typeof(System.Runtime.CompilerServices.CompilerGeneratedAttribute))
                    || runtime.IsEnum)
                {
                    continue;
                }

                if (IsBoolean(field.FieldType))
                {
                    if (field.IsPublic && !field.IsInitOnly)
                    {
                        bare.Add($"field {field.Name} is a public Boolean anyone may set - a flag argument");
                    }

                    continue;
                }

                var found = BareTypesIn(field.FieldType);
                if (found.Length > 0)
                {
                    bare.Add($"field {field.Name} is {found}");
                    stateReported = true;
                }
            }

            foreach (var property in runtime.GetProperties(declared & ~BindingFlags.Static))
            {
                if (exempt.Contains(property.Name) || property.GetIndexParameters().Length > 0
                    || property.Name == "EqualityContract")
                {
                    continue;
                }

                if (IsBoolean(property.PropertyType))
                {
                    if (HasPublicSetter(property))
                    {
                        bare.Add($"property {property.Name} is Boolean with a public setter - a flag argument");
                    }

                    continue;
                }

                var found = BareTypesIn(property.PropertyType);
                if (found.Length > 0)
                {
                    bare.Add($"property {property.Name} is {found}");
                    stateReported = true;
                }
            }

            foreach (var method in runtime.GetMethods(declared))
            {
                if (method.IsSpecialName || PlatformMethods.Contains(method.Name) || exempt.Contains(method.Name)
                    || method.IsDefined(typeof(System.Runtime.CompilerServices.CompilerGeneratedAttribute)))
                {
                    continue;
                }

                var predicate = IsBoolean(method.ReturnType);
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
                violations.Add($"{type.FullName}: {string.Join("; ", bare.OrderBy(b => b, StringComparer.Ordinal))}"
                    + (stateReported && InstanceFieldCount(runtime) == 1
                        ? $" - it has one field: mark it as a value or an id ({markers.Marker(nameof(DcaMarkers.Value))}) to count as a wrapper"
                        : ""));
            }
        }

        DcaRule.Fail(
            "Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate",
            violations,
            "wrap each in a value object that carries its rules - a value of one component may hold the primitive it wraps;"
            + " replace a bool parameter or a public bool setter by a method that names the behaviour - Complete() instead of SetCompleted(true)");
    })
    .Experimental()
    .Selecting(
        "Classes, records, structs, enums and interfaces in <Module>.Domain of every module root, the shared"
        + " kernel's domain included, with their runtime type in the loaded assemblies - their declared"
        + " instance fields and properties and their declared methods, private ones included; constructors"
        + " are not selected, the members they fill are. Not selected: a wrapper value - a type assignable"
        + " to IValue or IId with exactly one instance field - with everything it declares; a type declared"
        + " inside a value or an id, such as the value's own error shapes, which carry the input it refused;"
        + " a failure - a type of the domain-exception or use-case-exception role; compiler-"
        + " generated members (a property's backing field, a record's EqualityContract, Deconstruct,"
        + " PrintMembers); property accessors and operators; Equals, GetHashCode, ToString and CompareTo; an"
        + " enum's members; a member that implements a building block's, such as a domain event's OccurredOn"
        + " and EventId. A field typed bool or bool? - a single yes/no fact - and a bool return - a question to"
        + " the object, a predicate - pass, and so does a bool property without a public setter (get-only, a"
        + " private or init setter); a bool parameter, a bool property with a public setter and a public non-readonly bool field are flag"
        + " arguments and do not.")
    .Checking(
        "No selected field, property, return type or parameter type involves string, bool, a numeric"
        + " primitive or char, a point in time (DateTime, DateTimeOffset, DateOnly, TimeOnly), or a bare Guid -"
        + " an identifier says whose it is through a typed id - nullable"
        + " and generic arguments and arrays included, so IReadOnlyList<string> counts. decimal, TimeSpan"
        + " and the project's own types pass. A field or a property typed bool or bool? and a method"
        + " returning one pass, unless anyone may set it - a public setter, a public non-readonly field; a bool among the parameters is a"
        + " flag argument and counts, and so does an IReadOnlyList<bool>. A value object with several components is checked like"
        + " any other type: each component is a value object itself. A reported type with exactly one"
        + " instance field that is no value or id is told to carry the value or id role to count as a"
        + " wrapper. An empty selection passes.")
```
