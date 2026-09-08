---
type: Rule
id: DCA-NET-003
title: Use cases must expose exactly one ExecuteAsync
rule: "One use case, one entry point: the input port is the only way in, and a cancellation token lets the host stop long-running work."
constraint: Use cases must expose exactly one ExecuteAsync.
selects: "Non-abstract classes under the root namespace that implement IUseCase<TInput, TOutput> and whose runtime type is in the loaded assemblies - in any namespace, not only the application layer."
checks: "The class declares exactly one public instance method named ExecuteAsync, which returns Task<T> (a plain Task is reported) and takes a CancellationToken as its last parameter. Inherited methods are not counted; other public members with a different name are not reported. An empty selection passes."
enforced_by: "DotnetRules#DCA-NET-003"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---

## Selection

Non-abstract classes under the root namespace that implement IUseCase<TInput, TOutput> and whose runtime type is in the loaded assemblies - in any namespace, not only the application layer.

## Check

The class declares exactly one public instance method named ExecuteAsync, which returns Task<T> (a plain Task is reported) and takes a CancellationToken as its last parameter. Inherited methods are not counted; other public members with a different name are not reported. An empty selection passes.

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
