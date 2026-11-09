---
type: Reference
title: DOMAIN LAYER RULES — General Domain Rules
tags: [reference]
evidence_for: "/guide/rules/domain-layer-rules.md#general-domain-rules"
---

[Full node and context](/guide/rules/domain-layer-rules.md#general-domain-rules). This is an evidence excerpt; retain the parent selection and caveats.

### General Domain Rules
- Domain contains business logic only
- Domain is framework-agnostic
- Domain is persistence-agnostic
- Domain is UI-agnostic
- Domain uses pure language features
- Domain can be tested without infrastructure
- Domain reflects business, not database structure
- Ubiquitous Language used throughout domain code
- The context's glossary names the terms **and the operations**, each with the word the code uses; an
  operation's code word is decided by the people who own the domain, not by whoever translates it. A
  read is an operation too: the verb for looking at a read model (`ListEntries` or `ShowEntryList`) is
  named like any other, though no event carries it
- A domain word that can name more than one operation is decided by its effect: what exists before the
  step and after it, and whose state changes. *Create* brings a thing into existence, *add* puts an
  existing one into a collection; *delete* removes it, *cancel* and *archive* keep it with a state. The
  effect decides which aggregate holds the invariants
