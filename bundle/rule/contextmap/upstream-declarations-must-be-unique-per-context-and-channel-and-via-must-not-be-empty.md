---
type: Rule
title: "Upstream declarations must be unique per context and channel, and via must not be empty"
rule: "Upstream declarations must be unique per context and channel, and via must not be empty."
constraint: "Upstream declarations must be unique per context and channel, and via must not be empty."
enforced_by: "ContextMapArchUnitTest#Upstream declarations must be unique per context and channel, and via must not be empty"
status: enforced
test_class: ContextMapArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/ContextMapArchUnitTest.groovy
tags: [contextmap, archunit]
---

```groovy
given:
Map<String, BoundedContext> contexts = discoverBoundedContextPackages()

expect:
contexts.each { pkg, bc ->
  String source = shortName(pkg)
  List<String> edges = []
  getPackageAnnotations(pkg, Upstream).each { Upstream u ->
    assert u.via().length > 0 :
    "Context '${source}': @Upstream(context = \"${u.context()}\") declares no channel — via must not be empty"
    u.via().each { Upstream.Consumes channel ->
      String edge = "${u.context()} :: ${channelName(channel)}"
      assert !edges.contains(edge) :
      "Context '${source}' declares (context, channel) '${edge}' more than once — the identity of an @Upstream declaration is (context, via); different translations per channel require separate annotations"
      edges << edge
    }
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)
