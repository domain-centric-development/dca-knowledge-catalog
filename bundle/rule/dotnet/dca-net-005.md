---
type: Rule
id: DCA-NET-005
title: Identifiers should be readonly record structs
rule: A strongly typed identifier as a readonly record struct costs no allocation and cannot be confused with a raw Guid or string.
constraint: Identifiers should be readonly record structs.
selects: "Non-interface, non-abstract types anywhere under the root namespace that are assignable to IId and whose runtime type is in the loaded assemblies."
checks: "The type must be a readonly record struct. Reference types, plain structs and mutable record structs fail."
enforced_by: "DotnetRules#DCA-NET-005"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---

## Selection

Non-interface, non-abstract types anywhere under the root namespace that are assignable to IId and whose runtime type is in the loaded assemblies.

## Check

The type must be a readonly record struct. Reference types, plain structs and mutable record structs fail.

### C# expression

```csharp
DcaRule.Check(
        "DCA-NET-005",
        "Identifiers should be readonly record structs",
        "A strongly typed identifier as a readonly record struct costs no allocation and cannot be confused with a raw Guid or string",
        arch =>
        {
            var violations = new List<string>();
            foreach (var type in arch.Types)
            {
                var runtime = arch.RuntimeType(type);
                if (runtime is null || runtime.IsInterface || runtime.IsAbstract || !typeof(IId).IsAssignableFrom(runtime))
                {
                    continue;
                }

                if (!runtime.IsValueType)
                {
                    violations.Add($"{runtime.FullName} implements IId but is a reference type");
                }
                else if (!IsRecord(type, runtime) || !runtime.IsDefined(typeof(System.Runtime.CompilerServices.IsReadOnlyAttribute), false))
                {
                    violations.Add($"{runtime.FullName} implements IId but is not a readonly record struct");
                }
            }

            DcaRule.Fail(
                "Identifiers should be readonly record structs\nbecause a readonly record struct costs no allocation and cannot be confused with a raw Guid or string",
                violations,
                "Declare the identifier as `public readonly record struct XId(Guid Value) : IId`.");
        })
    .Selecting(
        "Non-interface, non-abstract types anywhere under the root namespace that are"
            + " assignable to IId and whose runtime type is in the loaded assemblies.")
    .Checking(
        "The type must be a readonly record struct. Reference types, plain structs and mutable record structs fail." )
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
