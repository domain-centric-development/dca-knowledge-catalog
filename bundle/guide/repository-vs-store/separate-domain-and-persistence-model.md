---
type: Section
title: Separate domain and persistence model
chapter: Repository vs. Store
source: guide
resource: dca-guide/architecture/repository-vs-store.md
tags: [guide, section]
---

A repository implementation maps between two models: the aggregate the domain owns, and the
persistence type the ORM owns. The aggregate never carries persistence metadata — the mapping lives
in the outgoing adapter.

```java
// {context}/domain/model/Order.java — pure domain, no ORM metadata
public class Order implements AggregateRoot<Order, OrderId> {
    private final OrderId id;
    private final CustomerId customerId;
    private Money total;

    public void addLine(OrderLine line) { /* invariants */ }
    public void cancel() { /* invariants */ }
}

// {context}/adapter/outgoing/persistence/OrderEntity.java — the persistence model
@Entity
@Table(name = "orders")
class OrderEntity {
    @Id private String id;
    private String customerId;
    private BigDecimal totalAmount;
    private String currency;

    Order toDomain() {
        return Order.reconstitute(new OrderId(id), new CustomerId(customerId),
                                  new Money(totalAmount, Currency.getInstance(currency)));
    }

    static OrderEntity fromDomain(Order order) { /* … */ }
}

// {context}/adapter/outgoing/persistence/JpaOrderRepository.java — implements the output port
@Component
class JpaOrderRepository implements OrderRepository {
    private final SpringDataOrderRepository orders;

    @Override public Order save(Order order) {
        return orders.save(OrderEntity.fromDomain(order)).toDomain();
    }

    @Override public Optional<Order> findById(OrderId id) {
        return orders.findById(id.value()).map(OrderEntity::toDomain);
    }
}
```

Reconstitution goes through the aggregate's own reconstitution method, which raises no creation
event — an adapter must never rebuild an aggregate by calling its creation factory.

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
