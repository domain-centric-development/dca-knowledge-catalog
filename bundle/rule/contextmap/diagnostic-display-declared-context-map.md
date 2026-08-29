---
type: Rule
title: "Diagnostic: Display declared context map"
rule: "Diagnostic: Display declared context map."
constraint: "Diagnostic: Display declared context map."
enforced_by: "ContextMapArchUnitTest#Diagnostic: Display declared context map"
status: informational
test_class: ContextMapArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/ContextMapArchUnitTest.groovy
tags: [contextmap, archunit]
---

```groovy
when:
Map<String, BoundedContext> contexts = discoverBoundedContextPackages()

then:
println "=== Context Map (declared) ==="
contexts.each { pkg, bc ->
  String source = shortName(pkg)
  getPackageAnnotations(pkg, Upstream).each { Upstream u ->
    u.via().each { channel ->
      println "  ${source} --[${u.translation()} / ${channelName(channel)}]--> ${u.context()}"
    }
  }
  getPackageAnnotations(pkg, ExternalUpstream).each { ExternalUpstream e ->
    println "  ${source} --[${e.translation()} / ${e.interaction()}]--> (external) ${e.name()}"
  }
  getPackageAnnotations(pkg, Partnership).each { Partnership p ->
    println "  ${source} <--[PARTNERSHIP]--> ${p.context()}"
  }
}
println "=============================="
contexts.size() >= 1
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@Upstream](/marker/strategic/upstream.md)
