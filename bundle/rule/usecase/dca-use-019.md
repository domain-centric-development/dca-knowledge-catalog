---
type: Rule
id: DCA-USE-019
title: Query use cases must not write or publish
rule: "A read never creates. A query has no side effect: it does not create, save or publish, and when nothing exists it answers none. Find-or-create is a command, called where the caller is about to change state; a page or an answer that only shows what exists asks the query."
constraint: Query use cases must not write or publish.
selects: "Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix, and whose input ends with Query - a parameter of a public method, or a type argument of the input port they implement."
checks: "No code unit of the class calls a write on the repository or store role - a method whose name is a write verb alone or followed by a capital (save, delete, remove, add, insert, update, upsert, put, store, write, create, append, archive, purge, clear, set, mark) - nor any method of the domain-event or integration-event publisher role. Calls made by another class the use case delegates to are not followed. An empty selection passes."
enforced_by: "UseCaseRules#DCA-USE-019"
status: enforced
maturity: experimental
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Query use cases must not write or publish

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Non-interface classes in <module>.application.. that implement InputPort or whose simple name ends with the configured use-case suffix, and whose input ends with Query - a parameter of a public method, or a type argument of the input port they implement.

## Check

No code unit of the class calls a write on the repository or store role - a method whose name is a write verb alone or followed by a capital (save, delete, remove, add, insert, update, upsert, put, store, write, create, append, archive, purge, clear, set, mark) - nor any method of the domain-event or integration-event publisher role. Calls made by another class the use case delegates to are not followed. An empty selection passes.

## .NET reading

**Selection.** Concrete non-nested application operations selected by IInputPort marker or configured use-case suffix, with loadable runtime types, whose input ends in Query: the input type argument of an implemented IUseCase<TInput, TOutput>, or a parameter of a method that implements an IInputPort interface.

**Check.** No method of the class - async state machines and lambdas included - calls a repository write (IRepository.SaveAsync or DeleteByIdAsync, or a method of a repository or store port whose name starts with Save, Delete, Remove, Add, Insert, Update, Upsert, Put, Store, Write, Create, Append, Archive, Purge, Clear, Set or Mark), or any method of the domain-event or integration-event publisher. Only the class's own calls are read: a write reached through a helper class or a second port is not seen, and a store write under another verb passes. An empty selection passes.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/usecase/dca-use-019/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/usecase/dca-use-019/overview.md)
- [`useCases`](/evidence/rule/usecase/dca-use-019/usecases.md)
- [`takingAQuery`](/evidence/rule/usecase/dca-use-019/takingaquery.md)
- [`notWriteOrPublish`](/evidence/rule/usecase/dca-use-019/notwriteorpublish.md)
- [`TypeInspection.takesInputEndingWith`](/evidence/rule/usecase/dca-use-019/typeinspection-takesinputendingwith.md)
- [`sideEffectOf`](/evidence/rule/usecase/dca-use-019/sideeffectof.md)
- [`TypeInspection.inputTypes`](/evidence/rule/usecase/dca-use-019/typeinspection-inputtypes.md)
- [`TypeInspection.collectInputs`](/evidence/rule/usecase/dca-use-019/typeinspection-collectinputs.md)
- [`TypeInspection.involvedTypes`](/evidence/rule/usecase/dca-use-019/typeinspection-involvedtypes.md)
- [`TypeInspection.collect`](/evidence/rule/usecase/dca-use-019/typeinspection-collect.md)
- [`TypeInspection.typeArgumentBindings`](/evidence/rule/usecase/dca-use-019/typeinspection-typeargumentbindings.md)
- [`TypeInspection.variableKey`](/evidence/rule/usecase/dca-use-019/typeinspection-variablekey.md)
- [C# expression](/evidence/rule/usecase/dca-use-019/c-expression.md)
- [C# helper OperationPolicy](/evidence/rule/usecase/dca-use-019/c-helper-operationpolicy.md)
- [C# helper IntraClassCalls](/evidence/rule/usecase/dca-use-019/c-helper-intraclasscalls.md)
