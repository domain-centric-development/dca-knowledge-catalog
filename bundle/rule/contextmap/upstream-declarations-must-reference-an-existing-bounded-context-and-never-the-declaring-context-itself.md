---
type: Rule
id: DCA-MAP-004
title: Upstream declarations must reference an existing bounded context and never the declaring context itself
rule: A dangling or self-referencing upstream edge describes a relationship that cannot exist.
constraint: Upstream declarations must reference an existing bounded context and never the declaring context itself.
enforced_by: "ContextMapRules#DCA-MAP-004"
status: enforced
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-004",
    "Upstream declarations must reference an existing bounded context and never the declaring"
        + " context itself",
    "A dangling or self-referencing upstream edge describes a relationship that cannot exist",
    arch -> {
      Set<String> moduleNames = moduleNames(arch);
      for (String pkg : arch.boundedContextPackages()) {
        String source = arch.contextName(pkg);
        for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
          require(
              moduleNames.contains(u.context()),
              "Context '"
                  + source
                  + "' declares @Upstream(context = \""
                  + u.context()
                  + "\") but no bounded context module with that name exists (known: "
                  + moduleNames
                  + ")");
          require(
              !u.context().equals(source),
              "Context '" + source + "' declares itself as its own upstream");
        }
      }
    })
```

## Applies to markers

- [@Upstream](/marker/strategic/upstream.md)
