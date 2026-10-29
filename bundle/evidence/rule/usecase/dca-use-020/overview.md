---
type: Reference
title: Use cases must not parse raw input into an id — Overview
tags: [reference]
evidence_for: /rule/usecase/dca-use-020.md
---

[Full node and context](/rule/usecase/dca-use-020.md). This is an evidence excerpt; retain the parent selection and caveats.

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

```java
DcaRule.of(
        "DCA-USE-020",
        "Use cases must not parse raw input into an id",
        "The adapter turns raw input into the types the input port takes: an id arrives as the"
            + " id's value type, parsed at the edge or by the value type's own factory, never as"
            + " text the use case parses. Text that does not parse is a malformed call the"
            + " adapter answers itself; the use case never sees it",
        arch ->
            noClasses()
                .that(arch.inApplication())
                .should()
                .callMethod(java.util.UUID.class, "fromString", String.class)
                .allowEmptyShould(true))
    .experimental()
    .selecting("Classes in <module>.application.. of every module root.")
    .checking(
        "No code unit calls the platform's parse API for a universally unique identifier -"
            + " java.util.UUID.fromString(String). Parsing through another API, or through the"
            + " id's value type called from the use case, is not reported. An empty selection"
            + " passes.",
        "take the id's value type in the command and parse the text in the adapter")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
