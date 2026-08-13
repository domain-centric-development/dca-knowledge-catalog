---
type: ADR
title: "ADR-031: A Repository Hands Out Copies — Real Persistence Is the Default"
adr: 31
status: accepted
pattern: A repository hands out copies. An adapter that cannot honour that is not the default.
resource: ai-architecture-sample/docs/architecture/adr/adr-031-persistence-adapters-as-the-default.md
tags: [adr, repository]
---

A repository hands out copies. An adapter that cannot honour that is not the default.

**Consequences:** A forgotten `save` fails · The mapping boundary is visible · The port has a contract test · Two persistence styles are demonstrated · Copying costs · Nothing survives a restart yet · Four contexts still hand out live references

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
