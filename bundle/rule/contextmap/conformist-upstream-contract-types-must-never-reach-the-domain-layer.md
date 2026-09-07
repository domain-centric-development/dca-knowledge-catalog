---
type: Rule
id: DCA-MAP-009
title: "Conformist: upstream contract types must never reach the domain layer"
rule: Conformism does not suspend domain purity — the domain layer stays free of foreign contract types.
constraint: "Conformist: upstream contract types must never reach the domain layer."
enforced_by: "ContextMapRules#DCA-MAP-009"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
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
      CollectedViolations violations = CollectedViolations.withoutHeader();
      Map<String, String> packagesByName = packagesByName(arch);
      for (String pkg : arch.boundedContextPackages()) {
        String source = arch.contextName(pkg);
        for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
          String targetPkg = packagesByName.get(u.context());
          if (u.translation() != Upstream.Translation.CONFORMIST || targetPkg == null) {
            continue;
          }
          for (Upstream.Consumes channel : u.via()) {
            violations.addAll(
                noClasses()
                    .that()
                    .resideInAPackage(layout.domainPattern(pkg))
                    .should()
                    .dependOnClassesThat()
                    .resideInAPackage(targetPkg + "." + channelName(arch, channel) + "..")
                    .allowEmptyShould(true),
                arch.classes(),
                "Context '"
                    + source
                    + "' conforms to '"
                    + u.context()
                    + "' ("
                    + channelName(arch, channel)
                    + "), but conformism does not suspend domain purity — the domain"
                    + " layer stays free of foreign contract types");
          }
        }
      }
      violations.throwIfAny();
    })
```

## Applies to markers

- [@Upstream](/marker/strategic/upstream.md)
