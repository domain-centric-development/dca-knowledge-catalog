---
type: Rule
title: The rules of the Layered Architecture should be followed
rule: The rules of the Layered Architecture should be followed.
constraint: The rules of the Layered Architecture should be followed.
enforced_by: "LayeredArchitectureArchUnitTest#The rules of the Layered Architecture should be followed"
status: disabled
test_class: LayeredArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/LayeredArchitectureArchUnitTest.groovy
tags: [layered, archunit]
---

```groovy
expect:
// NOTE: Traditional layered architecture rules don't align well with Hexagonal Architecture.
//
// In Hexagonal Architecture (Ports & Adapters):
// - Application layer defines BOTH input ports (use cases) AND output ports (repository interfaces)
// - Incoming adapters depend on application (implement/use input ports)
// - Outgoing adapters depend on application (implement output port interfaces)
//
// This means BOTH adapter types depend on the application layer, which violates traditional
// layered architecture where "ApplicationServices may only be accessed by IncomingAdapters".
//
// The correct Hexagonal Architecture dependency rules are tested in HexagonalArchitectureArchUnitTest instead.
//
// Test disabled to avoid false violations in a Hexagonal Architecture codebase.

true // Test disabled - see comment above
```
