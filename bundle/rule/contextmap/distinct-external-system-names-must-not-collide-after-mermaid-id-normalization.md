---
type: Rule
id: DCA-MAP-003
title: Distinct external system names must not collide after mermaid id normalization
rule: The generated context map renders one node per normalized external system name — two spellings of the same system would silently merge into one node.
constraint: Distinct external system names must not collide after mermaid id normalization.
enforced_by: "ContextMapRules#DCA-MAP-003"
status: enforced
rule_set: contextmap
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

```java
DcaRule.check(
    "DCA-MAP-003",
    "Distinct external system names must not collide after mermaid id normalization",
    "The generated context map renders one node per normalized external system name — two"
        + " spellings of the same system would silently merge into one node",
    arch -> {
      Map<String, String> idToName = new LinkedHashMap<>();
      for (String pkg : arch.boundedContextPackages()) {
        for (ExternalUpstream e : arch.packageAnnotations(pkg, ExternalUpstream.class)) {
          String id = normalizedExternalId(e.name());
          String known = idToName.getOrDefault(id, e.name());
          require(
              known.equals(e.name()),
              "External system names '"
                  + known
                  + "' and '"
                  + e.name()
                  + "' normalize to the same mermaid node id '"
                  + id
                  + "' — use one canonical spelling");
          idToName.put(id, e.name());
        }
      }
    })
```

## Applies to markers

- [@ExternalUpstream](/marker/strategic/externalupstream.md)
