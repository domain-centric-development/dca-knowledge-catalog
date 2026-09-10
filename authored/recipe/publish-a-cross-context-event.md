---
type: Recipe
title: Publish a cross-context event
tags: [recipe, events, integration-event, outbox]
review: reviewed
owner: DCA catalog maintainers
evidence: [/guide/readme/integration-patterns.md, /rule/strategic/dca-str-007.md, /rule/advanced/dca-adv-005.md, /rule/advanced/dca-adv-006.md, /marker/tactical/domainevent.md, /marker/tactical/integrationevent.md, /guide/readme/rules.md]
---

Make one bounded context react to something that happened in another, or notify an external system. The event **crosses a boundary**, so it must become an `IntegrationEvent` — never a raw domain event. First decide the delivery mode; the wrong choice is the most common event mistake.

## Step 0 — decide (do this first)

Read [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md). Outcome:

- **Within the same context** → may stay a domain event; durable async delivery still needs transactional capture. Stop here.
- **Cross-context, in-process or over transport** → continue below.

## Steps (cross-context)

1. **Raise the domain event** in the aggregate as usual ([Add an aggregate](/recipe/add-an-aggregate.md)).
2. **Define the integration event** in the configured `{context}/events/` segment — a serializable record of primitives only, implementing `IntegrationEvent` and annotated with `@IntegrationEventType(name, version)` — the contract identity as a class property ([Integration patterns](/guide/readme/integration-patterns.md)).
3. **Translate in an ACL adapter, inside the transaction** — a synchronous listener on the domain event maps it to the integration event and writes the transactional-outbox row in the publishing transaction. Never translate after commit.
4. **Relay out of band** — a poller (plus an after-commit fast path) claims rows, sends to the broker, marks processed; retry with backoff. The outbox stores *your* integration event; the foreign wire payload is built at delivery by the outbound adapter (the ACL to the foreign contract).
5. **Consume** on the other side in `adapter/incoming/messaging/`, translate back through that context's ACL, invoke its use case.
6. **Verify** — `./gradlew test-architecture`.

## Rules to satisfy (build-time checklist)

- [Integration contracts belong in the configured events segment](/rule/strategic/dca-str-007.md)
- [Integration Events must be annotated with IntegrationEventType](/rule/advanced/dca-adv-005.md)
- [Integration schema versions belong in type metadata (business version is allowed)](/rule/advanced/dca-adv-006.md)
- Do **not** serialize raw domain events across the boundary — see the [pitfall](/pitfall/storing-domain-events-in-an-external-outbox.md)


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


## Anchors

- Decision: [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md)
- Note: [Domain vs integration events in an outbox](/note/outbox-domain-vs-integration-events.md)
- Pitfall: [Storing domain events in an external outbox](/pitfall/storing-domain-events-in-an-external-outbox.md)
- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- Guide: [Integration patterns](/guide/readme/integration-patterns.md) · [Layer rules](/guide/readme/rules.md)
