---
type: Rule
id: DCA-MAP-013
title: "Diagnostic: Display declared context map"
rule: Printing the declared edges makes the executable context map reviewable at a glance.
constraint: "Diagnostic: Display declared context map."
enforced_by: "ContextMapRules#DCA-MAP-013"
status: informational
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-013",
    "Diagnostic: Display declared context map",
    "Printing the declared edges makes the executable context map reviewable at a glance",
    arch -> {
      System.out.println("=== Context Map (declared) ===");
      for (String pkg : arch.boundedContextPackages()) {
        String source = shortName(pkg);
        for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
          for (Upstream.Consumes channel : u.via()) {
            System.out.println(
                "  "
                    + source
                    + " --["
                    + u.translation()
                    + " / "
                    + channelName(channel)
                    + "]--> "
                    + u.context());
          }
        }
        for (ExternalUpstream e : arch.packageAnnotations(pkg, ExternalUpstream.class)) {
          System.out.println(
              "  "
                  + source
                  + " --["
                  + e.translation()
                  + " / "
                  + e.interaction()
                  + "]--> (external) "
                  + e.name());
        }
        for (Partnership p : arch.packageAnnotations(pkg, Partnership.class)) {
          System.out.println("  " + source + " <--[PARTNERSHIP]--> " + p.context());
        }
      }
      System.out.println("==============================");
    })
```

## Applies to markers

- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@Upstream](/marker/strategic/upstream.md)
