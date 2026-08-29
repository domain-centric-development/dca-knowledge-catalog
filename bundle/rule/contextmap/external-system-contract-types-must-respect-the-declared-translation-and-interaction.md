---
type: Rule
id: DCA-MAP-010
title: External system contract types must respect the declared translation and interaction
rule: "An external system's contract types are confined to the adapter where the exchange crosses the boundary (ACL) or at least kept out of the domain (Conformist)."
constraint: External system contract types must respect the declared translation and interaction.
enforced_by: "ContextMapRules#DCA-MAP-010"
status: enforced
rule_set: contextmap
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-010",
    "External system contract types must respect the declared translation and interaction",
    "An external system's contract types are confined to the adapter where the exchange"
        + " crosses the boundary (ACL) or at least kept out of the domain (Conformist)",
    arch -> {
      // Without contractPackages (wire-level contract, no vendor SDK) there is nothing to
      // check — the declaration then only documents the relationship.
      for (String pkg : arch.boundedContextPackages()) {
        String source = shortName(pkg);
        for (ExternalUpstream e : arch.packageAnnotations(pkg, ExternalUpstream.class)) {
          if (e.contractPackages().length == 0) {
            continue;
          }
          if (e.translation() == Upstream.Translation.ANTI_CORRUPTION_LAYER) {
            String allowedAdapter =
                e.interaction() == ExternalUpstream.Interaction.OUTBOUND
                    ? layout.outgoingAdapterPattern(pkg)
                    : layout.incomingAdapterPattern(pkg);
            noClasses()
                .that()
                .resideInAPackage(pkg + "..")
                .and()
                .resideOutsideOfPackage(allowedAdapter)
                .should()
                .dependOnClassesThat()
                .resideInAnyPackage(e.contractPackages())
                .allowEmptyShould(true)
                .because(
                    "Context '"
                        + source
                        + "' declares ANTI_CORRUPTION_LAYER towards external system '"
                        + e.name()
                        + "' ("
                        + e.interaction()
                        + ") — its contract types ("
                        + String.join(", ", e.contractPackages())
                        + ") must not leave "
                        + allowedAdapter)
                .check(arch.classes());
          } else {
            noClasses()
                .that()
                .resideInAPackage(layout.domainPattern(pkg))
                .should()
                .dependOnClassesThat()
                .resideInAnyPackage(e.contractPackages())
                .allowEmptyShould(true)
                .because(
                    "Context '"
                        + source
                        + "' conforms to external system '"
                        + e.name()
                        + "', but conformism does not suspend domain purity — the domain"
                        + " layer stays free of its contract types")
                .check(arch.classes());
          }
        }
      }
    })
```

## Applies to markers

- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Upstream](/marker/strategic/upstream.md)
