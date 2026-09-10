---
type: Section
title: "References & Further Reading"
chapter: Domain-Centric Architecture
source: guide
resource: dca-guide/README.md
tags: [guide, section]
---

Domain-Centric Architecture synthesizes ideas from multiple foundational works and thought leaders. Below are the key sources that have influenced this architectural approach.

### Domain-Driven Design

**Books:**
- **[Domain-Driven Design: Tackling Complexity in the Heart of Software](https://www.domainlanguage.com/ddd/)** by Eric Evans (2003)
  - The seminal work that introduced DDD concepts
  - Defines tactical patterns: Entities, Value Objects, Aggregates, Domain Services
  - Defines strategic patterns: Bounded Contexts, Ubiquitous Language, Context Mapping
  - ISBN: 978-0321125217

- **[Implementing Domain-Driven Design](https://vaughnvernon.com/implementing-domain-driven-design/)** by Vaughn Vernon (2013)
  - Practical guide to implementing DDD patterns
  - Deep dive into Aggregates and bounded contexts
  - Event Sourcing and CQRS patterns
  - ISBN: 978-0321834577

- **[Domain-Driven Design Distilled](https://vaughnvernon.com/domain-driven-design-distilled/)** by Vaughn Vernon (2016)
  - Concise introduction to DDD core concepts
  - Great starting point for learning DDD
  - ISBN: 978-0134434421

**Online Resources:**
- [Domain Language - Eric Evans](https://www.domainlanguage.com/) - Official DDD resources
- [DDD Community](https://github.com/ddd-crew) - Tools, patterns, and community resources

### Hexagonal Architecture (Ports & Adapters)

**Articles:**
- **[Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)** by Alistair Cockburn (2005)
  - Original article introducing Ports & Adapters pattern
  - Foundation for dependency inversion in Domain-Centric Architecture

**Books:**
- **[Get Your Hands Dirty on Clean Architecture](https://thombergs.gumroad.com/l/gyhdoca)** by Tom Hombergs (2019)
  - Practical implementation of Hexagonal Architecture
  - Detailed package structures and code examples
  - Spring Boot implementation patterns
  - ISBN: 978-1839211966

### Clean Architecture

**Books:**
- **[Clean Architecture: A Craftsman's Guide to Software Structure and Design](https://www.informit.com/store/clean-architecture-a-craftsmans-guide-to-software-structure-9780134494166)** by Robert C. Martin (2017)
  - Defines the dependency rule and layer structure
  - Framework independence principles
  - ISBN: 978-0134494166

**Articles:**
- **[The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)** by Robert C. Martin (2012)
  - Original blog post introducing Clean Architecture circles

### Team Topologies

**Books:**
- **[Team Topologies: Organizing Business and Technology Teams for Fast Flow](https://teamtopologies.com/book)** by Matthew Skelton & Manuel Pais (2019)
  - Four fundamental team types
  - Team interaction modes
  - Conway's Law and organizational design
  - ISBN: 978-1942788812

**Online Resources:**
- [Team Topologies Website](https://teamtopologies.com/) - Official resources and tools
- [Team Topologies Academy](https://teamtopologies.com/academy) - Training and workshops

### Spring Modulith

**Official Resources:**
- **[Spring Modulith Reference Documentation](https://docs.spring.io/spring-modulith/reference/)** - Official documentation
- **[Spring Modulith GitHub](https://github.com/spring-projects/spring-modulith)** - Source code and examples
- **[Spring Blog - Introducing Spring Modulith](https://spring.io/blog/2022/10/21/introducing-spring-modulith)** - Announcement and overview

**Presentations:**
- **[Spring Modulith – Spring for the Architecturally Curious Developer](https://www.youtube.com/watch?v=QX6lP-h-u8I)** by Oliver Drotbohm - SpringOne 2023

### Self-Contained Systems (SCS)

**Online Resources:**
- **[SCS Architecture](https://scs-architecture.org/)** - Official SCS website
  - Principles and characteristics
  - Comparison with microservices
  - Implementation examples

### Microservices & Distributed Systems

**Books:**
- **[Building Microservices: Designing Fine-Grained Systems](https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/)** by Sam Newman (2nd Edition, 2021)
  - Microservices patterns and practices
  - Service decomposition strategies
  - ISBN: 978-1492034025

- **[Monolith to Microservices](https://www.oreilly.com/library/view/monolith-to-microservices/9781492047834/)** by Sam Newman (2019)
  - Migration patterns from monolith to microservices
  - ISBN: 978-1492047841

### Event-Driven Architecture

**Books:**
- **[Designing Event-Driven Systems](https://www.confluent.io/designing-event-driven-systems/)** by Ben Stopford (2018)
  - Event-driven patterns with Apache Kafka
  - Free ebook from Confluent

**Articles:**
- **[Domain Events vs. Integration Events](https://www.kamilgrzybek.com/blog/posts/domain-events-vs-integration-events)** by Kamil Grzybek
  - Clear explanation of event types

### Software Architecture Patterns

**Books:**
- **[Patterns of Enterprise Application Architecture](https://www.martinfowler.com/books/eaa.html)** by Martin Fowler (2002)
  - Foundational enterprise patterns
  - Repository, Unit of Work, and more
  - ISBN: 978-0321127420

- **[Software Architecture: The Hard Parts](https://www.oreilly.com/library/view/software-architecture-the/9781492086888/)** by Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani (2021)
  - Modern architectural decision-making
  - Trade-off analysis
  - ISBN: 978-1492086895

### Influential Blogs & Communities

**Blogs:**
- **[Martin Fowler's Blog](https://martinfowler.com/)** - Software architecture patterns and practices
- **[Vaughn Vernon's Blog](https://vaughnvernon.com/)** - DDD patterns and implementations
- **[Udi Dahan's Blog](https://udidahan.com/)** - SOA and DDD insights
- **[Tom Hombergs' Blog (Reflectoring)](https://reflectoring.io/)** - Clean/Hexagonal Architecture tutorials

**Communities:**
- **[DDD/CQRS Google Group](https://groups.google.com/g/dddcqrs)** - Active DDD community
- **[Software Architecture Slack](https://softwarearchitecture.slack.com/)** - Architecture discussions
- **[Virtual DDD](https://virtualddd.com/)** - Online DDD meetups and resources

### Related Patterns & Practices

**CQRS (Command Query Responsibility Segregation):**
- **[CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)** by Martin Fowler
- **[CQRS Journey](https://docs.microsoft.com/en-us/previous-versions/msp-n-p/jj554200(v=pandp.10))** by Microsoft patterns & practices

**Event Sourcing:**
- **[Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)** by Martin Fowler
- **[Event Sourcing Basics](https://eventstore.com/blog/what-is-event-sourcing/)** by Event Store

**Aggregates:**
- **[Effective Aggregate Design](https://www.dddcommunity.org/library/vernon_2011/)** by Vaughn Vernon (3-part series)

### Acknowledgments

Domain-Centric Architecture stands on the shoulders of giants. Special recognition to:

- **Eric Evans** - For Domain-Driven Design and the concept of Bounded Contexts
- **Alistair Cockburn** - For Hexagonal Architecture and the Ports & Adapters pattern
- **Robert C. Martin (Uncle Bob)** - For Clean Architecture and the Dependency Rule
- **Vaughn Vernon** - For practical DDD implementation guidance
- **Matthew Skelton & Manuel Pais** - For Team Topologies and organizational patterns
- **Tom Hombergs** - For practical Hexagonal Architecture implementation examples
- **Oliver Drotbohm** - For Spring Modulith framework
- **The DDD Community** - For continuous evolution of patterns and practices

### Contributing to This Documentation

This documentation is a living resource. Contributions, corrections, and improvements are welcome. The patterns and practices described here continue to evolve based on real-world experience and community feedback.

Repository and Store interfaces may live in the use-case package that alone needs
them; move reused ports into `application/shared`. A `*Response` belongs to an
adapter, incoming or outgoing: a provider response is an outgoing adapter model.

Entity constructors may be public. Construction belongs to the entity itself or
to an aggregate, entity or cooperating factory in the same context's domain layer.
Adapters reconstitute through the aggregate's or factory's reconstitution method,
without raising a creation event. The architecture check cannot identify ownership
inside a context: another aggregate in that same context passes, so review must
verify the actual invariant boundary.

### Wiring and domain metadata

Use cases may be registered by configuration or carry an injectable stereotype. A
static reference does not prove registration, and runtime scanning need not leave one;
`DCA-NAM-002` therefore only lists unannotated Java operations as an informational
diagnostic. It never fails. .NET registration is code and has no stereotype counterpart.
Outgoing adapters may reuse global and own-module infrastructure; another module's
infrastructure remains private (`DCA-HEX-005`).

Domain metadata is classified by configured roles, including members and composed
metadata. Types prohibit injectable/container, persistence-entity and transactional
roles; fields (and .NET properties) prohibit injection-site and persistence-mapping
roles; methods prohibit transaction and event-listener roles, plus setter injection
except on events; constructors prohibit injection-site metadata. Java detects direct
and meta-annotations. .NET checks an attribute's namespace and every base attribute
type against persistence, injection, transaction and container namespace lists; no
event-listener attribute role is configured by default. Unclassified metadata is
allowed by this check, without claiming it harmless. Events, services, factories and
specifications have exclusive `ADV-004/011/015/018` ownership; `ONI-003` owns the
remaining domain-model types, so one type is never reported twice for metadata.

### Operation boundaries and declared contracts

Ordinary use cases do not invoke other use cases, whether directly, through an
input port, or through an application helper. Shared collaborators that do not call
operations remain valid. `DCA-USE-016` follows dependencies within the module's
application layer and reports `Caller -> Target [via Helper]`. Explicit coordination
uses a caller-side exception, for example
`dca.rule.DCA-USE-016.ignore=^com\.example\.module\.application\.coordinate\.CoordinatorUseCase -> `.
This permits the coordinator to invoke operations; it does not permit an operation
to invoke the coordinator, and `DCA-CYC-005` still detects coordination cycles,
including two operations inside the same feature. No coordinator marker is implied.
When a reliable exception cannot be expressed, use WARN with a recorded reason and
review the coordinator's transaction boundaries and partial-failure semantics manually.
Reflection, container lookups and calls through interfaces outside the InputPort
hierarchy also require manual review.

The input port describes the complete effective public instance surface (`DCA-USE-017`).
Declared and inherited business methods, unrelated-interface methods and public
properties/getters/setters must be in the input-port contract. Constructors, Object
members and compiler-generated members are exempt; a property accessor is not exempt
merely because it has a special runtime name. Ordinary, inherited and explicit
input-port implementations are valid. In .NET, `DCA-NET-003` separately validates
`IUseCase<TIn,TOut>.ExecuteAsync(input, CancellationToken)` returning `Task<T>` through
the interface map; it does not count declared public methods.

For every declared ACL interaction, the matching adapter must contain a class that
uses that upstream's channel contract and the declaring context's own domain or
application model (`DCA-MAP-008`). Two translators for different upstreams may share
an adapter package. Evidence for one upstream does not satisfy another interaction.
This identifies a structural translation site, without proving translation quality.

### Optional events and reliable delivery

Events are optional: an aggregate that never registers a fact needs no publisher dependency. `DCA-USE-009`
exempts a save only when the repository type argument and the aggregate's complete hierarchy can be inspected
and no registration is found; unresolved arguments, incomplete scans and undecidable external helpers retain the check.
Contracts belong in the configured `{context}/events/` segment. Translators belong in `adapter/outgoing/event/`;
transport and storage are separate adapters. Schema versions belong in integration-event type metadata.
`DCA-ADV-006/007` use a name heuristic for `schemaVersion`, `eventVersion`, `contractVersion`; a business `version` is allowed.

An in-process registry may deliver domain events within a context **or integration events between contexts**.
Process location does not determine event classification. Synchronous delivery is atomic only for local resources
participating in the same transaction; a synchronous remote effect cannot be rolled back with the aggregate.
For an external effect, either (A) an own-context async consumer receives a durably captured domain fact, or
(B) an own-context synchronous translator captures an integration contract consumed asynchronously. Cross-context
consumers always use the integration contract. No broker is required to cross a context boundary.

Capture the publication in the aggregate transaction; establish delivery eligibility with commit, then wake the
worker after commit. Recovery reads committed publications even when that wakeup was lost. Track completion per
consumer/effect, retry only unfinished work with bounded attempts and exponential backoff, retain terminal failures
for inspection and deliberate replay. Reuse the original payload and `eventId + consumer + effect` identity.
Provider acceptance is the acknowledgement point. If the process stops after acceptance but before local acknowledgement,
provider-supported idempotency can deduplicate a repeated key; without it, a duplicate external effect remains possible.
For each concrete effect, decide whether rendering/template version and recipient are captured or resolved later;
the event snapshot alone does not decide these. No universal email policy is implied.

`DCA-USE-012` checks transaction-boundary evidence in Java and .NET (`FrameworkTypes.TransactionalAttribute` is empty
by default). Static call graphs cannot prove lambda containment: publishing after an empty boundary in the same
method passes this check. Verify runtime containment and rollback separately. `.NET DCA-USE-013` remains unavailable;
review remote-capable calls and transaction scope explicitly.

## Related mentions (heuristic)

- [InputPort](/marker/port-in/inputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
