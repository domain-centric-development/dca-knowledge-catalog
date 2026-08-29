---
type: Rule
title: ExternalUpstream declarations must be well-formed and unique per name and interaction
rule: ExternalUpstream declarations must be well-formed and unique per name and interaction.
constraint: ExternalUpstream declarations must be well-formed and unique per name and interaction.
enforced_by: "ContextMapArchUnitTest#ExternalUpstream declarations must be well-formed and unique per name and interaction"
status: enforced
test_class: ContextMapArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/ContextMapArchUnitTest.groovy
tags: [contextmap, archunit]
---

```groovy
given:
Map<String, BoundedContext> contexts = discoverBoundedContextPackages()
Set<String> moduleNames = contexts.keySet().collect { shortName(it) } as Set

expect:
contexts.each { pkg, bc ->
  String source = shortName(pkg)
  List<String> edges = []
  getPackageAnnotations(pkg, ExternalUpstream).each { ExternalUpstream e ->
    assert !e.name().isBlank() :
    "Context '${source}' declares an @ExternalUpstream with a blank name"
    assert !moduleNames.contains(e.name()) :
    "Context '${source}' declares external system '${e.name()}', which is an internal bounded context module — use @Upstream for internal contexts"
    String edge = "${e.name()} :: ${e.interaction()}"
    assert !edges.contains(edge) :
    "Context '${source}' declares external system edge '${edge}' more than once — the identity of an @ExternalUpstream declaration is (name, interaction)"
    edges << edge
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Upstream](/marker/strategic/upstream.md)
