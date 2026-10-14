---
type: Rule
id: DCA-HEX-016
title: "Diagnostic: adapters that publish an enum by its member name"
rule: A value an adapter publishes from an enum is spelled explicitly - a code per value on the enum or a mapping in the adapter - never derived from the member's name. Renaming a member is a refactoring inside the code and must not change what a client reads.
constraint: "Diagnostic: adapters that publish an enum by its member name."
selects: "Classes in <module>.adapter.. of every module root, incoming and outgoing, and their method calls whose target is an enum declared in <module>.domain.. or <module>.application.."
checks: "Informational diagnostic only: lists every call of name() or toString() on such an enum, and never fails. A member name reached through string concatenation or formatting, or a serializer that writes the name on its own, is not visible in the import model and is not listed; whether the value leaves the process is not established either."
enforced_by: "HexagonalRules#DCA-HEX-016"
status: informational
maturity: experimental
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Diagnostic: adapters that publish an enum by its member name

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes in <module>.adapter.. of every module root, incoming and outgoing, and their method calls whose target is an enum declared in <module>.domain.. or <module>.application..

## Check

Informational diagnostic only: lists every call of name() or toString() on such an enum, and never fails. A member name reached through string concatenation or formatting, or a serializer that writes the name on its own, is not visible in the import model and is not listed; whether the value leaves the process is not established either.

## .NET reading

**Selection.** Non-nested types in <module>.Adapter of every module root, incoming and outgoing, with their runtime type in the loaded assemblies, together with their nested, async state-machine and closure types; enums declared in a domain or application namespace of any module root.

**Check.** Informational diagnostic only: lists a method that turns such an enum into its member name as the IL shows it - ToString in any overload, called through a constrained call or on the boxed value; the boxed value passed straight into a string-building call (concatenation, formatting, joining, appending); an interpolation hole of the enum type; Enum.GetName or Enum.GetNames over it - and never fails. Compiler-generated methods, such as a record's generated PrintMembers and ToString, are not read. A boxed value stored first and formatted later, a serializer that writes names, and a name read through a generic helper are not seen; whether the text reaches a client stays with review.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/hexagonal/dca-hex-016/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allAdapterPatterns()`, `allApplicationPatterns()`, `allDomainPatterns()`, `classes()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/hexagonal/dca-hex-016/overview.md)
- [`name`](/evidence/rule/hexagonal/dca-hex-016/name.md)
- [C# expression](/evidence/rule/hexagonal/dca-hex-016/c-expression.md)
- [C# helper IntraClassCalls](/evidence/rule/hexagonal/dca-hex-016/c-helper-intraclasscalls.md)
