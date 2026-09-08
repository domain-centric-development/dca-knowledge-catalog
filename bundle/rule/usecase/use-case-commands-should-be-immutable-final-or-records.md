---
type: Rule
id: DCA-USE-004
title: "Use Case Commands should be immutable (final or records)"
rule: "Use case commands should be immutable (value objects)."
constraint: "Use Case Commands should be immutable (final or records)."
selects: "Non-interface, non-record classes in <module>.application.. whose simple name ends with Command."
checks: "The class is final. Records and interfaces are not selected, so a record Command always passes."
enforced_by: "UseCaseRules#DCA-USE-004"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

## Selection

Non-interface, non-record classes in <module>.application.. whose simple name ends with Command.

## Check

The class is final. Records and interfaces are not selected, so a record Command always passes.

## .NET reading

**Selection.** Non-record classes in <module>.Application of every module root whose name ends with Command.

**Check.** The class is sealed. Records and interfaces are not selected, so a record Command always passes; an abstract class is reported like any other unsealed class.

## Implementation

```java
DcaRule.of(
        "DCA-USE-004",
        "Use Case Commands should be immutable (final or records)",
        "Use case commands should be immutable (value objects)",
        arch -> immutableApplicationModels(arch, "Command"))
    .selecting(
        "Non-interface, non-record classes in <module>.application.. whose simple name ends with Command.")
    .checking(
        "The class is final. Records and interfaces are not selected, so a record Command always passes.")
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
