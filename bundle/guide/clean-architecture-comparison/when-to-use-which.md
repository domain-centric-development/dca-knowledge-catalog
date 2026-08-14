---
type: Section
title: When to Use Which?
chapter: Domain-Centric Architecture vs Clean Architecture
source: guide
resource: implementing-domain-centric-architecture/clean-architecture-comparison.md
tags: [guide, section]
---

### Use Clean Architecture When:

✅ **Simpler domains**
- Business logic is straightforward
- Less complex domain rules
- CRUD-heavy applications

✅ **Smaller teams**
- Single team
- Co-located team
- Less need for bounded contexts

✅ **Learning architecture**
- Team new to layered architecture
- Want simpler mental model
- Don't need DDD complexity

✅ **Framework flexibility is priority**
- Frequently changing frameworks
- Experimenting with different technologies
- Framework independence is critical

### Use Domain-Centric Architecture When:

✅ **Complex domains**
- Rich business logic
- Complex business rules
- Domain-driven applications

✅ **Large systems**
- Multiple bounded contexts
- Need strategic design
- Complex integrations

✅ **Multiple teams**
- Team per bounded context
- Need clear team boundaries
- Conway's Law considerations

✅ **Event-driven systems**
- Asynchronous communication
- Eventual consistency
- Microservices or modular monolith

✅ **Long-term evolution**
- System will grow over time
- Need clear boundaries for extraction
- May evolve to microservices

> **See:** [Deployment Patterns](/guide/deployment-patterns.md) for evolution strategies
