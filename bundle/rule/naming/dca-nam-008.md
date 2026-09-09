---
type: Rule
id: DCA-NAM-008
title: Converters must reside in the adapter layer
rule: Converters/Mappers translate between layers and should be in adapters.
constraint: Converters must reside in the adapter layer.
selects: Classes under the base package whose simple name ends with Converter.
checks: "Each resides in an adapter package of some module root (<module>.adapter..), incoming or outgoing. Only the Converter suffix is checked - a class named *Mapper or *Assembler is not selected by this rule. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-008"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# Converters must reside in the adapter layer

## Selection

Classes under the base package whose simple name ends with Converter.

## Check

Each resides in an adapter package of some module root (<module>.adapter..), incoming or outgoing. Only the Converter suffix is checked - a class named *Mapper or *Assembler is not selected by this rule. An empty selection passes.

## .NET reading

**Selection.** Types under the root namespace whose name ends with Converter.

**Check.** Each resides in an adapter namespace of some module root (<module>.Adapter or below), incoming or outgoing. Only the Converter suffix is checked - a type named *Mapper or *Assembler is not selected by this rule. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-008",
        "Converters must reside in the adapter layer",
        "Converters/Mappers translate between layers and should be in adapters",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Converter")
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .should()
                .resideInAnyPackage(arch.allAdapterPatterns())
                .allowEmptyShould(true))
    .selecting("Classes under the base package whose simple name ends with Converter.")
    .checking(
        "Each resides in an adapter package of some module root (<module>.adapter..), incoming"
            + " or outgoing. Only the Converter suffix is checked - a class named *Mapper or"
            + " *Assembler is not selected by this rule. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-NAM-008",
        "Converters must reside in the adapter layer",
        "Converters/Mappers translate between layers and should be in adapters",
        arch =>
            Types()
                .That()
                .HaveNameEndingWith("Converter")
                .And()
                .ResideInNamespaceMatching(DcaLayout.Below(layout.RootNamespace))
                .Should()
                .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllAdapterPatterns())))
    .Selecting(
        "Types under the root namespace whose name ends with Converter.")
    .Checking(
        "Each resides in an adapter namespace of some module root (<module>.Adapter or"
            + " below), incoming or outgoing. Only the Converter"
            + " suffix is checked - a type named *Mapper or *Assembler is not selected by this"
            + " rule. An empty selection passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
