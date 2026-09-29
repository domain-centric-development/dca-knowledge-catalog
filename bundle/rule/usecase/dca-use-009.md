---
type: Rule
id: DCA-USE-009
title: Use cases that save an aggregate must publish its domain events
rule: "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the instance they may later be published out of context. Publishing belongs after the save, in the use case that owns the unit of work - unless the aggregate is proven never to register an event: its whole hierarchy is under scan and no code unit of it, of a helper it calls, or of any other scanned class registering on that aggregate (a nested class it never calls) calls registerEvent; a helper in another top-level class cannot reach the protected method; an unresolved type argument keeps the requirement. Checked per entry path, following calls within the use case class: every entry point that reaches a save - a method callable from outside the class, or one nothing in the class calls - must also reach a publication; a wrapper that publishes does not cover a direct call of the public method it wraps, and a helper two methods share does not connect them. That the publication follows the save and concerns the same aggregate is not established statically. Only DomainEventPublisher.publishAndClearEvents counts as a publication: iterating domainEvents() and calling publish(event), even followed by clearDomainEvents(), separates dispatch from acknowledgement and is not accepted."
constraint: Use cases that save an aggregate must publish its domain events.
selects: "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix."
checks: "Only a resolved Repository<T,ID> whose aggregate and every non-building-block superclass are scanned and have no registration call (including helpers) is exempt. Unresolved generics, partial scans or undecidable external helpers remain required. For every non-exempt method of the class that calls Repository.save, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of DomainEventPublisher.publishAndClearEvents. Only publishAndClearEvents counts - publish(event), even followed by clearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes. The method names are fixed and are not part of the marker roles: a vocabulary whose repository writes under another name is selected and then found to save nothing, so this rule passes over it."
enforced_by: "UseCaseRules#DCA-USE-009"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use cases that save an aggregate must publish its domain events

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

Only a resolved Repository<T,ID> whose aggregate and every non-building-block superclass are scanned and have no registration call (including helpers) is exempt. Unresolved generics, partial scans or undecidable external helpers remain required. For every non-exempt method of the class that calls Repository.save, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of DomainEventPublisher.publishAndClearEvents. Only publishAndClearEvents counts - publish(event), even followed by clearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes. The method names are fixed and are not part of the marker roles: a vocabulary whose repository writes under another name is selected and then found to save nothing, so this rule passes over it.

## .NET reading

**Selection.** Classes in <module>.Application of every module root selected by IInputPort assignability or the configured use-case suffix, whose runtime type is in the loaded assemblies.

**Check.** Only a resolved IRepository<T,ID> aggregate is exempt, and only when its complete hierarchy is under scan and nothing registers an event on it: neither the hierarchy itself nor a type outside it. The walk stops at the platform and at the namespaces the configured marker roles live in, so a project's own vocabulary stops it where the library's does. Unresolved arguments and partial scans are not exempt. For every non-exempt method calling IRepository.SaveAsync, every entry point reaching it (a method callable from outside the class, or one nothing in the class calls) also reaches, through calls within the class, a call of IDomainEventPublisher.PublishAndClearEventsAsync. Calls are read from the IL of the class and its nested state-machine and closure types, so async methods and lambdas are followed. Only PublishAndClearEventsAsync counts - PublishAsync(event), even followed by ClearDomainEvents(), does not. A use case without a save (a query, a bulk delete) is selected but has nothing to check and passes. The method names are fixed and are not part of the marker roles: a vocabulary whose repository writes under another name is selected and then found to save nothing, so this rule passes over it.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/usecase/dca-use-009/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [InputPort](/marker/port-in/inputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/usecase/dca-use-009/overview.md)
- [`useCases`](/evidence/rule/usecase/dca-use-009/usecases.md)
- [`publishAfterSaving`](/evidence/rule/usecase/dca-use-009/publishaftersaving.md)
- [`calls`](/evidence/rule/usecase/dca-use-009/calls.md)
- [`pathName`](/evidence/rule/usecase/dca-use-009/pathname.md)
- [`EventFreeAggregate.repository`](/evidence/rule/usecase/dca-use-009/eventfreeaggregate-repository.md)
- [`IntraClassCalls.entryPointsOf`](/evidence/rule/usecase/dca-use-009/intraclasscalls-entrypointsof.md)
- [`IntraClassCalls.reachableFrom`](/evidence/rule/usecase/dca-use-009/intraclasscalls-reachablefrom.md)
- [`EventFreeAggregate.aggregate`](/evidence/rule/usecase/dca-use-009/eventfreeaggregate-aggregate.md)
- [`EventFreeAggregate.platform`](/evidence/rule/usecase/dca-use-009/eventfreeaggregate-platform.md)
- [`EventFreeAggregate.noRegistration`](/evidence/rule/usecase/dca-use-009/eventfreeaggregate-noregistration.md)
- [`EventFreeAggregate.noExternalRegistration`](/evidence/rule/usecase/dca-use-009/eventfreeaggregate-noexternalregistration.md)
- [`IntraClassCalls.callersOf`](/evidence/rule/usecase/dca-use-009/intraclasscalls-callersof.md)
- [`IntraClassCalls.isEntryPoint`](/evidence/rule/usecase/dca-use-009/intraclasscalls-isentrypoint.md)
- [`IntraClassCalls.closure`](/evidence/rule/usecase/dca-use-009/intraclasscalls-closure.md)
- [C# expression](/evidence/rule/usecase/dca-use-009/c-expression.md)
- [C# helper EventFreeAggregate](/evidence/rule/usecase/dca-use-009/c-helper-eventfreeaggregate.md)
- [C# helper IntraClassCalls](/evidence/rule/usecase/dca-use-009/c-helper-intraclasscalls.md)
