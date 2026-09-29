---
type: Rule
id: DCA-USE-013
title: Declaratively transactional use cases must not call remote-capable output ports
rule: "A declaratively transactional use case holds a database connection for its whole run. Calling an output port that may leave the process (another context's API, a payment provider, a mail gateway) inside it blocks that connection for the remote round trip; under load the pool runs dry, and a rollback cannot undo the remote effect. Only transactional resources belong inside the boundary: Repository, Store, DomainEventPublisher, IntegrationEventPublisher. Everything else is called before the transaction - draw the boundary by hand with TransactionBoundary.inTransaction(...) - or after it, as a reaction to an integration event."
constraint: Declaratively transactional use cases must not call remote-capable output ports.
selects: "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix."
checks: "Every method that runs under one of the configured transactional annotations - on the class, on itself, or on a method that reaches it within the class - calls no OutputPort other than Repository, Store, DomainEventPublisher or IntegrationEventPublisher. A use case without such an annotation (explicit TransactionBoundary or none) is selected but never reported; with an empty role nothing is ever reported."
enforced_by: "UseCaseRules#DCA-USE-013"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Declaratively transactional use cases must not call remote-capable output ports

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

Every method that runs under one of the configured transactional annotations - on the class, on itself, or on a method that reaches it within the class - calls no OutputPort other than Repository, Store, DomainEventPublisher or IntegrationEventPublisher. A use case without such an annotation (explicit TransactionBoundary or none) is selected but never reported; with an empty role nothing is ever reported.

## .NET reading

**Selection.** Concrete application operations selected by IInputPort marker or configured use-case suffix, with loadable runtime types. Nothing at all while no transactional attribute is configured, which is the default: neither .NET preset names one, because ASP.NET Core has no ambient transaction attribute.

**Check.** Every code unit that runs under the configured transactional attribute - on the class, on itself, or on an entry point that reaches it within the class - calls no output port other than IRepository, IStore, IDomainEventPublisher or IIntegrationEventPublisher. A use case without such an attribute (an explicit ITransactionBoundary, or none) is selected but never reported, and with no attribute configured nothing is ever reported - the rule then carries the id without checking anything, as the Java twin does where no framework annotation is on the class path. What happens inside an InTransactionAsync block is not inspected; the explicit boundary is the developer's own and its extent is visible at the call site.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/usecase/dca-use-013/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [InputPort](/marker/port-in/inputport.md)
- [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [TransactionBoundary](/marker/application/transactionboundary.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/usecase/dca-use-013/overview.md)
- [`useCases`](/evidence/rule/usecase/dca-use-013/usecases.md)
- [`notCallRemotePortsWhenTransactional`](/evidence/rule/usecase/dca-use-013/notcallremoteportswhentransactional.md)
- [`isTransactional`](/evidence/rule/usecase/dca-use-013/istransactional.md)
- [`isTransactionalResource`](/evidence/rule/usecase/dca-use-013/istransactionalresource.md)
- [`AnnotationRoles.isMetaAnnotatedWithAny`](/evidence/rule/usecase/dca-use-013/annotationroles-ismetaannotatedwithany.md)
- [`IntraClassCalls.callersOf`](/evidence/rule/usecase/dca-use-013/intraclasscalls-callersof.md)
- [`IntraClassCalls.closure`](/evidence/rule/usecase/dca-use-013/intraclasscalls-closure.md)
- [C# expression](/evidence/rule/usecase/dca-use-013/c-expression.md)
- [C# helper OperationPolicy](/evidence/rule/usecase/dca-use-013/c-helper-operationpolicy.md)
- [C# helper IntraClassCalls](/evidence/rule/usecase/dca-use-013/c-helper-intraclasscalls.md)
