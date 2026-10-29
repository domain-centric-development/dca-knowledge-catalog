---
type: Rule
id: DCA-USE-020
title: Use cases must not parse raw input into an id
rule: "The adapter turns raw input into the types the input port takes: an id arrives as the id's value type, parsed at the edge or by the value type's own factory, never as text the use case parses. Text that does not parse is a malformed call the adapter answers itself; the use case never sees it."
constraint: Use cases must not parse raw input into an id.
selects: "Classes in <module>.application.. of every module root."
checks: "No code unit calls the platform's parse API for a universally unique identifier - java.util.UUID.fromString(String). Parsing through another API, or through the id's value type called from the use case, is not reported. An empty selection passes."
enforced_by: "UseCaseRules#DCA-USE-020"
status: enforced
maturity: experimental
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Use cases must not parse raw input into an id

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes in <module>.application.. of every module root.

## Check

No code unit calls the platform's parse API for a universally unique identifier - java.util.UUID.fromString(String). Parsing through another API, or through the id's value type called from the use case, is not reported. An empty selection passes.

## .NET reading

**Selection.** Non-nested types in <module>.Application of every module root with their runtime type in the loaded assemblies - use cases, helpers and application services alike - together with their nested, async state-machine and closure types.

**Check.** No method calls the platform's parse API for a unique identifier: System.Guid.Parse, TryParse, ParseExact or TryParseExact, in any overload. Parsing a project's own id type, or an id held as a number or another text format, is not seen; the value type's own factory in the domain is outside the selection and may parse. An empty selection passes.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/usecase/dca-use-020/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/usecase/dca-use-020/overview.md)
- [C# expression](/evidence/rule/usecase/dca-use-020/c-expression.md)
- [C# helper IntraClassCalls](/evidence/rule/usecase/dca-use-020/c-helper-intraclasscalls.md)
