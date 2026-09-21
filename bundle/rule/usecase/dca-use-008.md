---
type: Rule
id: DCA-USE-008
title: "Types named *Response reside in an adapter"
rule: HTTP response models should be in adapter layer.
constraint: "Types named *Response reside in an adapter."
selects: Classes under the base package whose simple name ends with Response.
checks: "Each resides in an adapter package of some module root (<module>.adapter..), the shared kernel's included."
enforced_by: "UseCaseRules#DCA-USE-008"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Types named *Response reside in an adapter

## Selection

Classes under the base package whose simple name ends with Response.

## Check

Each resides in an adapter package of some module root (<module>.adapter..), the shared kernel's included.

## .NET reading

**Selection.** Types under the root namespace whose name ends with Response.

**Check.** Each resides in an adapter namespace (incoming or outgoing) of some module root (<module>.Adapter or below), the shared kernel's included.

## Implementation

```java
DcaRule.of(
        "DCA-USE-008",
        "Types named *Response reside in an adapter",
        "HTTP response models should be in adapter layer",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Response")
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .should()
                .resideInAnyPackage(arch.allAdapterPatterns())
                .allowEmptyShould(true))
    .selecting("Classes under the base package whose simple name ends with Response.")
    .checking(
        "Each resides in an adapter package of some module root (<module>.adapter..), the shared kernel's included.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-008",
        "Types named *Response reside in an adapter",
        "HTTP response models should be in adapter layer",
        arch =>
            Types()
                .That()
                .HaveNameEndingWith("Response")
                .And()
                .ResideInNamespaceMatching(DcaLayout.Below(layout.RootNamespace))
                .Should()
                .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllAdapterPatterns())))
    .Selecting(
        "Types under the root namespace whose name ends with Response.")
    .Checking(
        "Each resides in an adapter namespace (incoming or outgoing) of some module root"
            + " (<module>.Adapter or below), the shared kernel's included.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
