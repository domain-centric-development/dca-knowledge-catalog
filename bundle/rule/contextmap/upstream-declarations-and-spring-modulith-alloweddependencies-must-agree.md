---
type: Rule
title: Upstream declarations and Spring Modulith allowedDependencies must agree
rule: Upstream declarations and Spring Modulith allowedDependencies must agree.
constraint: Upstream declarations and Spring Modulith allowedDependencies must agree.
enforced_by: "ContextMapArchUnitTest#Upstream declarations and Spring Modulith allowedDependencies must agree"
status: enforced
test_class: ContextMapArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/ContextMapArchUnitTest.groovy
tags: [contextmap, archunit]
---

```groovy
given:
// Loaded reflectively so this test class compiles and runs in projects without Spring
// Modulith — there the rule is skipped and the remaining rules still bind the declarations
// to the code itself.
Class<? extends java.lang.annotation.Annotation> applicationModule =
  Class.forName(APPLICATION_MODULE_ANNOTATION) as Class<? extends java.lang.annotation.Annotation>
Map<String, BoundedContext> contexts = discoverBoundedContextPackages()
Set<String> moduleNames = contexts.keySet().collect { shortName(it) } as Set

expect:
contexts.each { pkg, bc ->
  String source = shortName(pkg)
  Set<String> declared = declaredEdges(pkg)

  def module = getPackageAnnotation(pkg, applicationModule)
  Set<String> allowed = (module == null ? [] : module.allowedDependencies().toList())
    .collect { it.replaceAll(/\s*::\s*/, ' :: ').trim() }
    .findAll { it.contains(' :: ') }
    .findAll { moduleNames.contains(it.split(' :: ')[0]) }
    .toSet()

  assert declared == allowed :
  "Context '${source}': @Upstream declarations ${declared.sort()} and @ApplicationModule.allowedDependencies named-interface entries ${allowed.sort()} must describe the same edges — neither side may know more than the other"
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)
