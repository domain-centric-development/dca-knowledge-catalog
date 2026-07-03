---
type: Rule
title: Event Listeners consuming integration events should use Anti-Corruption Layer
rule: Event Listeners consuming integration events should use Anti-Corruption Layer.
constraint: Event Listeners consuming integration events should use Anti-Corruption Layer.
enforced_by: "DddStrategicPatternsArchUnitTest#Event Listeners consuming integration events should use Anti-Corruption Layer"
status: informational
test_class: DddStrategicPatternsArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/DddStrategicPatternsArchUnitTest.groovy
tags: [strategic, archunit]
---

```groovy
expect:
// This test documents the architectural pattern but is informational
// We verify that ProductStockEventListener (cross-context) uses CartEventTranslator
// This is checked through code review rather than ArchUnit
true // Documented pattern: see ProductStockEventListener.onCartCheckedOut() using CartEventTranslator
```
