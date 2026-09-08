---
type: Rule
id: DCA-ONI-001
title: "Domain must not access Application Services (Onion Architecture - Domain is innermost layer)"
rule: Domain is the innermost layer in onion architecture and should not depend on application services.
constraint: "Domain must not access Application Services (Onion Architecture - Domain is innermost layer)."
selects: "Classes in <module>.domain.. of every module root."
checks: "No dependency on a class in an application package of any module root (<module>.application..), the module's own included. Dependencies on adapters or infrastructure are covered by other rules, not this one."
enforced_by: "OnionRules#DCA-ONI-001"
status: enforced
rule_set: onion
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/OnionRules.java
tags: [onion, archunit]
---

## Selection

Classes in <module>.domain.. of every module root.

## Check

No dependency on a class in an application package of any module root (<module>.application..), the module's own included. Dependencies on adapters or infrastructure are covered by other rules, not this one.

## .NET reading

**Selection.** Types whose namespace lies under <Module>.Domain of every module root - declared bounded contexts, the shared kernel when it owns a domain layer, and undeclared modules alike, at any depth below the root namespace.

**Check.** No dependency on a type whose namespace lies under <Module>.Application of any module root, the module's own included. Dependencies on adapters or infrastructure are covered by other rules, not this one; an empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ONI-001",
        "Domain must not access Application Services (Onion Architecture - Domain is innermost"
            + " layer)",
        "Domain is the innermost layer in onion architecture and should not depend on application"
            + " services",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allDomainPatterns())
                .should()
                .dependOnClassesThat()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .allowEmptyShould(true))
    .selecting("Classes in <module>.domain.. of every module root.")
    .checking(
        "No dependency on a class in an application package of any module root"
            + " (<module>.application..), the module's own included. Dependencies on adapters"
            + " or infrastructure are covered by other rules, not this one.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
