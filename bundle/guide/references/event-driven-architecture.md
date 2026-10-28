---
type: Section
title: Event-Driven Architecture
chapter: "References & Further Reading"
source: guide
resource: dca-guide/architecture/references.md
tags: [guide, section]
---

**Books:**
- **[Designing Event-Driven Systems](https://www.confluent.io/designing-event-driven-systems/)** by Ben Stopford (2018)
  - Event-driven patterns with Apache Kafka
  - Free ebook from Confluent

**Articles:**
- **[Domain events: design and implementation](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation)** — Microsoft .NET microservices guidance
  - Where the line between a domain event and an integration event falls, and what each one may carry

**Long-running processes:**
- **[Sagas](https://www.cs.princeton.edu/research/techreps/598)** by Hector Garcia-Molina and Kenneth Salem (SIGMOD 1987)
  - A long-lived transaction as steps that commit one by one, each with a compensating step
- **[Process Manager](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ProcessManager.html)** in *Enterprise Integration Patterns* by Gregor Hohpe and Bobby Woolf (2003)
  - A central unit that keeps the state of a sequence and decides the next step
