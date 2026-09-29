---
type: Rule
id: DCA-USE-012
title: Use cases that save an aggregate or publish domain events must have a transaction boundary
rule: "The use case owns the unit of work. Saving an aggregate is one business fact, yet the repository may write it as several statements - an aggregate of entities and value objects often spans several tables - and a repository adapter draws no boundary of its own; without one, a failure between the statements leaves half an aggregate behind. Publishing adds a second effect that must fall with the save: integration events are relayed after commit by the framework's after-commit listeners, and their publication is registered in the publishing transaction. Without an active transaction the after-commit listeners are skipped silently and nothing is registered: the use case succeeds, the other contexts never hear of it. The boundary is either declarative transaction metadata (the configured transactional annotation on the class or the executing method) or an explicit TransactionBoundary.inTransaction(...) around load, mutate, save and publish. Checked per entry path, following calls within the class: from every entry point - a method callable from outside the class, or one nothing in the class calls - no route down to the saving, deleting or publishing method may be free of an annotation or a boundary; a covered caller does not cover another route to the same helper, and a boundary on one route does not cover a second route. Whether the save or the publication sits inside the block handed to inTransaction(...) is not visible in ArchUnit's call model, which folds a lambda's body into the enclosing method; that placement stays a review check."
constraint: Use cases that save an aggregate or publish domain events must have a transaction boundary.
selects: "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix."
checks: "For every method that calls Repository.save, Repository.deleteById or a DomainEventPublisher, every route from each entry point down to it is covered: the class carries one of the configured transactional annotations, or every uncovered unit on the route is either annotated or calls TransactionBoundary.inTransaction. A covered caller does not cover a second route to the same helper. With an empty transactional role only the explicit boundary counts - which is the .NET default, where no preset configures a transactional attribute, while the Java presets configure the framework's own. A use case that neither saves, deletes nor publishes (a query, a Store write) is selected but has nothing to check and passes. Whether the save or publish call sits inside the inTransaction block is not checked - ArchUnit folds a lambda into its enclosing method. The method names are fixed and are not part of the marker roles: a vocabulary whose repository writes under another name is selected and then found to save nothing, so this rule passes over it."
enforced_by: "UseCaseRules#DCA-USE-012"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use cases that save an aggregate or publish domain events must have a transaction boundary

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix.

## Check

For every method that calls Repository.save, Repository.deleteById or a DomainEventPublisher, every route from each entry point down to it is covered: the class carries one of the configured transactional annotations, or every uncovered unit on the route is either annotated or calls TransactionBoundary.inTransaction. A covered caller does not cover a second route to the same helper. With an empty transactional role only the explicit boundary counts - which is the .NET default, where no preset configures a transactional attribute, while the Java presets configure the framework's own. A use case that neither saves, deletes nor publishes (a query, a Store write) is selected but has nothing to check and passes. Whether the save or publish call sits inside the inTransaction block is not checked - ArchUnit folds a lambda into its enclosing method. The method names are fixed and are not part of the marker roles: a vocabulary whose repository writes under another name is selected and then found to save nothing, so this rule passes over it.

## .NET reading

**Selection.** Concrete application operations selected by IInputPort marker or suffix with loadable runtime types, including closure and async units.

**Check.** Every entry path to a unit calling IRepository.SaveAsync, IRepository.DeleteByIdAsync or an IDomainEventPublisher crosses a unit calling ITransactionBoundary.InTransactionAsync (including its extension overloads) or carrying the configured TransactionalAttribute; a type-level attribute covers all paths. The declarative path is empty by default in .NET - AspNetCore() and None() both leave TransactionalAttribute unset, because ASP.NET Core has no ambient transaction attribute - so out of the box only the explicit boundary satisfies the rule, while the Java twin also accepts the framework's transactional annotation. A use case that neither saves, deletes nor publishes (a query, a Store write) is selected but has nothing to check and passes. Static limit: a boundary call in the same unit passes even when the save or publication follows an empty boundary block. Runtime rollback containment must be tested separately. The method names are fixed and are not part of the marker roles: a vocabulary whose repository writes under another name is selected and then found to save nothing, so this rule passes over it.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/usecase/dca-use-012/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [InputPort](/marker/port-in/inputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [TransactionBoundary](/marker/application/transactionboundary.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/usecase/dca-use-012/overview.md)
- [`useCases`](/evidence/rule/usecase/dca-use-012/usecases.md)
- [`beTransactionalWhenMutating`](/evidence/rule/usecase/dca-use-012/betransactionalwhenmutating.md)
- [`transactionalEffectOf`](/evidence/rule/usecase/dca-use-012/transactionaleffectof.md)
- [`pathIsTransactional`](/evidence/rule/usecase/dca-use-012/pathistransactional.md)
- [`pathName`](/evidence/rule/usecase/dca-use-012/pathname.md)
- [`IntraClassCalls.entryPointsOf`](/evidence/rule/usecase/dca-use-012/intraclasscalls-entrypointsof.md)
- [`calls`](/evidence/rule/usecase/dca-use-012/calls.md)
- [`callsBoundary`](/evidence/rule/usecase/dca-use-012/callsboundary.md)
- [`AnnotationRoles.isMetaAnnotatedWithAny`](/evidence/rule/usecase/dca-use-012/annotationroles-ismetaannotatedwithany.md)
- [`IntraClassCalls.reachableThrough`](/evidence/rule/usecase/dca-use-012/intraclasscalls-reachablethrough.md)
- [`IntraClassCalls.callersOf`](/evidence/rule/usecase/dca-use-012/intraclasscalls-callersof.md)
- [`IntraClassCalls.isEntryPoint`](/evidence/rule/usecase/dca-use-012/intraclasscalls-isentrypoint.md)
- [`IntraClassCalls.closure`](/evidence/rule/usecase/dca-use-012/intraclasscalls-closure.md)
- [C# expression](/evidence/rule/usecase/dca-use-012/c-expression.md)
- [C# helper OperationPolicy](/evidence/rule/usecase/dca-use-012/c-helper-operationpolicy.md)
- [C# helper IntraClassCalls](/evidence/rule/usecase/dca-use-012/c-helper-intraclasscalls.md)
