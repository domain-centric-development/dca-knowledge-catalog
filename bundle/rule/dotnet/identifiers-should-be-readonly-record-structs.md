---
type: Rule
id: DCA-NET-005
title: Identifiers should be readonly record structs
rule: A strongly typed identifier as a readonly record struct costs no allocation and cannot be confused with a raw Guid or string.
constraint: Identifiers should be readonly record structs.
enforced_by: "DotnetRules#DCA-NET-005"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---
