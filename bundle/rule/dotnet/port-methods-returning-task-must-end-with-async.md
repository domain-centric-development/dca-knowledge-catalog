---
type: Rule
id: DCA-NET-002
title: Port methods returning Task must end with Async
rule: The Async suffix is the .NET convention that tells callers a method is awaitable; ports are the contract other layers program against.
constraint: Port methods returning Task must end with Async.
enforced_by: "DotnetRules#DCA-NET-002"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---
