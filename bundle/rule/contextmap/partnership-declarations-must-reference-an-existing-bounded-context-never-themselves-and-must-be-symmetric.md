---
type: Rule
title: "Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric"
rule: "Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric."
constraint: "Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric."
enforced_by: "ContextMapArchUnitTest#Partnership declarations must reference an existing bounded context, never themselves, and must be symmetric"
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
  getPackageAnnotations(pkg, Partnership).each { Partnership p ->
    assert packagesByName.containsKey(p.context()) :
    "Context '${source}' declares @Partnership(context = \"${p.context()}\") but no bounded context module with that name exists"
    assert p.context() != source :
    "Context '${source}' declares a partnership with itself"

    List<Partnership> reverse = getPackageAnnotations(packagesByName[p.context()], Partnership)
    assert reverse.any { it.context() == source } :
    "Partnership between '${source}' and '${p.context()}' is only declared on '${source}' — partnerships are symmetric, add @Partnership(context = \"${source}\") to '${p.context()}'"
  }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Partnership](/marker/strategic/partnership.md)
