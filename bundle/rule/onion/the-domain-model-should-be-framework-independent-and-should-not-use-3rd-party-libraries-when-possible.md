---
type: Rule
id: DCA-ONI-002
title: The Domain Model should be framework independent and should not use 3rd party libraries when possible
rule: "Domain should be framework-independent (Dependency Inversion Principle)."
constraint: The Domain Model should be framework independent and should not use 3rd party libraries when possible.
enforced_by: "OnionRules#DCA-ONI-002"
status: enforced
rule_set: onion
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/OnionRules.java
tags: [onion, archunit]
---

```java
DcaRule.of(
    "DCA-ONI-002",
    "The Domain Model should be framework independent and should not use 3rd party libraries"
        + " when possible",
    "Domain should be framework-independent (Dependency Inversion Principle)",
    arch -> {
      // Every discovered context's domain plus the shared kernel's own domain package — the
      // inclusion is explicit here, where the former base.*.domain.. wildcard covered the
      // shared kernel only as a side effect of matching one segment.
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
```
