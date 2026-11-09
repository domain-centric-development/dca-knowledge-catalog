---
type: Reference
title: "Domain services are used only by the application and by other domain services — `failIfAny`"
tags: [reference]
evidence_for: "/rule/advanced/dca-adv-021.md#failifany"
---

[Full node and context](/rule/advanced/dca-adv-021.md#failifany). This is an evidence excerpt; retain the parent selection and caveats.

### `failIfAny`

```java
private static void failIfAny(List<String> violations, String header) {
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(header, violations);
  }
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `inApplication()`, `inInfrastructure()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
