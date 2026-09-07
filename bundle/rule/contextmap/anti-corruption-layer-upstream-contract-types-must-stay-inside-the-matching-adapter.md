---
type: Rule
id: DCA-MAP-008
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter"
rule: "The ACL sits where the dependency crosses the boundary — outgoing adapters for synchronous API calls, incoming adapters for consumed events — and translates the upstream contract into the context's own model there."
constraint: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter."
enforced_by: "ContextMapRules#DCA-MAP-008"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-008",
    "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter",
    "The ACL sits where the dependency crosses the boundary — outgoing adapters for synchronous"
        + " API calls, incoming adapters for consumed events — and translates the upstream"
        + " contract into the context's own model there",
    arch -> {
      CollectedViolations violations = CollectedViolations.withoutHeader();
      Map<String, String> packagesByName = packagesByName(arch);
      for (String pkg : arch.boundedContextPackages()) {
        String source = arch.contextName(pkg);
        for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
          String targetPkg = packagesByName.get(u.context());
          if (u.translation() != Upstream.Translation.ANTI_CORRUPTION_LAYER
              || targetPkg == null) {
            continue;
          }
          for (Upstream.Consumes channel : u.via()) {
            String allowedAdapter =
                channel == Upstream.Consumes.API
                    ? layout.outgoingAdapterPattern(pkg)
                    : layout.incomingAdapterPattern(pkg);
            violations.addAll(
                noClasses()
                    .that()
                    .resideInAPackage(pkg + "..")
                    .and()
                    .resideOutsideOfPackage(allowedAdapter)
                    .should()
                    .dependOnClassesThat()
                    .resideInAPackage(targetPkg + "." + channelName(arch, channel) + "..")
                    .allowEmptyShould(true),
                arch.classes(),
                "Context '"
                    + source
                    + "' declares ANTI_CORRUPTION_LAYER towards '"
                    + u.context()
                    + "' ("
                    + channelName(arch, channel)
                    + ") — upstream contract types must not leave "
                    + allowedAdapter
                    + "; translate them there into the context's own model");
          }
        }
      }
      violations.throwIfAny();
    })
```

## Applies to markers

- [@Upstream](/marker/strategic/upstream.md)
