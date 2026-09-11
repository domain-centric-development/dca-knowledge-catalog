---
type: Section
title: Principle
chapter: "Language Mappings: Java/Spring ↔ C#/.NET"
source: guide
resource: dca-guide/topics/language-mappings.md
tags: [guide, section]
---

The architecture is language-neutral; its *spelling* is not. A DCA code base in C# reads as C#:
interfaces carry the `I` prefix, asynchronous ports end in `Async`, attributes replace package
annotations, projects replace packages as the physical module boundary. Everything that matters
to the architecture stays: the four layers and their dependency direction, one folder per use case,
ports defined inside and implemented outside, a bounded context that is a deep module, and the
same rule ids (`DCA-TAC-001`, `DCA-USE-009`, …) checked by the same catalog.

Rule of thumb: **roles, folders and rule ids are shared; names follow the host language.**
