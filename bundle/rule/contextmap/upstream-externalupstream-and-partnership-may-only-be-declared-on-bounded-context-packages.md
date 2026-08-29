---
type: Rule
title: "Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages"
rule: "Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages."
constraint: "Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages."
enforced_by: "ContextMapArchUnitTest#Upstream, ExternalUpstream, and Partnership may only be declared on bounded context packages"
status: enforced
test_class: ContextMapArchUnitTest
resource: dca-ecommerce-sample/src/test-architecture/groovy/de/sample/aiarchitecture/ContextMapArchUnitTest.groovy
tags: [contextmap, archunit]
---

```groovy
given:
Set<String> roots = allRootPackages()

expect:
roots.each { pkg ->
  if (getPackageAnnotation(pkg, BoundedContext) == null) {
    assert getPackageAnnotations(pkg, Upstream).isEmpty() :
    "Package '${pkg}' declares @Upstream but is not a @BoundedContext — context map declarations are reserved for bounded contexts"
    assert getPackageAnnotations(pkg, ExternalUpstream).isEmpty() :
    "Package '${pkg}' declares @ExternalUpstream but is not a @BoundedContext — context map declarations are reserved for bounded contexts"
    assert getPackageAnnotations(pkg, Partnership).isEmpty() :
    "Package '${pkg}' declares @Partnership but is not a @BoundedContext — context map declarations are reserved for bounded contexts"
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@Upstream](/marker/strategic/upstream.md)
