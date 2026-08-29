---
type: Rule
id: DCA-ONI-002
title: The Domain Model should be framework independent and should not use 3rd party libraries when possible
rule: "Domain should be framework-independent (Dependency Inversion Principle)."
constraint: The Domain Model should be framework independent and should not use 3rd party libraries when possible.
enforced_by: "OnionRules#DCA-ONI-002"
status: enforced
rule_set: onion
implementations: [java]
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
      // Matched by pattern, never by context name: domainPattern() is base.*.domain.., which
      // also covers the shared kernel's own domain package.
      String[] domainPackages = {
        layout.domainPattern(),
        DcaLayout.BUILDING_BLOCKS_TACTICAL_PACKAGE,
        DcaLayout.BUILDING_BLOCKS_PORT_OUT_PACKAGE
      };
      List<String> allowed = new ArrayList<>(layout.thirdPartyPackagesAllowedInDomain());
      allowed.addAll(List.of(domainPackages));
      return classes()
          .that()
          .resideInAnyPackage(domainPackages)
          .should()
          .onlyDependOnClassesThat()
          .resideInAnyPackage(allowed.toArray(String[]::new));
    })
```
