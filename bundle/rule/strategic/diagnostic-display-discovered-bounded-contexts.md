---
type: Rule
title: "Diagnostic: Display discovered bounded contexts"
rule: "Diagnostic: Display discovered bounded contexts."
constraint: "Diagnostic: Display discovered bounded contexts."
enforced_by: "DddStrategicPatternsArchUnitTest#Diagnostic: Display discovered bounded contexts"
status: informational
test_class: DddStrategicPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddStrategicPatternsArchUnitTest.groovy
tags: [strategic, archunit]
---

```groovy
when:
Map<String, BoundedContext> contexts = discoverBoundedContextPackages()
String sharedKernel = discoverSharedKernelPackage()

then:
println "=== Discovered Bounded Contexts ==="
contexts.each { pkg, annotation ->
  println "  ${annotation.name()}: ${pkg}"
  if (annotation.description()) {
    println "    Description: ${annotation.description()}"
  }
}
println "=== Shared Kernel ==="
println "  Package: ${sharedKernel}"
println "=================================="

// Verify we discovered the expected contexts
contexts.size() >= 1
sharedKernel != null
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
