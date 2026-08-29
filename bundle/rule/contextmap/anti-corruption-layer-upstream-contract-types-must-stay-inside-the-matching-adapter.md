---
type: Rule
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter"
rule: "Context '<context>' declares ANTI_CORRUPTION_LAYER towards '<context>' (<context>) — upstream contract types must not leave <context>; translate them there into the context's own model."
constraint: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter."
enforced_by: "ContextMapArchUnitTest#Anti-Corruption Layer: upstream contract types must stay inside the matching adapter"
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
    .findAll { it.translation() == Upstream.Translation.ANTI_CORRUPTION_LAYER }
    .each { Upstream u ->
      String targetPkg = packagesByName[u.context()]
      u.via().each { Upstream.Consumes channel ->
        // The ACL edge sits where the dependency crosses the boundary: outgoing adapters for
        // synchronous API calls, incoming adapters for consumed events.
        String allowedAdapter = channel == Upstream.Consumes.API
          ? "${pkg}.adapter.outgoing.."
          : "${pkg}.adapter.incoming.."

        noClasses()
          .that().resideInAPackage("${pkg}..")
          .and().resideOutsideOfPackage(allowedAdapter)
          .should().dependOnClassesThat()
          .resideInAPackage("${targetPkg}.${channelName(channel)}..")
          .allowEmptyShould(true)
          .because("Context '${source}' declares ANTI_CORRUPTION_LAYER towards '${u.context()}' (${channelName(channel)}) — upstream contract types must not leave ${allowedAdapter}; translate them there into the context's own model")
          .check(allClasses)
      }
    }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)
