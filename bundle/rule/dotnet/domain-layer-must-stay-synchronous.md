---
type: Rule
id: DCA-NET-001
title: Domain layer must stay synchronous
rule: "Async is an I/O concern of ports and adapters; a synchronous domain model stays testable, deterministic and free of sync-over-async hazards."
constraint: Domain layer must stay synchronous.
enforced_by: "DotnetRules#DCA-NET-001"
status: enforced
rule_set: dotnet
implementations: [dotnet]
resource: dca-dotnet/src/DomainCentric.ArchRules/Rules/DotnetRules.cs
tags: [dotnet, archunitnet]
---
