---
type: Rule
id: DCA-ONI-002
title: The Domain Model should be framework independent and should not use 3rd party libraries when possible
rule: "Domain should be framework-independent (Dependency Inversion Principle)."
constraint: The Domain Model should be framework independent and should not use 3rd party libraries when possible.
selects: "Classes in <module>.domain.. of every module root, plus the classes of the building-blocks packages ddd.tactical.. and hexagonal.port.out.. when they are on the classpath under scan."
checks: "Every dependency targets a class in one of those same packages or in an allowed third-party package: by default java.., lombok.., org.apache.commons.lang3.., org.apache.commons.collections4.. and org.jspecify.annotations.., plus whatever the layout adds. The building-blocks strategic and port.in packages are not on the list, nor is the shared kernel unless it is a module root with a domain layer of its own. A dependency on any other package is reported."
enforced_by: "OnionRules#DCA-ONI-002"
status: enforced
rule_set: onion
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/OnionRules.java
tags: [onion, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/OnionRules.cs
---

# The Domain Model should be framework independent and should not use 3rd party libraries when possible

## Selection

Classes in <module>.domain.. of every module root, plus the classes of the building-blocks packages ddd.tactical.. and hexagonal.port.out.. when they are on the classpath under scan.

## Check

Every dependency targets a class in one of those same packages or in an allowed third-party package: by default java.., lombok.., org.apache.commons.lang3.., org.apache.commons.collections4.. and org.jspecify.annotations.., plus whatever the layout adds. The building-blocks strategic and port.in packages are not on the list, nor is the shared kernel unless it is a module root with a domain layer of its own. A dependency on any other package is reported.

## .NET reading

**Selection.** Types below the root namespace whose namespace lies under <Module>.Domain of every module root; the building-blocks types themselves are not selected.

**Check.** Every dependency whose target has a namespace points into one of those same domain namespaces or below an allowed prefix: the layout's third-party allow-list (by default System and Microsoft.Extensions.Logging.Abstractions, plus whatever the layout adds) and, of the building blocks, only Ddd.Tactical and Hexagonal.Ports.Out - a building-blocks entry in the allow-list is ignored here, so the strategic annotations and the input ports are not allowed in the domain. The shared kernel is not on the list either, unless it is a module root with a Domain layer of its own. A dependency on any other namespace is reported, each distinct pair once.

## Implementation

```java
DcaRule.of(
        "DCA-ONI-002",
        "The Domain Model should be framework independent and should not use 3rd party libraries"
            + " when possible",
        "Domain should be framework-independent (Dependency Inversion Principle)",
        arch -> {
          // The domain packages of every module root - the shared kernel among them when it
          // owns a domain package - plus the two building-blocks packages a domain may use:
          // the tactical markers and the output ports. Strategic annotations and input ports
          // are deliberately not on the list.
          List<String> domainPackageList = new ArrayList<>(List.of(arch.allDomainPatterns()));
          domainPackageList.add(DcaLayout.BUILDING_BLOCKS_TACTICAL_PACKAGE);
          domainPackageList.add(DcaLayout.BUILDING_BLOCKS_PORT_OUT_PACKAGE);
          String[] domainPackages = domainPackageList.toArray(String[]::new);
          List<String> allowed = new ArrayList<>(layout.thirdPartyPackagesAllowedInDomain());
          allowed.addAll(List.of(domainPackages));
          return classes()
              .that()
              .resideInAnyPackage(domainPackages)
              .should()
              .onlyDependOnClassesThat()
              .resideInAnyPackage(allowed.toArray(String[]::new))
              .allowEmptyShould(true);
        })
    .selecting(
        "Classes in <module>.domain.. of every module root, plus the classes of the"
            + " building-blocks packages ddd.tactical.. and hexagonal.port.out.. when they are"
            + " on the classpath under scan.")
    .checking(
        "Every dependency targets a class in one of those same packages or in an allowed"
            + " third-party package: by default java.., lombok.., org.apache.commons.lang3..,"
            + " org.apache.commons.collections4.. and org.jspecify.annotations.., plus"
            + " whatever the layout adds. The building-blocks strategic and port.in packages"
            + " are not on the list, nor is the shared kernel unless it is a module root with a"
            + " domain layer of its own. A dependency on any other package is reported.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-ONI-002",
    title,
    rationale,
    arch =>
    {
        var domain = new Regex(DcaLayout.AnyOf(arch.AllDomainPatterns()));
        // The layout's allow-list may name the whole building-blocks namespace (the default does, so
        // that attribute rules accept every marker); for *dependencies* only the tactical markers and
        // the output ports belong in the domain - strategic annotations and input ports do not.
        var allowedPrefixes = Layout.ThirdPartyNamespacesAllowedInDomain
            .Where(p => !DcaLayout.IsBelow(p, DcaLayout.BuildingBlocksNamespace))
            .Concat(new[] { DcaLayout.BuildingBlocksTacticalNamespace, DcaLayout.BuildingBlocksPortsOutNamespace })
            .ToList();
        bool Allowed(string ns) => domain.IsMatch(ns) || allowedPrefixes.Any(p => DcaLayout.IsBelow(ns, p));

        var violations = arch.Types
            .Where(t => t.Namespace is not null && domain.IsMatch(t.Namespace.FullName))
            .SelectMany(t => t.Dependencies
                .Select(d => d.Target)
                .Where(target => target.Namespace is not null && !string.IsNullOrEmpty(target.Namespace.FullName))
                .Where(target => !Allowed(target.Namespace.FullName))
                .Select(target => $"{t.FullName} depends on {target.FullName}"))
            .Distinct()
            .ToList();
        DcaRule.Fail($"{title}\nbecause {rationale}", violations);
    })
    .Selecting(
        "Types below the root namespace whose namespace lies under <Module>.Domain of "
        + "every module root; the building-blocks types themselves are not selected.")
    .Checking(
        "Every dependency whose target has a namespace points into one of those same "
        + "domain namespaces or below an allowed prefix: the layout's third-party "
        + "allow-list (by default System and Microsoft.Extensions.Logging.Abstractions, "
        + "plus whatever the layout adds) and, of the building blocks, only Ddd.Tactical "
        + "and Hexagonal.Ports.Out - a building-blocks entry in the allow-list is ignored "
        + "here, so the strategic annotations and the input ports are not allowed in the "
        + "domain. The shared kernel is not on the list either, unless it is a module root "
        + "with a Domain layer of its own. A dependency on any other namespace is reported, "
        + "each distinct pair once.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
