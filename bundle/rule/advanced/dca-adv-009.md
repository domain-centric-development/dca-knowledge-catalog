---
type: Rule
id: DCA-ADV-009
title: Marked domain services reside in the configured domain service segment
rule: "Domain services implement DomainService marker and reside in domain.service packages (named descriptively, e.g., PricingService, CartTotalCalculator)."
constraint: Marked domain services reside in the configured domain service segment.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to DomainService.
checks: "Each resides in a package matching ..<domain subpackage>.service.. - the configured domain subpackage followed by service, anywhere in the package path, not tied to a module root. A domain service directly in domain or in domain.model is reported. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-009"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Marked domain services reside in the configured domain service segment

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainService.

## Check

Each resides in a package matching ..<domain subpackage>.service.. - the configured domain subpackage followed by service, anywhere in the package path, not tied to a module root. A domain service directly in domain or in domain.model is reported. An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainService.

**Check.** Each resides in a namespace matching .<domain segment>.Service or below - the configured domain segment followed by Service, anywhere in the namespace path, not tied to a module root. A domain service directly in Domain or in Domain.Model is reported. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-009",
        "Marked domain services reside in the configured domain service segment",
        "Domain services implement DomainService marker and reside in domain.service packages"
            + " (named descriptively, e.g., PricingService, CartTotalCalculator)",
        arch ->
            classes()
                .that()
                .implement(DomainService.class)
                .and()
                .areNotInterfaces()
                .should()
                .resideInAPackage(".." + layout.domainSubpackage() + ".service..")
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to"
            + " DomainService.")
    .checking(
        "Each resides in a package matching ..<domain subpackage>.service.. - the configured domain"
            + " subpackage followed by service, anywhere in the package path, not tied to a module root. A"
            + " domain service directly in domain or in domain.model is reported. An empty selection passes.")
```
### C# expression

```csharp
DcaRule.Of(
    "DCA-ADV-009",
    "Marked domain services reside in the configured domain service segment",
    "Domain services implement IDomainService marker and reside in Domain.Service namespaces"
        + " (named descriptively, e.g., PricingService, CartTotalCalculator)",
    arch => Types()
        .That()
        .AreAssignableTo(typeof(IDomainService))
        .And()
        .FollowCustomPredicate(t => t is not Interface, "are not interfaces")
        .Should()
        .ResideInNamespaceMatching(DomainServicePattern()))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to IDomainService.")
    .Checking(
        "Each resides in a namespace matching .<domain segment>.Service or below - the configured "
        + "domain segment followed by Service, anywhere in the namespace path, not tied to a module "
        + "root. A domain service directly in Domain or in Domain.Model is reported. An empty "
        + "selection passes.")
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
