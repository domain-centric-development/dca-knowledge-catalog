---
type: Rule
id: DCA-NET-005
title: Identifiers should be readonly record structs
rule: A strongly typed identifier as a readonly record struct costs no allocation and cannot be confused with a raw Guid or string.
constraint: Identifiers should be readonly record structs.
selects: "Non-interface, non-abstract types anywhere under the root namespace that are assignable to IId and whose runtime type is in the loaded assemblies."
checks: "The type is a record struct: a reference type (a record class included) is reported as such, a plain struct as not being a record. Whether the struct is declared readonly is not checked. An empty selection passes."
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

The type is a record struct: a reference type (a record class included) is reported as such, a plain struct as not being a record. Whether the struct is declared readonly is not checked. An empty selection passes.

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
