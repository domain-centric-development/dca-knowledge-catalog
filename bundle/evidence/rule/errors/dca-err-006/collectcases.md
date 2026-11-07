---
type: Reference
title: "Diagnostic: incoming adapter packages that drive a use case without translating its failures — `collectCases`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-006.md#collectcases"
---

[Full node and context](/rule/errors/dca-err-006.md#collectcases). This is an evidence excerpt; retain the parent selection and caveats.

### `collectCases`

```java
private static void collectCases(JavaClass sealed, Set<String> cases) {
  for (JavaClass permitted : sealed.getPermittedSubclasses().orElse(Set.of())) {
    if (cases.add(permitted.getName()) && permitted.isSealed()) {
      collectCases(permitted, cases);
    }
  }
}
```
