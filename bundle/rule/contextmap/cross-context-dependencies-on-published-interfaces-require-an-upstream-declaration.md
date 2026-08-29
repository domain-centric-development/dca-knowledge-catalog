---
type: Rule
id: DCA-MAP-011
title: Cross-context dependencies on published interfaces require an Upstream declaration
rule: Every real dependency on a foreign api/ or events/ package is a context-map edge and must be declared as such.
constraint: Cross-context dependencies on published interfaces require an Upstream declaration.
enforced_by: "ContextMapRules#DCA-MAP-011"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-011",
    "Cross-context dependencies on published interfaces require an Upstream declaration",
    "Every real dependency on a foreign api/ or events/ package is a context-map edge and must"
        + " be declared as such",
    arch -> {
      List<String> contexts = arch.boundedContextPackages();
      for (String srcPkg : contexts) {
        String source = shortName(srcPkg);
        Set<String> declared = declaredEdges(arch, srcPkg);
        for (String tgtPkg : contexts) {
          if (tgtPkg.equals(srcPkg)) {
            continue;
          }
          String target = shortName(tgtPkg);
          for (String channel : List.of(API, EVENTS)) {
            if (declared.contains(target + " :: " + channel)) {
              continue;
            }
            noClasses()
                .that()
                .resideInAPackage(srcPkg + "..")
                .should()
                .dependOnClassesThat()
                .resideInAPackage(tgtPkg + "." + channel + "..")
                .allowEmptyShould(true)
                .because(
                    "Context '"
                        + source
                        + "' depends on '"
                        + target
                        + " :: "
                        + channel
                        + "' without declaring it — add @Upstream(context = \""
                        + target
                        + "\", translation = ..., via = ...) to its package-info")
                .check(arch.classes());
          }
        }
      }
    })
```

## Applies to markers

- [@Upstream](/marker/strategic/upstream.md)
