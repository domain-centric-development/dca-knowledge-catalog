---
type: Section
title: "Related Patterns & Practices"
chapter: "References & Further Reading"
source: guide
resource: dca-guide/architecture/references.md
tags: [guide, section]
---

**CQRS (Command Query Responsibility Segregation):**
- **[CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)** by Martin Fowler
- **[CQRS Journey](https://docs.microsoft.com/en-us/previous-versions/msp-n-p/jj554200(v=pandp.10))** by Microsoft patterns & practices

**Event Sourcing:**
- **[Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)** by Martin Fowler
- **[Event Sourcing Basics](https://eventstore.com/blog/what-is-event-sourcing/)** by Event Store

**Aggregates:**
- **[Effective Aggregate Design](https://www.dddcommunity.org/library/vernon_2011/)** by Vaughn Vernon (3-part series)

**Results and exceptions:**
- **[Against Railway-Oriented Programming](https://fsharpforfunandprofit.com/posts/against-railway-oriented-programming/)** by Scott Wlaschin
  - The author of railway-oriented programming on where it stops: results for what the domain models and a
    caller handles, exceptions for what nobody handles where it happens
  - The cut DCA draws between a returned refusal and a thrown failure
