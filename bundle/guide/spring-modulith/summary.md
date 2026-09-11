---
type: Section
title: Summary
chapter: Spring Modulith Implementation
source: guide
resource: dca-guide/topics/spring-modulith.md
tags: [guide, section]
---

**Spring Modulith implements [Domain-Centric Architecture](/guide/readme.md) by:**

1. **Enforcing Boundaries** - Modules = Bounded Contexts with verified boundaries
2. **Event-Driven** - Domain Events and Integration Events with guaranteed delivery
3. **Clear Structure** - `api/`, `events/`, `internal/` packages
4. **Progressive Complexity** - Start simple, grow as needed
5. **Testing** - Verify structure and test modules in isolation

**Migration Path:**
- Start with Spring Modulith modular monolith
- Extract to microservices when needed
- Event-based integration survives extraction

**Cross-References:**
- Core architecture: [Domain-Centric Architecture](/guide/readme.md)
- Deployment options: [Deployment Patterns](/guide/deployment-patterns.md)
- Team alignment: [Team Topologies Integration](/guide/team-topologies.md)

### Optional events and reliable delivery

Events are optional: an aggregate that never registers a fact needs no publisher dependency. `DCA-USE-009`
exempts a save only when the repository type argument and the aggregate's complete hierarchy can be inspected
and no registration is found; unresolved arguments, incomplete scans and undecidable external helpers retain the check.
Contracts belong in the configured `{context}/events/` segment. Translators belong in an outgoing adapter named after its channel — `event/` when delivery is in-process, `messaging/` once transport or an outbox relay lives there;
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
