---
type: Rule
id: DCA-MAP-012
title: "Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric"
rule: A partnership is a mutual commitment — it exists only when both contexts declare it.
constraint: "Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric."
enforced_by: "ContextMapRules#DCA-MAP-012"
status: enforced
rule_set: contextmap
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-012",
    "Partnership declarations must reference an existing bounded context, never themselves,"
        + " and must be symmetric",
    "A partnership is a mutual commitment — it exists only when both contexts declare it",
    arch -> {
      Map<String, String> packagesByName = packagesByName(arch);
      for (String pkg : arch.boundedContextPackages()) {
        String source = shortName(pkg);
        for (Partnership p : arch.packageAnnotations(pkg, Partnership.class)) {
          require(
              packagesByName.containsKey(p.context()),
              "Context '"
                  + source
                  + "' declares @Partnership(context = \""
                  + p.context()
                  + "\") but no bounded context module with that name exists");
          require(
              !p.context().equals(source),
              "Context '" + source + "' declares a partnership with itself");
          boolean reverse =
              arch
                  .packageAnnotations(packagesByName.get(p.context()), Partnership.class)
                  .stream()
                  .anyMatch(r -> r.context().equals(source));
          require(
              reverse,
              "Partnership between '"
                  + source
                  + "' and '"
                  + p.context()
                  + "' is only declared on '"
                  + source
                  + "' — partnerships are symmetric, add @Partnership(context = \""
                  + source
                  + "\") to '"
                  + p.context()
                  + "'");
        }
      }
    })
```

## Applies to markers

- [@Partnership](/marker/strategic/partnership.md)
