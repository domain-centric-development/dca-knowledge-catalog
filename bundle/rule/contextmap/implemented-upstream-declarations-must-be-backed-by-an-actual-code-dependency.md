---
type: Rule
id: DCA-MAP-007
title: Implemented Upstream declarations must be backed by an actual code dependency
rule: "A declared IMPLEMENTED edge without any real dependency is stale (or premature — then it is PLANNED) and would otherwise pass forever alongside an equally stale module boundary entry."
constraint: Implemented Upstream declarations must be backed by an actual code dependency.
enforced_by: "ContextMapRules#DCA-MAP-007"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-007",
    "Implemented Upstream declarations must be backed by an actual code dependency",
    "A declared IMPLEMENTED edge without any real dependency is stale (or premature — then it"
        + " is PLANNED) and would otherwise pass forever alongside an equally stale module"
        + " boundary entry",
    arch -> {
      CollectedViolations violations = CollectedViolations.withoutHeader();
      Map<String, String> packagesByName = packagesByName(arch);
      for (String pkg : arch.boundedContextPackages()) {
        String source = arch.contextName(pkg);
        for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
          String targetPkg = packagesByName.get(u.context());
          if (u.status() != Upstream.Status.IMPLEMENTED || targetPkg == null) {
            continue;
          }
          for (Upstream.Consumes channel : u.via()) {
            String channelPkg = targetPkg + "." + channelName(arch, channel);
            boolean exists = false;
            for (JavaClass javaClass : arch.classes()) {
              if (!inPackageTree(javaClass.getPackageName(), pkg)) {
                continue;
              }
              for (Dependency dep : javaClass.getDirectDependenciesFromSelf()) {
                if (inPackageTree(dep.getTargetClass().getPackageName(), channelPkg)) {
                  exists = true;
                  break;
                }
              }
              if (exists) {
                break;
              }
            }
            violations.require(
                exists,
                "Context '"
                    + source
                    + "' declares @Upstream(context = \""
                    + u.context()
                    + "\", via = "
                    + channelName(arch, channel)
                    + ") as IMPLEMENTED, but no class in '"
                    + pkg
                    + "' depends on '"
                    + channelPkg
                    + "..' — implement the dependency, mark the declaration status = PLANNED,"
                    + " or remove it");
          }
        }
      }
      violations.throwIfAny();
    })
```

## Applies to markers

- [@Upstream](/marker/strategic/upstream.md)
