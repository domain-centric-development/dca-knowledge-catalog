---
type: ADR
title: "ADR-020: Use Case Output Naming Convention (*Result instead of *Response)"
adr: 20
status: accepted
pattern: "Use `*Result` suffix for all use case output classes in the application layer."
resource: ai-architecture-sample/docs/architecture/adr/adr-020-use-case-result-naming.md
tags: [adr, naming, use-case]
---

Use `*Result` suffix for all use case output classes in the application layer.

**Consequences:** Clearer layer boundaries · Reduced confusion · Better semantic fit · Consistent naming · Future-proof · Breaking change · Differs from some examples

## Applies to markers

- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
