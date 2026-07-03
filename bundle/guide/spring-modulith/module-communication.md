---
type: Section
title: Module Communication
chapter: Spring Modulith Implementation
source: guide
resource: implementing-domain-centric-architecture/spring-modulith.md
tags: [guide, section]
---

### Option 1: Domain Events (Preferred - Async)

```java
// Publisher (Order Module)
@Service
class CreateOrderService implements OrderApi {
    private final ApplicationEventPublisher events;

    @Transactional
    public OrderResponse createOrder(CreateOrderRequest request) {
        Order order = Order.create(...);
        repository.save(order);

        // Publish event
        events.publishEvent(new OrderCreatedEvent(...));

        return toResponse(order);
    }
}

// Consumer (Inventory Module)
@Component
class OrderEventListener {
    @ApplicationModuleListener
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    void on(OrderCreatedEvent event) {
        // Reserve stock for order
        inventoryService.reserveStock(event.orderId());
    }
}
```

**Benefits:**
- ✅ Loose coupling
- ✅ Async processing
- ✅ Event persistence (with Spring Modulith JPA)
- ✅ Automatic retry
- ✅ Transaction boundaries

### Option 2: Direct API Calls (Sync)

```java
// Publisher (Order Module API)
// order/api/OrderApi.java
public interface OrderApi {
    OrderResponse createOrder(CreateOrderRequest request);
    OrderResponse findOrder(String orderId);
}

// Implementation (Order Module)
@Service
class CreateOrderService implements OrderApi {
    // Implementation
}

// Consumer (Customer Module)
@Service
class CustomerService {
    private final OrderApi orderApi; // injected from order module

    public CustomerStats getCustomerStats(String customerId) {
        var orders = orderApi.findOrdersByCustomer(customerId);
        return calculateStats(orders);
    }
}
```

**Module Dependency:**
```java
// customer/package-info.java
@ApplicationModule(
    allowedDependencies = {"order::api"}  // Can only use order.api
)
package com.company.ecommerce.customer;
```
