---
type: Rule
id: DCA-HEX-006
title: Incoming port adapters must not depend directly on outgoing port adapters within the same context
rule: "Port adapters should communicate through application services, not directly (event consumers are the exception)."
constraint: Incoming port adapters must not depend directly on outgoing port adapters within the same context.
selects: "Classes in <module>.adapter.incoming.. of every module root, excluding those below an adapter.incoming.event package (event consumers)."
checks: "No dependency on a class in <module>.adapter.outgoing.. of any module root. The reverse direction (an outgoing adapter using an incoming one) and dependencies between two incoming or two outgoing adapters are not checked. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-006"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/HexagonalRules.cs
---

# Incoming port adapters must not depend directly on outgoing port adapters within the same context

## Selection

Classes in <module>.adapter.incoming.. of every module root, excluding those below an adapter.incoming.event package (event consumers).

## Check

No dependency on a class in <module>.adapter.outgoing.. of any module root. The reverse direction (an outgoing adapter using an incoming one) and dependencies between two incoming or two outgoing adapters are not checked. An empty selection passes.

## .NET reading

**Selection.** Types in <module>.Adapter.Incoming of every module root, excluding those below an Adapter.Incoming.Event namespace (event consumers).

**Check.** No dependency on a type in <module>.Adapter.Outgoing of any module root. The reverse direction (an outgoing adapter using an incoming one) and dependencies between two incoming or two outgoing adapters are not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-006",
        "Incoming port adapters must not depend directly on outgoing port adapters"
            + " within the same context",
        "Port adapters should communicate through application services, not directly (event"
            + " consumers are the exception)",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .and()
                .resideOutsideOfPackage(eventConsumerPattern())
                .should()
                .dependOnClassesThat()
                .resideInAnyPackage(arch.allOutgoingAdapterPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.adapter.incoming.. of every module root, excluding those"
            + " below an adapter.incoming.event package (event consumers).")
    .checking(
        "No dependency on a class in <module>.adapter.outgoing.. of any module root. The"
            + " reverse direction (an outgoing adapter using an incoming one) and dependencies"
            + " between two incoming or two outgoing adapters are not checked. An empty"
            + " selection passes.")
```

## Helpers

### `eventConsumerPattern`

```java
/** Pattern of event consumers, which may depend on other contexts' integration events. */
  private String eventConsumerPattern() {
    return ".." + layout.adapterSubpackage() + "." + layout.incomingSubpackage() + ".event..";
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()`, `allOutgoingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-HEX-006",
        "Incoming port adapters must not depend directly on outgoing port adapters"
            + " within the same context",
        "Port adapters should communicate through application services, not directly (event"
            + " consumers are the exception)",
        arch => Types().That().ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllIncomingAdapterPatterns()))
            .And().DoNotResideInNamespaceMatching(EventConsumerPattern())
            .Should().NotDependOnAnyTypesThat().ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllOutgoingAdapterPatterns())))
    .Selecting(
        "Types in <module>.Adapter.Incoming of every module root, excluding those"
            + " below an Adapter.Incoming.Event namespace (event consumers).")
    .Checking(
        "No dependency on a type in <module>.Adapter.Outgoing of any module root. The"
            + " reverse direction (an outgoing adapter using an incoming one) and dependencies"
            + " between two incoming or two outgoing adapters are not checked. An empty"
            + " selection passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
