---
type: Rule
id: DCA-MAP-009
title: "Conformist: upstream contract types must never reach the domain layer"
rule: Conformism does not suspend domain purity — the domain layer stays free of foreign contract types.
constraint: "Conformist: upstream contract types must never reach the domain layer."
enforced_by: "ContextMapRules#DCA-MAP-009"
status: enforced
rule_set: contextmap
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-009",
    "Conformist: upstream contract types must never reach the domain layer",
    "Conformism does not suspend domain purity — the domain layer stays free of foreign"
        + " contract types",
    arch -> {
      Map<String, String> packagesByName = packagesByName(arch);
      for (String pkg : arch.boundedContextPackages()) {
        String source = shortName(pkg);
        for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
          String targetPkg = packagesByName.get(u.context());
          if (u.translation() != Upstream.Translation.CONFORMIST || targetPkg == null) {
            continue;
          }
          for (Upstream.Consumes channel : u.via()) {
            noClasses()
                .that()
                .resideInAPackage(layout.domainPattern(pkg))
                .should()
                .dependOnClassesThat()
                .resideInAPackage(targetPkg + "." + channelName(channel) + "..")
                .allowEmptyShould(true)
                .because(
                    "Context '"
                        + source
                        + "' conforms to '"
                        + u.context()
                        + "' ("
                        + channelName(channel)
                        + "), but conformism does not suspend domain purity — the domain"
                        + " layer stays free of foreign contract types")
                .check(arch.classes());
          }
        }
      }
    })
```

## Applies to markers

- [@Upstream](/marker/strategic/upstream.md)
