---
type: Section
title: Grouping use cases into features
chapter: Java Package Structure
source: guide
resource: dca-guide/architecture/package-structure.md
tags: [guide, section]
---

`withOperationContainers("usecases")` (C#: `WithOperationContainers("UseCases")`)
can declare an organisational segment such as `application/usecases/<usecase>`.
Configured segments do not contribute to flat/grouped depth; the operation class's
marker or suffix determines the root. Supporting subfolders are allowed. A context
mixing flat and feature-grouped operations remains invalid after normalization.

DCA has three scales below the system: the **bounded context**, the **layer**, and the **use case**. When the
application layer of one context grows — a dozen use-case packages in one flat list — a fourth, optional scale
fills the gap between layer and use case: the **feature**.

```text
system -> bounded context -> layer -> feature -> use case
```

A *feature* is a domain-named group of related use cases inside one bounded context. It is a navigation and
cohesion boundary and nothing more: not a layer, not a module, not an aggregate owner, not a deployment unit.

The two canonical forms of the application layer — and the only two — are:

```text
application/{usecase}/              # flat: a small context
application/{feature}/{usecase}/    # grouped: cohesive clusters have emerged
```

A context that has grown into features:

```text
checkout/
├── domain/                              # concepts owned by the whole context — never mirrored by feature
│   ├── model/
│   ├── service/
│   ├── event/
│   └── readmodel/
├── application/
│   ├── session/                         # feature
│   │   ├── startcheckout/               # use case — input port, implementation, command/query, result
│   │   ├── getactivecheckoutsession/
│   │   ├── getcheckoutsession/
│   │   └── getconfirmedcheckoutsession/
│   ├── checkoutcompletion/              # feature — a term of the ubiquitous language, not UI jargon
│   │   ├── submitbuyerinfo/
│   │   ├── getshippingoptions/
│   │   ├── submitdelivery/
│   │   ├── getpaymentproviders/
│   │   ├── submitpayment/
│   │   └── confirmcheckout/
│   ├── cartsync/
│   │   └── synccheckoutwithcart/
│   └── shared/                          # context-wide output ports only
├── adapter/
│   ├── incoming/
│   │   ├── web/{session,checkoutcompletion}/   # protocol first, feature below it
│   │   └── event/cartsync/
│   └── outgoing/{persistence,payment,cart,product,event}/   # by technology or partner, as before
├── api/
├── events/
└── infrastructure/
```

**The eight rules of the feature scale:**

1. **Flat first.** A small context keeps `application/{usecase}/`. Add the feature level when cohesive clusters
   have emerged and the flat list has become hard to navigate. The "about ten entries" guidance above is a prompt
   to *evaluate* grouping, not a numeric law.
2. **Feature names come from the ubiquitous language**, lowercase: `cartrecovery`, `checkoutcompletion`,
   `session`. Never technical buckets (`commands`, `queries`, `handlers`, `services`, `utils`) and never delivery
   mechanisms (`web`, `api`).
3. **The use case stays the smallest application unit.** Its input port, implementation, command or query,
   result and any use-case-specific output port stay together in the use-case package.
4. **`application/shared` stays context-wide.** Repository and Store interfaces continue to live there
   (`DCA-TAC-014`, `DCA-TAC-019`); there is no `application/{feature}/shared`. A port used by one use case stays
   with that use case, a port used by several belongs in `application/shared`.
5. **The domain is organised by concept, not mirrored by feature.** Aggregates and value objects belong to the
   bounded context and may serve several features — a feature owns no aggregate.
6. **Incoming adapters may mirror features *below* their protocol:** `adapter/incoming/web/{feature}`,
   `adapter/incoming/event/{feature}`. The protocol segment stays first, so the adapter vocabulary and its rules
   (`DCA-NAM-011`) keep working. Outgoing adapters stay organised by technology or partner.

   **Both sides name the counterpart — they differ in what the counterpart is.** Incoming, it is the channel the
   traffic arrives on: `web`, `api`, `event`, `mcp`. One segment per *client implementation*, so when a context
   consumes from two sources that are genuinely different code — a broker topic and a cloud queue, two upstreams
   with their own deserialisation, authentication and retry semantics — they are siblings at that level
   (`adapter/incoming/kafka/`, `adapter/incoming/sqs/`), not two folders under one `event/`. Features stay below
   them. Outgoing, the counterpart is who the adapter talks to: `persistence`, `payment`, `product`, `messaging`.

   The asymmetry is worth keeping in view when reading these trees. An incoming adapter is a client: it receives,
   translates through the anti-corruption layer, calls an input port, and stores nothing. The outgoing side is
   where the machinery accumulates — the relay that drains the outbox, the retries, the transport — which is why a
   single outgoing segment often holds far more than its incoming counterpart, against one published contract.
7. **One form per context.** Within one context, use cases are either all flat or all grouped once a migration is
   complete; a lasting mixture leaves the reader guessing whether a direct child of `application/` is a feature,
   a use case or a leftover. A short-lived mixed state during one refactoring is fine — move one whole context
   atomically. `DCA-USE-014` checks this; `DCA-CYC-005` keeps the feature (or, in a flat context, use-case)
   packages free of cycles — a one-directional dependency between two features is allowed.
8. **A vertical slice is not a feature.** `{context}/{feature}/{domain,application,adapter}` puts a layer segment
   below the feature, so the structural module discovery rightly treats every slice as a module of its own and the
   isolation rules demand communication through `api`/`events`. If that boundary is what you want, model it as a
   module and ask whether it is a separate bounded context. Do not weaken the isolation rules to let a shared
   aggregate span such slices.

A feature relieves *package pressure*. It is not evidence against splitting a context: when language, model or
team ownership have diverged, split the context — grouping use cases does not resolve that.

---

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
