---
type: Rule
id: DCA-NET-002
title: Port methods returning Task must end with Async
rule: The Async suffix is the .NET convention that tells callers a method is awaitable; ports are the contract other layers program against.
constraint: Port methods returning Task must end with Async.
selects: Interfaces under the root namespace that are assignable to IInputPort or IOutputPort and whose runtime type is in the loaded assemblies.
checks: "Every public method declared on the interface itself (inherited members, property accessors and operators excluded) returns Task, Task<T>, ValueTask or ValueTask<T> exactly when its name ends with Async. Both directions are reported: an awaitable method without the suffix and a suffixed method that returns something else. An empty selection passes."
enforced_by: "DotnetRules#DCA-NET-002"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---

## Selection

Interfaces under the root namespace that are assignable to IInputPort or IOutputPort and whose runtime type is in the loaded assemblies.

## Check

Every public method declared on the interface itself (inherited members, property accessors and operators excluded) returns Task, Task<T>, ValueTask or ValueTask<T> exactly when its name ends with Async. Both directions are reported: an awaitable method without the suffix and a suffixed method that returns something else. An empty selection passes.

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
