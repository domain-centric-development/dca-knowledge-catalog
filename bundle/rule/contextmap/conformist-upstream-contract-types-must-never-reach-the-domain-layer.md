---
type: Rule
title: "Conformist: upstream contract types must never reach the domain layer"
rule: "Context '<context>' conforms to '<context>' (<context>), but conformism does not suspend domain purity — the domain layer stays free of foreign contract types."
constraint: "Conformist: upstream contract types must never reach the domain layer."
enforced_by: "ContextMapArchUnitTest#Conformist: upstream contract types must never reach the domain layer"
status: enforced
test_class: ContextMapArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/ContextMapArchUnitTest.groovy
tags: [contextmap, archunit]
---

```groovy
given:
Map<String, BoundedContext> contexts = discoverBoundedContextPackages()
Map<String, String> packagesByName = contexts.keySet().collectEntries { [(shortName(it)): it] }

expect:
contexts.each { pkg, bc ->
  String source = shortName(pkg)
  getPackageAnnotations(pkg, Upstream)
    .findAll { it.translation() == Upstream.Translation.CONFORMIST }
    .each { Upstream u ->
      String targetPkg = packagesByName[u.context()]
      u.via().each { Upstream.Consumes channel ->
        noClasses()
          .that().resideInAPackage("${pkg}.domain..")
          .should().dependOnClassesThat()
          .resideInAPackage("${targetPkg}.${channelName(channel)}..")
          .allowEmptyShould(true)
          .because("Context '${source}' conforms to '${u.context()}' (${channelName(channel)}), but conformism does not suspend domain purity — the domain layer stays free of foreign contract types")
          .check(allClasses)
      }
    }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)
