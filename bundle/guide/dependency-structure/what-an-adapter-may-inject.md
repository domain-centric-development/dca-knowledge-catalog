---
type: Section
title: What an adapter may inject
chapter: Dependency Structure
source: guide
resource: dca-guide/architecture/dependency-structure.md
tags: [guide, section]
---

Allowed in either direction:

- **Application components** — an input port in an incoming adapter, an output port the adapter implements
- **Domain objects**, transitively through the application layer
- **External frameworks and libraries** — `@RestController`, a `KafkaTemplate`, an HTTP client
- **Shared-kernel types** — universal value objects, shared application ports, and the shared
  kernel's own infrastructure

**Infrastructure depends on the direction of the adapter**, and this is where the two halves of the
adapter layer part company:

- An **incoming adapter** reaches no infrastructure at all — neither the global
  `{base}.infrastructure` nor its own module's `{module}.infrastructure` (`DCA-HEX-004`). A
  controller that needs a technical capability has two honest options: the use case needs it too and
  declares an output port, or it is adapter mechanics and stays a plain class in the adapter package.
  Using the identity port to resolve the caller is fine — it translates request context into the
  project's language; cookie or token handling is not a port.
- An **outgoing adapter** may use the global infrastructure and its own module's infrastructure —
  that is where a persistence adapter meets the `EntityManager` your configuration produced. What it
  may not touch is *another* module's infrastructure (`DCA-HEX-005`), which would tie two contexts
  together through their wiring.

```java
// adapter/incoming/web/OrderRestController.java
@RestController
class OrderRestController {
    private final CreateOrderInputPort createOrder;     // ✅ input port
    private final KafkaTemplate<String, String> kafka;  // ✅ external library
    private final DatabaseConfig config;                // ❌ infrastructure — not from here
}

// adapter/outgoing/persistence/JpaOrderRepository.java
@Component
class JpaOrderRepository implements OrderRepository {
    private final EntityManagerFactory factory;         // ✅ own module's infrastructure
    private final PaymentDataSourceConfig foreign;      // ❌ another module's infrastructure
}
```
