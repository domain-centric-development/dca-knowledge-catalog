---
type: Rule
id: DCA-MAP-002
title: ExternalUpstream declarations must be well-formed and unique per name and interaction
rule: "The identity of an @ExternalUpstream declaration is (name, interaction); internal contexts are declared with @Upstream instead."
constraint: ExternalUpstream declarations must be well-formed and unique per name and interaction.
enforced_by: "ContextMapRules#DCA-MAP-002"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-002",
    "ExternalUpstream declarations must be well-formed and unique per name and interaction",
    "The identity of an @ExternalUpstream declaration is (name, interaction); internal"
        + " contexts are declared with @Upstream instead",
    arch -> {
      Set<String> moduleNames = moduleNames(arch);
      for (String pkg : arch.boundedContextPackages()) {
        String source = arch.contextName(pkg);
        List<String> edges = new ArrayList<>();
        for (ExternalUpstream e : arch.packageAnnotations(pkg, ExternalUpstream.class)) {
          require(
              !e.name().isBlank(),
              "Context '" + source + "' declares an @ExternalUpstream with a blank name");
          require(
              !moduleNames.contains(e.name()),
              "Context '"
                  + source
                  + "' declares external system '"
                  + e.name()
                  + "', which is an internal bounded context module — use @Upstream for"
                  + " internal contexts");
          String edge = e.name() + " :: " + e.interaction();
          require(
              !edges.contains(edge),
              "Context '"
                  + source
                  + "' declares external system edge '"
                  + edge
                  + "' more than once — the identity of an @ExternalUpstream declaration is"
                  + " (name, interaction)");
          edges.add(edge);
        }
      }
    })
```

## Applies to markers

- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Upstream](/marker/strategic/upstream.md)
