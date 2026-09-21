---
type: Rule
id: DCA-ONI-002
title: The Domain Model should be framework independent and should not use 3rd party libraries when possible
rule: "Domain should be framework-independent (Dependency Inversion Principle)."
constraint: The Domain Model should be framework independent and should not use 3rd party libraries when possible.
selects: "Classes in <module>.domain.. of every module root, plus the classes of the packages the configured marker vocabulary declares its domain-facing roles in — the tactical roles and the outgoing ports — when they are on the classpath under scan. With the default vocabulary those are the building-blocks packages ddd.tactical.. and hexagonal.port.out..; with a project's own markers they are the packages those markers live in."
checks: "Every dependency targets a class in one of those same packages or in an allowed third-party package: by default java.., lombok.., org.apache.commons.lang3.., org.apache.commons.collections4.. and org.jspecify.annotations... A logging facade is deliberately not among them - which logging, validation or utility library a domain model may see is a project decision, made with withThirdPartyPackagesAllowedInDomain(...). The vocabulary's own packages are on the list because they are derived from the roles, so pointing a role at another library's type does not make that library a reported dependency. The application-layer roles and the incoming ports are not on the list, nor are the strategic annotations, nor the shared kernel unless it is a module root with a domain layer of its own. A dependency on any other package is reported."
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

Classes in <module>.domain.. of every module root, plus the classes of the packages the configured marker vocabulary declares its domain-facing roles in — the tactical roles and the outgoing ports — when they are on the classpath under scan. With the default vocabulary those are the building-blocks packages ddd.tactical.. and hexagonal.port.out..; with a project's own markers they are the packages those markers live in.

## Check

Every dependency targets a class in one of those same packages or in an allowed third-party package: by default java.., lombok.., org.apache.commons.lang3.., org.apache.commons.collections4.. and org.jspecify.annotations... A logging facade is deliberately not among them - which logging, validation or utility library a domain model may see is a project decision, made with withThirdPartyPackagesAllowedInDomain(...). The vocabulary's own packages are on the list because they are derived from the roles, so pointing a role at another library's type does not make that library a reported dependency. The application-layer roles and the incoming ports are not on the list, nor are the strategic annotations, nor the shared kernel unless it is a module root with a domain layer of its own. A dependency on any other package is reported.

## .NET reading

**Selection.** Types below the root namespace whose namespace lies under <Module>.Domain of every module root; the building-blocks types themselves are not selected.

**Check.** Every dependency whose target has a namespace points into one of those same domain namespaces or below an allowed prefix: the layout's third-party allow-list (by default System only - a logging, validation or utility library is a project decision, added with WithThirdPartyNamespacesAllowedInDomain) and the namespaces the configured marker vocabulary declares its domain-facing roles in - the tactical roles and the outgoing ports, which for the default vocabulary are Ddd.Tactical and Hexagonal.Ports.Out. The vocabulary's own namespaces are on the list because they are derived from the roles, so pointing a role at another library's type does not make that library a reported dependency. A building-blocks entry in the allow-list is ignored here, so the strategic attributes, the application-layer roles and the input ports are not allowed in the domain. The shared kernel is not on the list either, unless it is a module root with a Domain layer of its own. A dependency on any other namespace is reported, each distinct pair once.

## Implementation

```java
DcaRule.of(
        "DCA-ONI-002",
        "The Domain Model should be framework independent and should not use 3rd party libraries"
            + " when possible",
        "Domain should be framework-independent (Dependency Inversion Principle)",
        arch -> {
          // The domain packages of every module root - the shared kernel among them when it
          // owns a domain package - plus the packages the marker vocabulary declares the
          // domain-facing roles in: the tactical markers and the outgoing ports. Derived from
          // the roles rather than hard-wired, so a project that points the roles at its own
          // markers is not reported as depending on a foreign library inside its own domain.
          // Strategic annotations, the application-layer roles and input ports are
          // deliberately not on the list.
          List<String> domainPackageList = new ArrayList<>(List.of(arch.allDomainPatterns()));
          domainPackageList.addAll(
              layout.markers().declaringPackagePatternsOf(DcaMarkers.DOMAIN_FACING_ROLES));
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
        "Classes in <module>.domain.. of every module root, plus the classes of the packages"
            + " the configured marker vocabulary declares its domain-facing roles in — the"
            + " tactical roles and the outgoing ports — when they are on the classpath under"
            + " scan. With the default vocabulary those are the building-blocks packages"
            + " ddd.tactical.. and hexagonal.port.out..; with a project's own markers they are"
            + " the packages those markers live in.")
    .checking(
        "Every dependency targets a class in one of those same packages or in an allowed"
            + " third-party package: by default java.., lombok.., org.apache.commons.lang3..,"
            + " org.apache.commons.collections4.. and org.jspecify.annotations... A logging"
            + " facade is deliberately not among them - which logging, validation or utility"
            + " library a domain model may see is a project decision, made with"
            + " withThirdPartyPackagesAllowedInDomain(...). The vocabulary's own packages are on the list"
            + " because they are derived from the roles, so pointing a role at another"
            + " library's type does not make that library a reported dependency. The"
            + " application-layer roles and the incoming ports are not on the list, nor are"
            + " the strategic annotations, nor the shared kernel unless it is a module root"
            + " with a domain layer of its own. A dependency on any other package is"
            + " reported.")
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
        // that attribute rules accept every marker); for *dependencies* only the namespaces the
        // configured vocabulary declares its domain-facing roles in belong in the domain - the
        // application-layer roles, the strategic attributes and the input ports do not. Derived from
        // the roles rather than hard-wired, so a project that points the roles at its own markers is
        // not reported as depending on a foreign library inside its own domain.
        var allowedPrefixes = Layout.ThirdPartyNamespacesAllowedInDomain
            .Where(p => !DcaLayout.IsBelow(p, DcaLayout.BuildingBlocksNamespace))
            .Concat(Layout.Markers.DeclaringNamespacesOf(DcaMarkers.DomainFacingRoles))
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
        + "allow-list (by default System only - a logging, validation or utility library "
        + "is a project decision, added with WithThirdPartyNamespacesAllowedInDomain) and "
        + "the namespaces the configured marker "
        + "vocabulary declares its domain-facing roles in - the tactical roles and the "
        + "outgoing ports, which for the default vocabulary are Ddd.Tactical and "
        + "Hexagonal.Ports.Out. The vocabulary's own namespaces are on the list because "
        + "they are derived from the roles, so pointing a role at another library's type "
        + "does not make that library a reported dependency. A building-blocks entry in "
        + "the allow-list is ignored here, so the strategic attributes, the "
        + "application-layer roles and the input ports are not allowed in the domain. The "
        + "shared kernel is not on the list either, unless it is a module root with a "
        + "Domain layer of its own. A dependency on any other namespace is reported, each "
        + "distinct pair once.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
