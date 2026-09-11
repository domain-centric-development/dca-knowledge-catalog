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

```mermaid
flowchart TD
    START(["A domain service needs data it does not have"]) --> Q1{"Can the use case load<br>all of it up front?"}
    Q1 -- yes --> PURE["<b>Pure domain service</b><br>the default: hand it the facts"]
    Q1 -- no --> Q2{"Does the domain service decide<br>while running which data it needs?"}
    Q2 -- yes --> GW["<b>DomainGateway</b>"]
    Q2 -- no --> Q3{"A single, simple query?"}
    Q3 -- no --> GW
    Q3 -- yes --> Q4{"Do several domain services<br>need that same query?"}
    Q4 -- yes --> GW2["<b>DomainGateway</b><br>one reusable interface"]
    Q4 -- no --> CB["<b>Strategy / callback</b><br>lightweight, one call site"]
```

---

## Related mentions (heuristic)

- [DomainGateway](/marker/tactical/domaingateway.md)
