---
type: Rule
id: DCA-NAM-011
title: ViewModels must reside in adapter.incoming.web packages
rule: ViewModels are presentation concerns and must reside in incoming web adapter packages.
constraint: ViewModels must reside in adapter.incoming.web packages.
selects: Classes under the base package whose simple name ends with ViewModel.
checks: "Each resides in <module>.adapter.incoming.web.. of some module root - the adapter and incoming segments are the configured ones, the web segment is fixed. A ViewModel in a domain or application package, or in a non-web incoming adapter such as adapter.incoming.mcp, is reported. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-011"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

## Selection

Classes under the base package whose simple name ends with ViewModel.

## Check

Each resides in <module>.adapter.incoming.web.. of some module root - the adapter and incoming segments are the configured ones, the web segment is fixed. A ViewModel in a domain or application package, or in a non-web incoming adapter such as adapter.incoming.mcp, is reported. An empty selection passes.

## .NET reading

**Selection.** Types under the root namespace whose name ends with ViewModel.

**Check.** Each resides in <module>.Adapter.Incoming.Web of some module root - the adapter and incoming segments are the configured ones, the Web segment is fixed. A ViewModel in a domain or application namespace, or in a non-web incoming adapter such as Adapter.Incoming.Mcp, is reported. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-011",
        "ViewModels must reside in adapter.incoming.web packages",
        "ViewModels are presentation concerns and must reside in incoming web adapter packages",
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
        "Each resides in <module>.adapter.incoming.web.. of some module root - the adapter and"
            + " incoming segments are the configured ones, the web segment is fixed. A"
            + " ViewModel in a domain or application package, or in a non-web incoming adapter"
            + " such as adapter.incoming.mcp, is reported. An empty selection passes.")
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
                  + ".web..")
      .toArray(String[]::new);
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `layout()`, `moduleRoots()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
