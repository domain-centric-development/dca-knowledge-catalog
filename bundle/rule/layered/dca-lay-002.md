---
type: Rule
id: DCA-LAY-002
title: Domain must not have dependencies on Infrastructure
rule: "Domain should not depend on infrastructure concerns (Dependency Inversion Principle)."
constraint: Domain must not have dependencies on Infrastructure.
selects: "Classes in <module>.domain.. of every module root, the shared kernel's domain included."
checks: "No dependency on a class in the global infrastructure package (<base>.infrastructure..) or in any module's own infrastructure package (<module>.infrastructure..). The shared kernel's infrastructure package is not in that list. A module without a domain layer selects nothing and passes."
enforced_by: "LayeredRules#DCA-LAY-002"
status: enforced
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/LayeredRules.cs
---

# Domain must not have dependencies on Infrastructure

## Selection

Classes in <module>.domain.. of every module root, the shared kernel's domain included.

## Check

No dependency on a class in the global infrastructure package (<base>.infrastructure..) or in any module's own infrastructure package (<module>.infrastructure..). The shared kernel's infrastructure package is not in that list. A module without a domain layer selects nothing and passes.

## .NET reading

**Selection.** Types in <module>.Domain of every module root, the shared kernel's domain included.

**Check.** No dependency on a type in the global infrastructure namespace (<root>.Infrastructure or below) or in any isolated module's own infrastructure namespace (<module>.Infrastructure or below). The shared kernel's infrastructure namespace is not in that list. A module without a domain layer selects nothing and passes.

## Implementation

```java
DcaRule.of(
        "DCA-LAY-002",
        "Domain must not have dependencies on Infrastructure",
        "Domain should not depend on infrastructure concerns (Dependency Inversion Principle)",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allDomainPatterns())
                .should()
                .dependOnClassesThat()
                // The global infrastructure package and every module's own one.
                .resideInAnyPackage(arch.allInfrastructurePatterns())
                // A context may legitimately have no domain layer at all - a supporting or
                // generic
                // subdomain in transaction-script style. An absent domain is not a violation.
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.domain.. of every module root, the shared kernel's domain"
            + " included.")
    .checking(
        "No dependency on a class in the global infrastructure package"
            + " (<base>.infrastructure..) or in any module's own infrastructure package"
            + " (<module>.infrastructure..). The"
            + " shared kernel's infrastructure package is not in that list. A module without a"
            + " domain layer selects nothing and passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()`, `allInfrastructurePatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
    "DCA-LAY-002",
    "Domain must not have dependencies on Infrastructure",
    "Domain should not depend on infrastructure concerns (Dependency Inversion Principle)",
    // The global infrastructure namespace and every isolated module's own.
    arch => Types().That().ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllDomainPatterns()))
        .Should().NotDependOnAnyTypesThat().ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllInfrastructurePatterns())))
    .Selecting(
        "Types in <module>.Domain of every module root, the shared kernel's domain included.")
    .Checking(
        "No dependency on a type in the global infrastructure namespace (<root>.Infrastructure or "
        + "below) or in any isolated module's own infrastructure namespace (<module>.Infrastructure "
        + "or below). The shared kernel's infrastructure namespace is not in that list. A module "
        + "without a domain layer selects nothing and passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
