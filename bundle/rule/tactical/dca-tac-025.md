---
type: Rule
id: DCA-TAC-025
title: "Domain types must not hold bare primitives, strings or time types"
rule: "A value with rules of its own - a postal code, a quantity, a status, a moment, an identifier - is a value object; held as a bare String, int, boolean, Instant or UUID its validation is repeated at every use or missing. A value object with several components holds value objects too; only a wrapper - a value of exactly one component - holds the primitive it wraps."
constraint: "Domain types must not hold bare primitives, strings or time types."
selects: "Classes, records, enums and interfaces in <module>.domain.. of every module root, the shared kernel's domain included - their instance fields and their methods, private ones included; constructors are not selected, the fields they fill are. Not selected: a wrapper value - a type assignable to the value or the id role with exactly one instance field - with everything it declares; synthetic and bridge members; equals, hashCode, toString and compareTo; the values() and valueOf(String) the language declares on an enum; a method that implements a method of a building block, such as a domain event's occurredOn() or a specification's isSatisfiedBy, and the field of the same name behind it. A boolean return is a question to the object - a predicate - and passes; a boolean field or parameter does not."
checks: "No selected field, return type or parameter type involves String, a primitive or its box, or a point in time (java.time.Instant, LocalDate, LocalDateTime, LocalTime, OffsetDateTime, ZonedDateTime, java.util.Date), nor a bare java.util.UUID - an identifier says whose it is through a typed id - generic type arguments included, so List<String> counts. BigDecimal, BigInteger, Duration and the project's own types pass. A value object with several components is checked like any other type: each component is a value object itself. A record's accessor is not reported again beside its field. An empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-025"
status: enforced
maturity: experimental
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Domain types must not hold bare primitives, strings or time types

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes, records, enums and interfaces in <module>.domain.. of every module root, the shared kernel's domain included - their instance fields and their methods, private ones included; constructors are not selected, the fields they fill are. Not selected: a wrapper value - a type assignable to the value or the id role with exactly one instance field - with everything it declares; synthetic and bridge members; equals, hashCode, toString and compareTo; the values() and valueOf(String) the language declares on an enum; a method that implements a method of a building block, such as a domain event's occurredOn() or a specification's isSatisfiedBy, and the field of the same name behind it. A boolean return is a question to the object - a predicate - and passes; a boolean field or parameter does not.

## Check

No selected field, return type or parameter type involves String, a primitive or its box, or a point in time (java.time.Instant, LocalDate, LocalDateTime, LocalTime, OffsetDateTime, ZonedDateTime, java.util.Date), nor a bare java.util.UUID - an identifier says whose it is through a typed id - generic type arguments included, so List<String> counts. BigDecimal, BigInteger, Duration and the project's own types pass. A value object with several components is checked like any other type: each component is a value object itself. A record's accessor is not reported again beside its field. An empty selection passes.

## .NET reading

**Selection.** Classes, records, structs, enums and interfaces in <Module>.Domain of every module root, the shared kernel's domain included, with their runtime type in the loaded assemblies - their declared instance fields and properties and their declared methods, private ones included; constructors are not selected, the members they fill are. Not selected: a wrapper value - a type assignable to IValue or IId with exactly one instance field - with everything it declares; compiler- generated members (a property's backing field, a record's EqualityContract, Deconstruct, PrintMembers); property accessors and operators; Equals, GetHashCode, ToString and CompareTo; an enum's members; a member that implements a building block's, such as a domain event's OccurredOn and EventId. A bool return is a question to the object - a predicate - and passes; a bool field, property or parameter does not.

**Check.** No selected field, property, return type or parameter type involves string, bool, a numeric primitive or char, a point in time (DateTime, DateTimeOffset, DateOnly, TimeOnly), or a bare Guid - an identifier says whose it is through a typed id - nullable and generic arguments and arrays included, so IReadOnlyList<string> counts. decimal, TimeSpan and the project's own types pass. A value object with several components is checked like any other type: each component is a value object itself. An empty selection passes.

## Implementation

The verbatim ArchUnit expression is in the evidence slice [Overview](/evidence/rule/tactical/dca-tac-025/overview.md); every helper it calls has a slice of its own, listed under *Evidence slices* below.

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()`, `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/rule/tactical/dca-tac-025/overview.md)
- [`buildingBlockTypes`](/evidence/rule/tactical/dca-tac-025/buildingblocktypes.md)
- [`classesMatching`](/evidence/rule/tactical/dca-tac-025/classesmatching.md)
- [`isWrapperValue`](/evidence/rule/tactical/dca-tac-025/iswrappervalue.md)
- [`implementsBuildingBlock`](/evidence/rule/tactical/dca-tac-025/implementsbuildingblock.md)
- [`bareTypesIn`](/evidence/rule/tactical/dca-tac-025/baretypesin.md)
- [`isEnumImplicit`](/evidence/rule/tactical/dca-tac-025/isenumimplicit.md)
- [`fail`](/evidence/rule/tactical/dca-tac-025/fail.md)
- [`isEnumValueOf`](/evidence/rule/tactical/dca-tac-025/isenumvalueof.md)
- [C# expression](/evidence/rule/tactical/dca-tac-025/c-expression.md)
