---
type: Section
title: Dependency Rules
chapter: Architecture Reference Guide
source: guide
resource: implementing-domain-centric-architecture/architecture-reference-guide.md
tags: [guide, section]
---

### The Golden Rule
**Dependencies always point INWARD**

```
Infrastructure → Adapters → Application → Domain
```

No inner layer knows about outer layers.

### Layer Dependency Matrix

| Layer | Can Depend On | Cannot Depend On |
|-------|---------------|------------------|
| **Domain** | Nothing (maybe Common) | Application, Adapters, Infrastructure |
| **Application** | Domain, Common | Adapters, Infrastructure |
| **Adapters** | Application, Domain, External libs, Common | Infrastructure, Other adapters* |
| **Infrastructure** | Everything | Nothing |

*Adapter-to-adapter dependencies are a code smell but sometimes pragmatically necessary

### What Adapters Can Inject

#### ✅ ALLOWED in Adapters:

1. **Application layer components**
```java
@RestController
public class OrderRestController {
    private final CreateOrderUseCase createOrder;  // ✅ Application port
}
```

2. **Domain objects** (transitively)
```java
Order order = Order.create(...);  // ✅ Domain object
```

3. **External framework/library components**
```java
@RestController  // ✅ Spring from external library
public class OrderRestController {
    @Autowired  // ✅ Spring DI
    private final KafkaTemplate kafka;  // ✅ External library
}
```

4. **Common module components**
```java
@Component
public class OrderAdapter {
    private final Clock clock;  // ✅ From common module
}
```

#### ❌ NOT ALLOWED in Adapters:

1. **Infrastructure layer classes**
```java
@RestController
public class OrderRestController {
    private final SpringConfig config;  // ❌ WRONG!
    private final MetricsCollector metrics;  // ❌ If in infrastructure
}
```

2. **Configuration beans from Infrastructure**
```java
private final DatabaseConfig dbConfig;  // ❌ WRONG!
```

### Infrastructure vs Framework Distinction

**Important**: Your **Infrastructure layer** is different from **external frameworks**!

```java
// ✅ CORRECT - Using external framework (Spring)
@RestController  // Spring annotation - OK in adapters
public class OrderRestController {
    @Autowired  // Spring DI - OK
    private final CreateOrderUseCase useCase;
}

// ❌ WRONG - Depending on YOUR infrastructure layer
@RestController
public class OrderRestController {
    private final MyAppMetricsCollector metrics;  // ❌ If this is in infrastructure/
}
```

**Rule**: Adapters can use external frameworks but not your custom Infrastructure layer.

### Fixing Wrong Dependencies

**Problem**: Adapter needs something from Infrastructure

**Solution 1**: Move it to Application as a port
```java
// application/ports/out/MetricsPublisher.java
public interface MetricsPublisher {
    void increment(String metric);
}

// infrastructure/metrics/PrometheusMetrics.java
public class PrometheusMetrics implements MetricsPublisher {
    // Implementation
}
```

**Solution 2**: Move it to Common module
```java
// common/metrics/MetricsCollector.java
public class MetricsCollector {
    // Shared utility
}

// Both adapters and infrastructure can depend on common
```

**Solution 3**: Move concern into Application service
```java
// Application service handles it, not the adapter
public class CreateOrderService implements CreateOrderUseCase {
    private final MetricsPublisher metrics;

    public OrderId execute(CreateOrderCommand command) {
        metrics.increment("orders.created");  // Handled in application
        // ...
    }
}
```

---
