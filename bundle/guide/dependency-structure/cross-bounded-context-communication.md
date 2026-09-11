---
type: Section
title: Cross-Bounded Context Communication
chapter: Dependency Structure
source: guide
resource: dca-guide/architecture/dependency-structure.md
tags: [guide, section]
---

```mermaid
flowchart TB
    subgraph ORDER["ORDER CONTEXT"]
        direction TB
        UC["CreateOrderUseCase<br><i>application</i>"]
        DE["OrderCreated<br><i>domain event</i>"]
        MAP["OrderEventMapper<br><i>adapter/outgoing</i>"]
        IE["OrderCreatedEvent<br><i>integration event</i>"]
        UC -- publishes --> DE
        DE -- via DomainEventPublisher --> MAP
        MAP -- translates --> IE
    end

    BROKER{{"Publication and delivery<br><i>two shapes — see below</i>"}}

    subgraph INVENTORY["INVENTORY CONTEXT"]
        direction TB
        CONS["OrderEventConsumer<br><i>adapter/incoming</i>"]
        ACL["ExternalEventToCommandMapper<br><i>anti-corruption layer</i>"]
        PORT["ReserveStockInputPort<br><i>application</i>"]
        UC2["ReserveStockUseCase<br><i>application</i>"]
        CONS -- via ACL --> ACL
        ACL -- builds ReserveStockCommand --> PORT
        PORT -. implemented by .-> UC2
    end

    IE --> BROKER --> CONS
```

Neither context knows the other's model. What crosses the boundary is the
integration contract; the anti-corruption layer turns it into this context's own
command before any use case sees it.

## Related mentions (heuristic)

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
