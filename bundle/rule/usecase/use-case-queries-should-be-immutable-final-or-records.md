---
type: Rule
id: DCA-USE-005
title: "Use Case Queries should be immutable (final or records)"
rule: "Use case queries should be immutable (value objects)."
constraint: "Use Case Queries should be immutable (final or records)."
selects: "Non-interface, non-record classes in <module>.application.. whose simple name ends with Query."
checks: The class is final. Records and interfaces are not selected.
enforced_by: "UseCaseRules#DCA-USE-005"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

## Selection

Non-interface, non-record classes in <module>.application.. whose simple name ends with Query.

## Check

The class is final. Records and interfaces are not selected.

## .NET reading

**Selection.** Non-record classes in <module>.Application of every module root whose name ends with Query.

**Check.** The class is sealed. Records and interfaces are not selected.

## Implementation

```java
DcaRule.of(
        "DCA-USE-005",
        "Use Case Queries should be immutable (final or records)",
        "Use case queries should be immutable (value objects)",
        arch -> immutableApplicationModels(arch, "Query"))
    .selecting(
        "Non-interface, non-record classes in <module>.application.. whose simple name ends with Query.")
    .checking("The class is final. Records and interfaces are not selected.")
```

## Helpers

### `immutableApplicationModels`

```java
private static com.tngtech.archunit.lang.ArchRule immutableApplicationModels(
    DcaArchitecture arch, String suffix) {
  return classes()
      .that()
      .haveSimpleNameEndingWith(suffix)
      .and()
      .resideInAnyPackage(arch.allApplicationPatterns())
      .and()
      .areNotInterfaces()
      .and()
      .areNotRecords()
      .should()
      .haveModifier(JavaModifier.FINAL)
      .allowEmptyShould(true);
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
