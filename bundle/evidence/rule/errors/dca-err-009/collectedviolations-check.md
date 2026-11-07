---
type: Reference
title: "A domain exception is constructed only in the domain layer — `CollectedViolations.check`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-009.md#collectedviolationscheck"
---

[Full node and context](/rule/errors/dca-err-009.md#collectedviolationscheck). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.check`

```java
/** Evaluates every rule, then throws all their violations at once. */
  static void check(List<ArchRule> rules, JavaClasses classes) {
    CollectedViolations collected = withoutHeader();
    rules.forEach(rule -> collected.addAll(rule, classes));
    collected.throwIfAny();
  }
```
