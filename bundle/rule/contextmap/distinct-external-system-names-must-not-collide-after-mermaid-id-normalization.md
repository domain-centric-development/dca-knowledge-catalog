---
type: Rule
title: Distinct external system names must not collide after mermaid id normalization
rule: Distinct external system names must not collide after mermaid id normalization.
constraint: Distinct external system names must not collide after mermaid id normalization.
enforced_by: "ContextMapArchUnitTest#Distinct external system names must not collide after mermaid id normalization"
status: enforced
test_class: ContextMapArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/ContextMapArchUnitTest.groovy
tags: [contextmap, archunit]
---

```groovy
given:
Map<String, BoundedContext> contexts = discoverBoundedContextPackages()

expect:
// The generated context map renders one mermaid node per external system, identified by the
// normalized name. Two spellings of the same system ("Payment-Service", "Payment Service")
// would silently merge into one node while the tables list them as two systems.
Map<String, String> idToName = [:]
contexts.each { pkg, bc ->
  getPackageAnnotations(pkg, ExternalUpstream).each { ExternalUpstream e ->
    String id = normalizedExternalId(e.name())
    assert idToName.getOrDefault(id, e.name()) == e.name() :
    "External system names '${idToName[id]}' and '${e.name()}' normalize to the same mermaid node id '${id}' — use one canonical spelling"
    idToName[id] = e.name()
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
