---
type: Reference
title: "Anti-Corruption Layer: upstream contract types must stay inside the matching adapter — `CollectedViolations.addAll`"
tags: [reference]
evidence_for: "/rule/contextmap/dca-map-008.md#collectedviolationsaddall"
---

[Full node and context](/rule/contextmap/dca-map-008.md#collectedviolationsaddall). This is an evidence excerpt; retain the parent selection and caveats.

### `CollectedViolations.addAll`

```java
/**
   * Evaluates one ArchUnit rule and records each of its violation details, suffixed with the
   * explanation of what the rule was checking — the detail alone ({@code Class A depends on B})
   * does not say why that dependency is wrong.
   */
  void addAll(ArchRule rule, JavaClasses classes, String explanation) {
    for (String detail : rule.evaluate(classes).getFailureReport().getDetails()) {
      add(explanation.isEmpty() ? detail : detail + " - " + explanation);
    }
  }

/** Evaluates one ArchUnit rule and records its violation details as they are. */
  void addAll(ArchRule rule, JavaClasses classes) {
    addAll(rule, classes, "");
  }
```
