---
type: Rule
title: Implemented Upstream declarations must be backed by an actual code dependency
rule: Implemented Upstream declarations must be backed by an actual code dependency.
constraint: Implemented Upstream declarations must be backed by an actual code dependency.
enforced_by: "ContextMapArchUnitTest#Implemented Upstream declarations must be backed by an actual code dependency"
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
// The completeness rule proves actual dependency -> declaration; this rule proves the
// reverse: a declared IMPLEMENTED edge without any real dependency is stale (or premature —
// then it is PLANNED) and would otherwise pass forever alongside an equally stale
// allowedDependencies entry.
contexts.each { pkg, bc ->
  String source = shortName(pkg)
  getPackageAnnotations(pkg, Upstream)
    .findAll { it.status() == Upstream.Status.IMPLEMENTED }
    .each { Upstream u ->
      String targetPkg = packagesByName[u.context()]
      u.via().each { Upstream.Consumes channel ->
        String channelPkg = "${targetPkg}.${channelName(channel)}"
        boolean exists = allClasses.any { javaClass ->
          inPackageTree(javaClass.getPackageName(), pkg) &&
            javaClass.getDirectDependenciesFromSelf().any { dep ->
              inPackageTree(dep.getTargetClass().getPackageName(), channelPkg)
            }
        }
        assert exists :
        "Context '${source}' declares @Upstream(context = \"${u.context()}\", via = ${channelName(channel)}) as IMPLEMENTED, but no class in '${pkg}' depends on '${channelPkg}..' — implement the dependency, mark the declaration status = PLANNED, or remove it"
      }
    }
}
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@Upstream](/marker/strategic/upstream.md)
