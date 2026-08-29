---
type: Rule
id: DCA-MAP-006
title: Upstream declarations and Spring Modulith allowedDependencies must agree
rule: Neither the context map nor the module boundary may know more than the other — an edge that exists only on one side is stale.
constraint: Upstream declarations and Spring Modulith allowedDependencies must agree.
enforced_by: "ContextMapRules#DCA-MAP-006"
status: enforced
rule_set: contextmap
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
not_applicable_dotnet: Upstream declarations and Spring Modulith allowedDependencies must agree — .NET has no module system annotation; project boundaries take that role
---

```java
DcaRule.check(
    "DCA-MAP-006",
    "Upstream declarations and Spring Modulith allowedDependencies must agree",
    "Neither the context map nor the module boundary may know more than the other — an edge"
        + " that exists only on one side is stale",
    arch -> {
      Optional<Class<? extends Annotation>> moduleAnnotation = moduleAnnotationType();
      if (moduleAnnotation.isEmpty()) {
        return;
      }
      Set<String> moduleNames = moduleNames(arch);
      for (String pkg : arch.boundedContextPackages()) {
        String source = shortName(pkg);
        Set<String> declared = declaredEdges(arch, pkg);
        Set<String> allowed = new LinkedHashSet<>();
        for (String entry : allowedDependencies(arch, pkg, moduleAnnotation.get())) {
          String normalized = entry.replaceAll("\\s*::\\s*", " :: ").trim();
          if (normalized.contains(" :: ")
              && moduleNames.contains(normalized.split(" :: ")[0])) {
            allowed.add(normalized);
          }
        }
        require(
            declared.equals(allowed),
            "Context '"
                + source
                + "': @Upstream declarations "
                + new TreeSet<>(declared)
                + " and @ApplicationModule.allowedDependencies named-interface entries "
                + new TreeSet<>(allowed)
                + " must describe the same edges — neither side may know more than the other");
      }
    })
```

## Applies to markers

- [@Upstream](/marker/strategic/upstream.md)
