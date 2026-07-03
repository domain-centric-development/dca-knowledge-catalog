---
type: Process
title: How to write an ADR
resource: implementing-domain-centric-architecture/adr-template.md
tags: [adr, process, governance]
---

How to record an architectural decision in this project, so a new application keeps the same decision log format (Michael Nygard style).

## Steps

1. Copy the ADR template and number it sequentially: `adr-XXX-short-title.md` (next available number).
2. Use a descriptive title that states *what* is being decided.
3. Fill in every section (below) — brief is fine, but each adds context.
4. Set `Status` (Proposed → Accepted → Deprecated/Superseded by ADR-YYY). Never delete a superseded ADR; mark it and link the replacement.
5. Update the ADR index/README and get it reviewed.
6. Where the decision is machine-enforceable, add or reference an ArchUnit rule and link it from the ADR.

## Section skeleton

- **Context**
- **Decision**
- **Rationale**
- **Consequences**
- **Alternatives Considered**
- **Related Decisions**
- **Implementation Notes**
- **Review Date**
- **References**

## When to write an ADR

Significant, hard-to-reverse decisions; choices between viable alternatives; patterns used across the codebase. Skip trivial or easily reversible details.
