---
type: Rule
id: DCA-NET-004
title: Value objects should be records or readonly record structs
rule: "Records give attribute-based equality, immutability by default and with-expressions — the C# way to write a Value Object."
constraint: Value objects should be records or readonly record structs.
enforced_by: "DotnetRules#DCA-NET-004"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---
