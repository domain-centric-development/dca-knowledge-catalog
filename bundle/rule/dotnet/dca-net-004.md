---
type: Rule
id: DCA-NET-004
title: Struct value objects must be readonly
rule: "Records give attribute-based equality, immutability by default and with-expressions — the C# way to write a Value Object."
constraint: Struct value objects must be readonly.
selects: "Non-interface, non-abstract types in <module>.Domain of every module root that are assignable to IValue and whose runtime type is in the loaded assemblies."
checks: Struct values must carry the readonly modifier. Classes are governed by TAC-009/010/012; equality is checked by TAC-012. An IValue outside a domain namespace is not selected.
enforced_by: "DotnetRules#DCA-NET-004"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---

## Selection

Non-interface, non-abstract types in <module>.Domain of every module root that are assignable to IValue and whose runtime type is in the loaded assemblies.

## Check

Struct values must carry the readonly modifier. Classes are governed by TAC-009/010/012; equality is checked by TAC-012. An IValue outside a domain namespace is not selected.

### C# expression

```csharp
DcaRule.Check(
        "DCA-NET-004",
        "Struct value objects must be readonly",
        "Records give attribute-based equality, immutability by default and with-expressions — the C# way to write a Value Object",
        arch =>
        {
            var domain = arch.AllDomainPatterns().Select(p => new Regex(p)).ToList();
            var violations = new List<string>();
            foreach (var type in arch.Types.Where(t => domain.Any(r => r.IsMatch(t.Namespace.FullName))))
            {
                var runtime = arch.RuntimeType(type);
                if (runtime is null || runtime.IsInterface || runtime.IsAbstract || !typeof(IValue).IsAssignableFrom(runtime))
                {
                    continue;
                }

                if (runtime.IsValueType && !runtime.IsDefined(typeof(System.Runtime.CompilerServices.IsReadOnlyAttribute), false))
                {
                    violations.Add($"{runtime.FullName} implements IValue but is a mutable struct");
                }
            }

            DcaRule.Fail(
                "Struct value objects must be readonly\nbecause records are the C# way to write a Value Object",
                violations,
                "Declare the value object as `public sealed record X(...)` or `public readonly record struct X(...)`.");
        })
    .Selecting(
        "Non-interface, non-abstract types in <module>.Domain of every module root that"
            + " are assignable to IValue and whose runtime type is in the loaded assemblies.")
    .Checking(
        "Struct values must carry the readonly modifier. Classes are governed by TAC-009/010/012; equality is checked by TAC-012. An IValue outside a domain namespace is not selected." )
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
