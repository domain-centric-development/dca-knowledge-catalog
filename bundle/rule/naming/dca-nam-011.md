---
type: Rule
id: DCA-NAM-011
title: ViewModels must reside in the configured web adapter package
rule: "A ViewModel is shaped for the protocol of one incoming adapter and belongs in it. It has no reading in the domain or the application layer, and none in a second adapter."
constraint: ViewModels must reside in the configured web adapter package.
selects: Classes under the base package whose simple name ends with ViewModel.
checks: "Each resides in <module>.adapter.incoming.<web>.. of some module root - all three segments are the configured ones (withWebSubpackage changes the last). A ViewModel in a domain or application package, or in an incoming adapter other than the configured web one, such as adapter.incoming.mcp, is reported. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-011"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# ViewModels must reside in the configured web adapter package

## Selection

Classes under the base package whose simple name ends with ViewModel.

## Check

Each resides in <module>.adapter.incoming.<web>.. of some module root - all three segments are the configured ones (withWebSubpackage changes the last). A ViewModel in a domain or application package, or in an incoming adapter other than the configured web one, such as adapter.incoming.mcp, is reported. An empty selection passes.

## .NET reading

**Selection.** Types under the root namespace whose name ends with ViewModel.

**Check.** Each resides in <module>.Adapter.Incoming.<Web> of some module root - all three segments are the configured ones (WithWebSegment changes the last). A ViewModel in a domain or application namespace, or in an incoming adapter other than the configured web one, such as Adapter.Incoming.Mcp, is reported. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-011",
        "ViewModels must reside in the configured web adapter package",
        "A ViewModel is shaped for the protocol of one incoming adapter and belongs in it. It has"
            + " no reading in the domain or the application layer, and none in a second"
            + " adapter",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("ViewModel")
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .should()
                .resideInAnyPackage(incomingWebAdapterPatterns(arch))
                .allowEmptyShould(true))
    .selecting("Classes under the base package whose simple name ends with ViewModel.")
    .checking(
        "Each resides in <module>.adapter.incoming.<web>.. of some module root - all three"
            + " segments are the configured ones (withWebSubpackage changes the last). A"
            + " ViewModel in a domain or application package, or in an incoming adapter other"
            + " than the configured web one, such as adapter.incoming.mcp, is reported. An"
            + " empty selection passes.")
```

## Helpers

### `incomingWebAdapterPatterns`

```java
private static String[] incomingWebAdapterPatterns(DcaArchitecture arch) {
  DcaLayout layout = arch.layout();
  return arch.moduleRoots().stream()
      .map(
          root ->
              root
                  + "."
                  + layout.adapterSubpackage()
                  + "."
                  + layout.incomingSubpackage()
                  + "."
                  + layout.webSubpackage()
                  + "..")
      .toArray(String[]::new);
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `layout()`, `moduleRoots()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-NAM-011",
        "ViewModels must reside in the configured web adapter namespace",
        "A ViewModel is shaped for the protocol of one incoming adapter and belongs in it. It has no"
        + " reading in the domain or the application layer, and none in a second adapter",
        arch =>
            Types()
                .That()
                .HaveNameEndingWith("ViewModel")
                .And()
                .ResideInNamespaceMatching(DcaLayout.Below(layout.RootNamespace))
                .Should()
                .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.ModuleRoots().Select(root =>
                    DcaLayout.Below($"{root}.{layout.AdapterSegment}.{layout.IncomingSegment}.{layout.WebSegment}")))))
    .Selecting(
        "Types under the root namespace whose name ends with ViewModel.")
    .Checking(
        "Each resides in <module>.Adapter.Incoming.<Web> of some module root - all three"
            + " segments are the configured ones (WithWebSegment changes the last). A"
            + " ViewModel in a domain or application namespace, or in an incoming adapter"
            + " other than the configured web one, such as Adapter.Incoming.Mcp, is"
            + " reported. An empty selection passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
