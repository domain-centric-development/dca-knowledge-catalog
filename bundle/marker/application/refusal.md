---
type: Marker
title: Refusal
category: application
kind: interface
signature: public interface Refusal
package: dev.domaincentric.dca.buildingblocks.application
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/application/Refusal.java
tags: [application, marker]
---

Marker for a case of a use-case result that refuses the request.

A use case may answer an expected refusal - the addressed thing does not exist, the caller may
not act on it, the model refused the input - in one of two styles, chosen per bounded context: it
throws a named failure, or it returns the refusal as a case of a closed result (a sealed type
whose cases its caller switches over). Both are equally valid; within one context the style is
uniform. This marker belongs to the second style: every case of a closed result that refuses the
request implements it, and a case that reports success never does.

**A refusal rolls back like a thrown failure.** A use case that wrote something before it
found out it has to refuse must not commit that write. A thrown failure rolls the transaction
back on its way out; a returned value would not, so the transaction boundary looks at the value
the work returns: when it is a `Refusal`, the boundary rolls back and hands the refusal to
the caller unchanged - see `TransactionBoundary`. An implementation of the platform's
declarative transactions does the same for a transactional use-case method that returns one. The
rule for good code stays "decide, then write" - check every refusal before the first write; the
roll-back is the net that catches a use case that does not.

**Shape.** A refusal case carries the ids and figures the refusal compared, never display
text; the incoming adapter turns it into its protocol's answer, exactly as it would translate the
thrown failure. The marker declares no method: it says what a case is, the case's own fields say
what happened.

```java
public sealed interface ReserveSeatResult {
  record Reserved(SeatId seat) implements ReserveSeatResult {}
  record SeatTaken(SeatId seat) implements ReserveSeatResult, Refusal {}
  record ShowNotFound(ShowId show) implements ReserveSeatResult, Refusal {}
}
```

A closed result describes the outcomes a use case can answer with; some are refusals, some are
not. One whose outcomes are all successes - found or nothing found, sent or already sent - is a
closed result all the same and carries no `Refusal`: marking such a case would roll back a
success. The marker means "the request was refused" whether or not a transaction is open - a
read-only use case refuses too; the roll-back only acts where something was written.

## Related mentions in guides (heuristic)

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Application Layer (Use Cases / Application Business Rules)](/guide/elements/application-layer-use-cases-application-business-rules.md)
- [Building blocks, as the library defines them](/guide/elements/building-blocks-as-the-library-defines-them.md)
- [Ports and Use Cases](/guide/language-mappings/ports-and-use-cases.md)
- [Structure Evolution Example: From Startup to Maturity](/guide/package-structure/structure-evolution-example-from-startup-to-maturity.md)
- [Checklist for new code](/guide/quick-reference/checklist-for-new-code.md)
- [ADAPTER LAYER RULES](/guide/rules/adapter-layer-rules.md)
- [ERROR HANDLING RULES](/guide/rules/error-handling-rules.md)
- [TRANSACTION RULES](/guide/rules/transaction-rules.md)
- [The use case once, each adapter its translation](/guide/testing-levels/the-use-case-once-each-adapter-its-translation.md)
