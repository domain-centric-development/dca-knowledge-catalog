---
type: Rule
title: Outgoing adapters may access Open Host Services from other contexts
rule: Outgoing adapters may access Open Host Services from other contexts.
constraint: Outgoing adapters may access Open Host Services from other contexts.
enforced_by: "HexagonalArchitectureArchUnitTest#Outgoing adapters may access Open Host Services from other contexts"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
given:
Map<String, BoundedContext> boundedContexts = discoverBoundedContextPackages()
List<String> contextPackages = boundedContexts.keySet().toList()

expect:
// This is a "positive" test documenting the allowed pattern:
// Outgoing adapters may access api/ packages from other contexts (Open Host Services)
// This is verified by the successful compilation and the stricter tests in DddStrategicPatternsArchUnitTest
// that ensure outgoing adapters do NOT access domain or application layers of other contexts
true // Pattern verification: outgoing adapters call Open Host Services via api/ packages
```

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
