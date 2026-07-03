# note

- [Domain vs integration events in an outbox / event store](outbox-domain-vs-integration-events.md) — Should an outbox store domain events or integration events? The short answer: an **external** (broker) outbox stores ...
- [The Store marker has no governing ArchUnit rules (governance gap)](store-marker-has-no-governing-rules.md) — The [Store marker](/marker/port-out/store.md) (`Store extends OutputPort`) is documented in the book

**Extensible zone — authored, not generated from sources.** `note/` nodes are written by a human or an LLM and **survive** `generate` (only this `index.md` is regenerated). Add one as `note/<slug>.md` with frontmatter `type: Note`, `title:`, `tags: [note]`, then link into the skeleton with bundle-relative links (e.g. `[UseCase](/marker/port-in/usecase.md)`).
