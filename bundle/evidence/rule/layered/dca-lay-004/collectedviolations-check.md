---
type: Reference
title: "Transaction boundaries belong to the application layer — `CollectedViolations.check`"
tags: [reference]
evidence_for: "/rule/layered/dca-lay-004.md#collectedviolationscheck"
---

[Full node and context](/rule/layered/dca-lay-004.md#collectedviolationscheck). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.check`

```java
/** Evaluates every rule, then throws all their violations at once. */
  static void check(List<ArchRule> rules, JavaClasses classes) {
    CollectedViolations collected = withoutHeader();
    rules.forEach(rule -> collected.addAll(rule, classes));
    collected.throwIfAny();
  }
```
