---
type: Rule
id: DCA-NET-001
title: Domain layer must stay synchronous
rule: "Async is an I/O concern of ports and adapters; a synchronous domain model stays testable, deterministic and free of sync-over-async hazards."
constraint: Domain layer must stay synchronous.
selects: "Types in <module>.Domain of every module root."
checks: "No dependency on Task, Task<T>, ValueTask, ValueTask<T> or CancellationToken - in a signature, a field or a method body. Other awaitables and IAsyncEnumerable<T> are not checked. An empty selection passes."
enforced_by: "DotnetRules#DCA-NET-001"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---

## Selection

Types in <module>.Domain of every module root.

## Check

No dependency on Task, Task<T>, ValueTask, ValueTask<T> or CancellationToken - in a signature, a field or a method body. Other awaitables and IAsyncEnumerable<T> are not checked. An empty selection passes.

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
