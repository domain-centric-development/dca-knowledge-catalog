---
type: Rule
id: DCA-ERR-007
title: "Diagnostic: failures that carry display data or objects instead of ids and figures"
rule: "A failure carries ids and figures, never what a page shows. Its fields are the typed identities and the values the rule compared; a name or a description of the thing an id refers to is resolved by the translation site through the queries it already has. A failure that carries the name decides for every surface what it shows, and one that carries an aggregate or an entity hands the model out through the error path."
constraint: "Diagnostic: failures that carry display data or objects instead of ids and figures."
selects: "Concrete project classes assignable to DomainException or UseCaseException - the building blocks' own types excluded - and their instance fields, inherited ones declared in project classes included."
checks: "Informational diagnostic only: lists every field that involves - through its raw type or a type argument - a plain string, an aggregate or entity, or any other type that is neither assignable to the id or value role, nor a number, a primitive, an enum or a date and time type of the platform, and never fails. Container types such as lists are looked through. The message the base type carries is not a field of the project's failure and is not listed. A string that holds a code rather than display text is listed as well: the type does not tell the two apart, and the remedy is a typed value for the code."
enforced_by: "ErrorHandlingRules#DCA-ERR-007"
status: informational
maturity: experimental
rule_set: errors
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# Diagnostic: failures that carry display data or objects instead of ids and figures

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Concrete project classes assignable to DomainException or UseCaseException - the building blocks' own types excluded - and their instance fields, inherited ones declared in project classes included.

## Check

Informational diagnostic only: lists every field that involves - through its raw type or a type argument - a plain string, an aggregate or entity, or any other type that is neither assignable to the id or value role, nor a number, a primitive, an enum or a date and time type of the platform, and never fails. Container types such as lists are looked through. The message the base type carries is not a field of the project's failure and is not listed. A string that holds a code rather than display text is listed as well: the type does not tell the two apart, and the remedy is a typed value for the code.

## .NET reading

**Selection.** The project's own types below DomainException or UseCaseException, with their runtime type in the loaded assemblies, and the instance fields they and their project base types declare - the backing fields of auto-properties included.

**Check.** Informational diagnostic only: lists a field whose type is a plain string, or is assignable to IAggregateRoot or IEntity - directly, as an array element or as a generic type argument - and never fails. Ids, values, numbers and every other type pass. A string that holds a code rather than display text is listed as well: the type does not tell the two apart, and the remedy is a typed value for the code.

## Rust reading

Unpublished (dca-rust); planned, not yet implemented. **Held by** a lint or a test (source-test).

**Selection.** Types that implement DomainFailure or UseCaseFailure, their fields and variant fields.

**Check.** Informational - lists every field of type String, an aggregate or an entity, and never fails.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/errors/dca-err-007/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/errors/dca-err-007/overview.md)
- [`isProjectException`](/evidence/rule/errors/dca-err-007/isprojectexception.md)
- [`fieldFinding`](/evidence/rule/errors/dca-err-007/fieldfinding.md)
- [`TypeInspection.instanceFields`](/evidence/rule/errors/dca-err-007/typeinspection-instancefields.md)
- [`TypeInspection.involvedTypes`](/evidence/rule/errors/dca-err-007/typeinspection-involvedtypes.md)
- [`TypeInspection.collect`](/evidence/rule/errors/dca-err-007/typeinspection-collect.md)
- [`TypeInspection.typeArgumentBindings`](/evidence/rule/errors/dca-err-007/typeinspection-typeargumentbindings.md)
- [`TypeInspection.variableKey`](/evidence/rule/errors/dca-err-007/typeinspection-variablekey.md)
- [C# expression](/evidence/rule/errors/dca-err-007/c-expression.md)
