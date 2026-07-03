---
type: Rule
title: "Port adapters (incoming and outgoing) must not communicate directly with each other within the same context"
rule: "Port adapters should communicate through application services, not directly (event consumers are the exception)."
constraint: "Port adapters (incoming and outgoing) must not communicate directly with each other within the same context."
enforced_by: "HexagonalArchitectureArchUnitTest#Port adapters (incoming and outgoing) must not communicate directly with each other within the same context"
status: enforced
test_class: HexagonalArchitectureArchUnitTest
resource: ai-architecture-sample/src/test-architecture/groovy/de/sample/aiarchitecture/HexagonalArchitectureArchUnitTest.groovy
tags: [hexagonal, archunit]
---

```groovy
expect:
// Incoming adapters within a context should not directly call outgoing adapters
// Exception: Event consumers (..adapter.incoming.event..) may depend on integration events
// in other contexts' events/ packages — this is the standard cross-context integration pattern
noClasses()
  .that().resideInAPackage(INCOMING_ADAPTER_PACKAGE)
    .and().resideOutsideOfPackage("..adapter.incoming.event..")
  .should().dependOnClassesThat().resideInAPackage(OUTGOING_ADAPTER_PACKAGE)
  .because("Port adapters should communicate through application services, not directly (event consumers are the exception)")
  .check(allClasses)

// Note: Outgoing adapters MAY access api/ packages from OTHER contexts
// when calling Open Host Services (e.g., Cart's ProductDataAdapter calls Product's ProductCatalogService)
// This is the intended cross-context communication pattern via api/ packages
```
