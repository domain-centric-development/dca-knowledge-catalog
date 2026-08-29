---
type: Rule
title: Upstream declarations must reference an existing bounded context and never the declaring context itself
rule: Upstream declarations must reference an existing bounded context and never the declaring context itself.
constraint: Upstream declarations must reference an existing bounded context and never the declaring context itself.
enforced_by: "ContextMapArchUnitTest#Upstream declarations must reference an existing bounded context and never the declaring context itself"
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
  getPackageAnnotations(pkg, Upstream).each { Upstream u ->
    assert moduleNames.contains(u.context()) :
    "Context '${source}' declares @Upstream(context = \"${u.context()}\") but no bounded context module with that name exists (known: ${moduleNames})"
    assert u.context() != source :
    "Context '${source}' declares itself as its own upstream"
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)
