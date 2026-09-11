---
type: Section
title: "Comparison: When to Use Which Approach"
chapter: Domain Services with Data Dependencies
source: guide
resource: dca-guide/topics/domain-services-with-data-dependencies.md
tags: [guide, section]
---

| Criterion                        | Pure Domain Service     | DomainGateway              | Strategy/Callback          |
|----------------------------------|-------------------------|----------------------------|----------------------------|
| **Complexity of data query**     | Simple (1-2 sources)    | Medium to complex          | Simple (1 source)          |
| **Dependencies in the domain**   | None                    | Abstract interface         | None                       |
| **Testability**                  | Trivial                 | Mock the gateway           | Lambda inline              |
| **Readability**                  | Very good               | Good (explicit interface)  | Moderate (long signatures) |
| **Reusability**                  | High                    | High (interface shared)    | Low (per call)             |
| **Number of classes**            | Minimal                 | +2 (interface + impl)      | Optional +1 (func. interf.)|
| **Domain model explicitness**    | —                       | High (Ubiquitous Language) | Low                        |
| **Recommended when...**          | Data can be loaded up front | Domain decides what data it needs, several services share the same query | Single, simple query used by one service |

### Decision Tree

```
START: Domain Service needs data it does not have
   │
   ├─ Can the Application Service load all data up front?
   │     YES → Pure Domain Service (default)
   │     │
   │     NO ↓
   │
   ├─ Does the Domain Service decide dynamically which data it needs?
   │     YES → DomainGateway Pattern
   │     │
   │     NO ↓
   │
   ├─ Is it a single, simple data query?
   │     YES → Strategy/Callback Pattern
   │     │
   │     NO ↓
   │
   └─ Do several Domain Services need the same query?
         YES → DomainGateway Pattern (reusable interface)
         NO → Strategy/Callback Pattern (lightweight)
```

---

## Related mentions (heuristic)

- [DomainGateway](/marker/tactical/domaingateway.md)
