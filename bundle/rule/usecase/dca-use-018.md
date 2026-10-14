---
type: Rule
id: DCA-USE-018
title: "In a module grouped by feature, incoming adapters must drive the commands of one feature only"
rule: "Once the application is grouped, the incoming adapter is cut the same way: one controller changes state through the use cases of one feature. A class that drives the commands of two features grows with every use case of both and hides the cut the application already made. Reading a neighbouring feature's query is no reason to cut."
constraint: "In a module grouped by feature, incoming adapters must drive the commands of one feature only."
selects: "Per module root whose input ports or use cases sit at the feature depth application.<feature>.<usecase> (configured operationContainers segments removed, application.shared excluded): every non-interface class in <module>.adapter.incoming.. of that module. Modules with flat use case packages are not selected."
checks: "The types assignable to the configured input-port role whose input ends with Command - a parameter of a public method, or a type argument of the input port they extend - that the class depends on directly, inside the same module, belong to at most one feature, the feature being the first segment below the application package. Input ports whose input ends with Query, or with neither suffix, are not counted, and neither is an input port of another module. Nested classes are counted on their own. An empty selection passes."
enforced_by: "UseCaseRules#DCA-USE-018"
status: enforced
maturity: experimental
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# In a module grouped by feature, incoming adapters must drive the commands of one feature only

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Per module root whose input ports or use cases sit at the feature depth application.<feature>.<usecase> (configured operationContainers segments removed, application.shared excluded): every non-interface class in <module>.adapter.incoming.. of that module. Modules with flat use case packages are not selected.

## Check

The types assignable to the configured input-port role whose input ends with Command - a parameter of a public method, or a type argument of the input port they extend - that the class depends on directly, inside the same module, belong to at most one feature, the feature being the first segment below the application package. Input ports whose input ends with Query, or with neither suffix, are not counted, and neither is an input port of another module. Nested classes are counted on their own. An empty selection passes.

## .NET reading

**Selection.** Classes in <module>.Adapter.Incoming of every module root, compiler-generated classes excluded, with the command ports they depend on: types assignable to IInputPort in the same module's application namespace whose input ends in Command - the input type argument of IUseCase<TInput, TOutput> or a parameter of an input-port method. A port counts toward a feature when it sits at Application.<Feature>.<UseCase> after removing configured OperationContainers segments, the grouped depth of DCA-USE-014.

**Check.** The command ports an adapter depends on belong to one feature. A port whose input ends in Query, or ends in neither, is not counted - reading a neighbouring feature's query is allowed. A port in a flat use-case namespace (Application.<UseCase>), in Application.Shared or in another module counts toward no feature, so a module that is not grouped into features is never reported. Fields, constructor parameters and calls all count as a dependency; constructor parameters are read from the runtime type as well. An empty selection passes.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/usecase/dca-use-018/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `moduleRoots()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/usecase/dca-use-018/overview.md)
- [`checkOneFeaturePerAdapter`](/evidence/rule/usecase/dca-use-018/checkonefeatureperadapter.md)
- [`isGroupedByFeature`](/evidence/rule/usecase/dca-use-018/isgroupedbyfeature.md)
- [`useCaseSegments`](/evidence/rule/usecase/dca-use-018/usecasesegments.md)
- [`TypeInspection.takesInputEndingWith`](/evidence/rule/usecase/dca-use-018/typeinspection-takesinputendingwith.md)
- [`TypeInspection.inputTypes`](/evidence/rule/usecase/dca-use-018/typeinspection-inputtypes.md)
- [`TypeInspection.collectInputs`](/evidence/rule/usecase/dca-use-018/typeinspection-collectinputs.md)
- [`TypeInspection.involvedTypes`](/evidence/rule/usecase/dca-use-018/typeinspection-involvedtypes.md)
- [`TypeInspection.collect`](/evidence/rule/usecase/dca-use-018/typeinspection-collect.md)
- [`TypeInspection.typeArgumentBindings`](/evidence/rule/usecase/dca-use-018/typeinspection-typeargumentbindings.md)
- [`TypeInspection.variableKey`](/evidence/rule/usecase/dca-use-018/typeinspection-variablekey.md)
- [C# expression](/evidence/rule/usecase/dca-use-018/c-expression.md)
