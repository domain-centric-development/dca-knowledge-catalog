---
type: Rule
id: DCA-MAP-005
title: "Upstream declarations must be unique per context and channel, and via must not be empty"
rule: "The identity of an @Upstream declaration is (context, via); different translations per channel require separate annotations."
constraint: "Upstream declarations must be unique per context and channel, and via must not be empty."
enforced_by: "ContextMapRules#DCA-MAP-005"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-005",
    "Upstream declarations must be unique per context and channel, and via must not be empty",
    "The identity of an @Upstream declaration is (context, via); different translations per"
        + " channel require separate annotations",
    arch -> {
      for (String pkg : arch.boundedContextPackages()) {
        String source = arch.contextName(pkg);
        List<String> edges = new ArrayList<>();
        for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
          require(
              u.via().length > 0,
              "Context '"
                  + source
                  + "': @Upstream(context = \""
                  + u.context()
                  + "\") declares no channel — via must not be empty");
          for (Upstream.Consumes channel : u.via()) {
            String edge = u.context() + " :: " + channelName(arch, channel);
            require(
                !edges.contains(edge),
                "Context '"
                    + source
                    + "' declares (context, channel) '"
                    + edge
                    + "' more than once — the identity of an @Upstream declaration is"
                    + " (context, via); different translations per channel require separate"
                    + " annotations");
            edges.add(edge);
          }
        }
      }
    })
```

## Applies to markers

- [@Upstream](/marker/strategic/upstream.md)
