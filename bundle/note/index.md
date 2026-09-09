# note

- [Domain vs integration events in an outbox / event store](outbox-domain-vs-integration-events.md) — Events are optional: an aggregate that never registers a fact needs no publisher dependency. `DCA-USE-009`

**Extensible zone — authored, not generated from sources.** `note/` nodes are written by a human or an LLM and **survive** `generate` (only this `index.md` is regenerated). Add one as `note/<slug>.md` with frontmatter `type: Note`, `title:`, `tags: [note]`, then link into the skeleton with bundle-relative links (e.g. `[UseCase](/marker/port-in/usecase.md)`).
