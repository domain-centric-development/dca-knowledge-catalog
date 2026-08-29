---
type: Rule
id: DCA-NET-003
title: Use cases must expose exactly one ExecuteAsync
rule: "One use case, one entry point: the input port is the only way in, and a cancellation token lets the host stop long-running work."
constraint: Use cases must expose exactly one ExecuteAsync.
enforced_by: "DotnetRules#DCA-NET-003"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---
