---
type: Rule
id: DCA-NAM-010
title: "Domain classes must not use technical suffixes (Helper, Util, Impl, Implementation)"
rule: "Domain names come from the ubiquitous language - name services by their specialty, not by technical role."
constraint: "Domain classes must not use technical suffixes (Helper, Util, Impl, Implementation)."
selects: "Classes in <module>.domain.. of every module root."
checks: "No simple name ends with Helper, Util, Utils, Impl or Implementation. Only these five suffixes are checked, only in domain packages - a *Service or *Factory in the domain is not reported, and an Impl in an adapter package is not checked. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-010"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# Domain classes must not use technical suffixes (Helper, Util, Impl, Implementation)

## Selection

Classes in <module>.domain.. of every module root.

## Check

No simple name ends with Helper, Util, Utils, Impl or Implementation. Only these five suffixes are checked, only in domain packages - a *Service or *Factory in the domain is not reported, and an Impl in an adapter package is not checked. An empty selection passes.

## .NET reading

**Selection.** Types in <module>.Domain of every module root.

**Check.** No name ends with Helper, Util, Utils, Impl or Implementation. Only these five suffixes are checked, only in domain namespaces - a *Service or *Factory in the domain is not reported, and an Impl in an adapter namespace is not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-010",
        "Domain classes must not use technical suffixes (Helper, Util, Impl, Implementation)",
        "Domain names come from the ubiquitous language - name services by their specialty, not by"
            + " technical role",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allDomainPatterns())
                .should()
                .haveSimpleNameEndingWith("Helper")
                .orShould()
                .haveSimpleNameEndingWith("Util")
                .orShould()
                .haveSimpleNameEndingWith("Utils")
                .orShould()
                .haveSimpleNameEndingWith("Impl")
                .orShould()
                .haveSimpleNameEndingWith("Implementation")
                .allowEmptyShould(true))
    .selecting("Classes in <module>.domain.. of every module root.")
    .checking(
        "No simple name ends with Helper, Util, Utils, Impl or Implementation. Only these five"
            + " suffixes are checked, only in domain packages - a *Service or *Factory in the"
            + " domain is not reported, and an Impl in an adapter package is not checked. An"
            + " empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-NAM-010",
        "Domain classes must not use technical suffixes (Helper, Util, Impl)",
        "Domain names come from the ubiquitous language - name services by their specialty, not by technical role",
        arch =>
            Types()
                .That()
                .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllDomainPatterns()))
                .Should()
                .NotHaveNameMatching("(Helper|Utils?|Impl|Implementation)$"))
    .Selecting(
        "Types in <module>.Domain of every module root.")
    .Checking(
        "No name ends with Helper, Util, Utils, Impl or Implementation. Only"
            + " these five suffixes are checked, only in domain namespaces - a *Service or"
            + " *Factory in the domain is not reported, and an Impl in an adapter namespace is"
            + " not checked. An empty selection passes.")
```

## Related mentions (heuristic)

- [Factory](/marker/tactical/factory.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
