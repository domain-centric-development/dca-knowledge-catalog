---
type: Rule
id: DCA-NET-004
title: Value objects should be records or readonly record structs
rule: "Records give attribute-based equality, immutability by default and with-expressions — the C# way to write a Value Object."
constraint: Value objects should be records or readonly record structs.
selects: "Non-interface, non-abstract types in <module>.Domain of every module root that are assignable to IValue and whose runtime type is in the loaded assemblies."
checks: "The type is a record class, a record struct or any other struct. A plain class implementing IValue is reported. Whether a struct is declared readonly is not checked, and an IValue type outside a domain namespace is not selected. An empty selection passes."
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

The type is a record class, a record struct or any other struct. A plain class implementing IValue is reported. Whether a struct is declared readonly is not checked, and an IValue type outside a domain namespace is not selected. An empty selection passes.

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
