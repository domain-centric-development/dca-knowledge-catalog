---
type: Reference
title: "Upstream declarations and the module declaration's allowed dependencies must agree — `CollectedViolations.check`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-006.md#collectedviolationscheck"
---

[Full node and context](/rule/contextmap/dca-map-006.md#collectedviolationscheck). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.check`

```java
/** Evaluates every rule, then throws all their violations at once. */
  static void check(List<ArchRule> rules, JavaClasses classes) {
    CollectedViolations collected = withoutHeader();
    rules.forEach(rule -> collected.addAll(rule, classes));
    collected.throwIfAny();
  }
```
