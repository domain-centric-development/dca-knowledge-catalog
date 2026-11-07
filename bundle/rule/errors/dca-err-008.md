---
type: Rule
id: DCA-ERR-008
title: "Diagnostic: closed use-case results without a case marked as a refusal"
rule: "A closed result describes the outcomes a use case can answer with; some of them are refusals, some are not. A result may hold several outcomes of which none refuses - found or nothing found, sent or already sent - and that alone is reason enough to close it. The refusal marker on a case says the request was refused, a meaning the caller answers with or without a transaction, and it is what lets the transaction boundary roll a refusal back like a thrown failure. Whether a case refuses is domain knowledge the type does not show, so a closed result without any marked case is listed for a look, not failed: if one of its outcomes is a refusal and stays unmarked, the transaction commits the writes made before it."
constraint: "Diagnostic: closed use-case results without a case marked as a refusal."
selects: "Closed results in <module>.application.. of every module root: a sealed type that a public method of a type assignable to InputPort returns, or that such an input port's use-case interface binds as a type argument - commands and queries excluded."
checks: "Informational diagnostic only: lists every closed result none of whose cases is assignable to the configured refusal role (by default the Refusal marker of the building blocks), and never fails. Its cases are its permitted subclasses, recursively through sealed cases, so refusals grouped below a sealed case of their own count. The result type itself carrying the marker does not count. A listed result is not a finding by itself: a closed result whose outcomes are all successes - found or nothing found - is correct as it is. A context that throws its refusals has no closed results and lists nothing."
enforced_by: "ErrorHandlingRules#DCA-ERR-008"
status: informational
maturity: experimental
rule_set: errors
implementations: [java, dotnet, rust]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Diagnostic: closed use-case results without a case marked as a refusal

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Closed results in <module>.application.. of every module root: a sealed type that a public method of a type assignable to InputPort returns, or that such an input port's use-case interface binds as a type argument - commands and queries excluded.

## Check

Informational diagnostic only: lists every closed result none of whose cases is assignable to the configured refusal role (by default the Refusal marker of the building blocks), and never fails. Its cases are its permitted subclasses, recursively through sealed cases, so refusals grouped below a sealed case of their own count. The result type itself carrying the marker does not count. A listed result is not a finding by itself: a closed result whose outcomes are all successes - found or nothing found - is correct as it is. A context that throws its refusals has no closed results and lists nothing.

## .NET reading

**Selection.** Closed results under <Module>.Application of every module root: a type an input port answers with - a type argument of its use-case interface or the return type of one of its methods, a task unwrapped - that derives from one of the configured closed-result base types (FrameworkTypes.ClosedResultBaseTypes, matched by name). An empty list of base types selects nothing.

**Check.** Informational diagnostic only: lists every closed result none of whose cases - the generic arguments of the closed-result base - is assignable to the configured refusal role (by default the IRefusal marker of the building blocks), and never fails. The result type itself carrying the marker does not count. A listed result is not a finding by itself: a closed result whose outcomes are all successes - found or nothing found - is correct as it is. A context that throws its refusals has no closed results and lists nothing.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a lint or a test (source-test).

**Selection.** Closed results in every application crate: an enum an input-port trait answers with - named in an associated-type binding of its bounds (Output = ...) or in a method's return type, through any wrapper such as Result - as DCA-ERR-006 finds them; an enum that implements std::error::Error, DomainFailure or UseCaseFailure is the failure side and not selected.

**Check.** Informational - lists every closed result none of whose variants carries a field whose type implements the building-block trait Refusal, and never fails. A unit variant carries nothing and cannot be the refusing one: a refusing variant wraps a value of a type that implements Refusal, and the result enum implements ClosedResult, whose refusal() match the compiler checks for coverage and for the Refusal bound - that is what TransactionBoundary::in_transaction_closed rolls back on. A listed result is not a finding by itself: one whose outcomes are all successes - found or nothing found - is correct as it is. A struct is no closed result.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/errors/dca-err-008/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `inApplication()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/errors/dca-err-008/overview.md)
- [`closedResultsOf`](/evidence/rule/errors/dca-err-008/closedresultsof.md)
- [`collectCaseClasses`](/evidence/rule/errors/dca-err-008/collectcaseclasses.md)
- [`TypeInspection.outputTypes`](/evidence/rule/errors/dca-err-008/typeinspection-outputtypes.md)
- [`TypeInspection.collectInputs`](/evidence/rule/errors/dca-err-008/typeinspection-collectinputs.md)
- [`TypeInspection.involvedTypes`](/evidence/rule/errors/dca-err-008/typeinspection-involvedtypes.md)
- [`TypeInspection.collect`](/evidence/rule/errors/dca-err-008/typeinspection-collect.md)
- [`TypeInspection.typeArgumentBindings`](/evidence/rule/errors/dca-err-008/typeinspection-typeargumentbindings.md)
- [`TypeInspection.variableKey`](/evidence/rule/errors/dca-err-008/typeinspection-variablekey.md)
- [C# expression](/evidence/rule/errors/dca-err-008/c-expression.md)
