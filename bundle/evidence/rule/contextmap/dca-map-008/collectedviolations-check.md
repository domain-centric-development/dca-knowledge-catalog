---
type: Reference
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter — `CollectedViolations.check`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-008.md#collectedviolationscheck"
---

[Full node and context](/rule/contextmap/dca-map-008.md#collectedviolationscheck). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.check`

```java
/** Evaluates every rule, then throws all their violations at once. */
  static void check(List<ArchRule> rules, JavaClasses classes) {
    CollectedViolations collected = withoutHeader();
    rules.forEach(rule -> collected.addAll(rule, classes));
    collected.throwIfAny();
  }
```
