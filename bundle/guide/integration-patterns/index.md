# integration-patterns

- [A Bounded Context Is a Deep Module](a-bounded-context-is-a-deep-module.md) — A bounded context is a *deep module* in the sense of Ousterhout (*A Philosophy of Software
- [A process that spans several transactions](a-process-that-spans-several-transactions.md) — Some flows outlive one transaction: they take several steps, wait for an answer, and pick the next step from what
- [Composite Adapter Pattern](composite-adapter-pattern.md) — When a context needs data from **multiple** Open Host Services, use a **Composite Adapter** to aggregate the data in ...
- [Declaring Context Relationships in Code](declaring-context-relationships-in-code.md) — Context-map relationships are declared on the bounded context's `package-info.java`, next to
- [Different Bounded Contexts](different-bounded-contexts.md) — Different Bounded Contexts
- [Domain services over supplied facts](domain-services-over-supplied-facts.md) — An aggregate answers questions about its own state. When a calculation combines facts from other aggregates or
- [Enriched Read Model Pattern](enriched-read-model-pattern.md) — When you need to **combine persisted data with fresh external data** for rich domain logic (e.g., comparing original ...
- [Factory for Cross-Context Assembly](factory-for-cross-context-assembly.md) — Use a **Factory** to assemble enriched domain objects from data fetched via ports.
- [Open Host Service Pattern](open-host-service-pattern.md) — For synchronous cross-context queries, use the Open Host Service pattern.
- [Optional events and reliable delivery](optional-events-and-reliable-delivery.md) — Events are optional: an aggregate that never registers a fact needs no publisher dependency. `DCA-USE-009`
- [Reacting to an event](reacting-to-an-event.md) — A reaction to an event goes **adapter → command → use case**. That holds for a contract from another context
- [Same Bounded Context](same-bounded-context.md) — Same Bounded Context
