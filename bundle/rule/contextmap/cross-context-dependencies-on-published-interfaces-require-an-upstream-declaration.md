---
type: Rule
title: Cross-context dependencies on published interfaces require an Upstream declaration
rule: "Context '<context>' depends on '<context> :: <context>' without declaring it — add @Upstream(context = \"<context>\", translation = ..., via = ...) to its package-info."
constraint: Cross-context dependencies on published interfaces require an Upstream declaration.
enforced_by: "ContextMapArchUnitTest#Cross-context dependencies on published interfaces require an Upstream declaration"
status: enforced
test_class: ContextMapArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/ContextMapArchUnitTest.groovy
tags: [contextmap, archunit]
---

```groovy
given:
Map<String, BoundedContext> contexts = discoverBoundedContextPackages()

expect:
contexts.each { srcPkg, bc ->
  String source = shortName(srcPkg)
  Set<String> declared = declaredEdges(srcPkg)

  contexts.each { tgtPkg, tbc ->
    if (tgtPkg == srcPkg) {
      return
    }
    String target = shortName(tgtPkg)
    ["api", "events"].each { channel ->
      if (!declared.contains("${target} :: ${channel}".toString())) {
        noClasses()
          .that().resideInAPackage("${srcPkg}..")
          .should().dependOnClassesThat().resideInAPackage("${tgtPkg}.${channel}..")
          .allowEmptyShould(true)
          .because("Context '${source}' depends on '${target} :: ${channel}' without declaring it — add @Upstream(context = \"${target}\", translation = ..., via = ...) to its package-info")
          .check(allClasses)
      }
    }
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)
