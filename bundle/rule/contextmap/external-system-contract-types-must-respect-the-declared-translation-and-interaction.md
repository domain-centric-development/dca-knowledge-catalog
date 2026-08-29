---
type: Rule
title: External system contract types must respect the declared translation and interaction
rule: "Context '<context>' declares ANTI_CORRUPTION_LAYER towards external system '<context>' (<context>) — its contract types (<context>) must not leave <context>."
constraint: External system contract types must respect the declared translation and interaction.
enforced_by: "ContextMapArchUnitTest#External system contract types must respect the declared translation and interaction"
status: enforced
test_class: ContextMapArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/ContextMapArchUnitTest.groovy
tags: [contextmap, archunit]
---

```groovy
given:
Map<String, BoundedContext> contexts = discoverBoundedContextPackages()

expect:
// Without contractPackages (wire-level contract, no vendor SDK) there is nothing to check —
// the declaration then only documents the relationship and feeds the generated context map.
contexts.each { pkg, bc ->
  String source = shortName(pkg)
  getPackageAnnotations(pkg, ExternalUpstream)
    .findAll { it.contractPackages().length > 0 }
    .each { ExternalUpstream e ->
      if (e.translation() == Upstream.Translation.ANTI_CORRUPTION_LAYER) {
        // The ACL sits where the exchange crosses the boundary: outgoing adapters when this
        // context initiates, incoming adapters when the external system does.
        String allowedAdapter = e.interaction() == ExternalUpstream.Interaction.OUTBOUND
          ? "${pkg}.adapter.outgoing.."
          : "${pkg}.adapter.incoming.."

        noClasses()
          .that().resideInAPackage("${pkg}..")
          .and().resideOutsideOfPackage(allowedAdapter)
          .should().dependOnClassesThat()
          .resideInAnyPackage(e.contractPackages())
          .allowEmptyShould(true)
          .because("Context '${source}' declares ANTI_CORRUPTION_LAYER towards external system '${e.name()}' (${e.interaction()}) — its contract types (${e.contractPackages().join(', ')}) must not leave ${allowedAdapter}")
          .check(allClasses)
      } else {
        noClasses()
          .that().resideInAPackage("${pkg}.domain..")
          .should().dependOnClassesThat()
          .resideInAnyPackage(e.contractPackages())
          .allowEmptyShould(true)
          .because("Context '${source}' conforms to external system '${e.name()}', but conformism does not suspend domain purity — the domain layer stays free of its contract types")
          .check(allClasses)
      }
    }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Upstream](/marker/strategic/upstream.md)
