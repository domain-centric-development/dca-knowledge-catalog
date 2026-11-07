---
type: Rule
id: DCA-ERR-009
title: A domain exception is constructed only in the domain layer
rule: "The model refuses: a domain exception names a business rule the model itself broke off. A use case never invents one. A failure the use case finds - an output port returned nothing, the caller does not own what it names, a precondition on a second aggregate - is the application's, a case of its result or a use-case exception; dressed as a domain failure it claims a rule the model never checked, and the model cannot know what a search found."
constraint: A domain exception is constructed only in the domain layer.
selects: "Every class of the scan outside <module>.domain.. of every module root - the application layer, the adapters, configuration and any unplaced class - with each constructor call and constructor reference it makes, lambdas, anonymous and nested classes included. Classes in the package of the configured domain-exception role are library code and not selected; test code is not imported."
checks: "No such call or reference creates a type assignable to the configured domain-exception role (by default DomainException of the building blocks). A subclass constructor chaining to its parent's constructor is not a construction - where a misplaced exception type lives is DCA-ERR-002's finding. Construction in the domain layer passes, a domain service and a factory included. A domain exception the application catches, wraps or rethrows is not constructed and passes. A construction through reflection or a generic factory method outside the domain is not seen. An empty selection passes."
enforced_by: "ErrorHandlingRules#DCA-ERR-009"
status: enforced
maturity: experimental
rule_set: errors
implementations: [java, dotnet, rust]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ErrorHandlingRules.java
tags: [errors, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/ErrorHandlingRules.cs
---

# A domain exception is constructed only in the domain layer

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Every class of the scan outside <module>.domain.. of every module root - the application layer, the adapters, configuration and any unplaced class - with each constructor call and constructor reference it makes, lambdas, anonymous and nested classes included. Classes in the package of the configured domain-exception role are library code and not selected; test code is not imported.

## Check

No such call or reference creates a type assignable to the configured domain-exception role (by default DomainException of the building blocks). A subclass constructor chaining to its parent's constructor is not a construction - where a misplaced exception type lives is DCA-ERR-002's finding. Construction in the domain layer passes, a domain service and a factory included. A domain exception the application catches, wraps or rethrows is not constructed and passes. A construction through reflection or a generic factory method outside the domain is not seen. An empty selection passes.

## .NET reading

**Selection.** Every type of the scan outside <Module>.Domain of every module root - the application layer, the adapters, configuration and any unplaced type - with each object creation its methods and constructors make, the compiler's async state machines, lambda closures and nested types included. Types in the namespace of the configured domain-exception role are library code and not selected; test assemblies are not loaded.

**Check.** No such creation (a newobj instruction) creates a type assignable to the configured domain-exception role (by default DomainException of the building blocks). A constructor chaining to its base constructor is not a creation - where a misplaced exception type lives is DCA-ERR-002's finding. Construction in the domain layer passes, a domain service and a factory included. A domain exception the application catches, wraps or rethrows is not constructed and passes. A construction through reflection or a generic factory method outside the domain is not seen. An empty selection passes.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a lint or a test (source-test).

**Selection.** Every expression in a function body of a module outside the domain crates - application, adapters, api, infrastructure, bootstrap and unplaced crates; #[cfg(test)] items and test targets are not read: a struct literal, a call of a tuple struct or an enum variant, a unit struct or unit variant used as a value, a variant or tuple struct passed as a function, and a call of an associated function without a receiver that returns Self or the type itself, whose type implements DomainFailure.

**Check.** None of them names a domain failure - only a domain crate constructs one. Self is not followed: a domain failure declared outside the domain is DCA-ERR-002's finding. A failure the application only passes on (a variant wrapping it, ? or map_err with a conversion) is not a construction. Constructions inside macro invocations, through From/Into conversions or a generic constructor are not seen. An empty selection passes.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/errors/dca-err-009/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `inDomain()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Related mentions (heuristic)

- [DomainException](/marker/tactical/domainexception.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/errors/dca-err-009/overview.md)
- [`chainsTo`](/evidence/rule/errors/dca-err-009/chainsto.md)
- [`CollectedViolations.check`](/evidence/rule/errors/dca-err-009/collectedviolations-check.md)
- [`CollectedViolations.withHeader`](/evidence/rule/errors/dca-err-009/collectedviolations-withheader.md)
- [`CollectedViolations.addAll`](/evidence/rule/errors/dca-err-009/collectedviolations-addall.md)
- [`CollectedViolations.add`](/evidence/rule/errors/dca-err-009/collectedviolations-add.md)
- [`CollectedViolations.throwIfAny`](/evidence/rule/errors/dca-err-009/collectedviolations-throwifany.md)
- [`CollectedViolations.withoutHeader`](/evidence/rule/errors/dca-err-009/collectedviolations-withoutheader.md)
- [`CollectedViolations.isEmpty`](/evidence/rule/errors/dca-err-009/collectedviolations-isempty.md)
- [C# expression](/evidence/rule/errors/dca-err-009/c-expression.md)
- [C# helper IntraClassCalls](/evidence/rule/errors/dca-err-009/c-helper-intraclasscalls.md)
