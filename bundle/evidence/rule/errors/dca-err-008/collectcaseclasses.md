---
type: Reference
title: "Diagnostic: closed use-case results without a case marked as a refusal — `collectCaseClasses`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-008.md#collectcaseclasses"
---

[Full node and context](/rule/errors/dca-err-008.md#collectcaseclasses). This is an evidence excerpt; retain the parent selection and caveats.

### `collectCaseClasses`

```java
private static void collectCaseClasses(JavaClass sealed, Set<JavaClass> cases) {
  for (JavaClass permitted : sealed.getPermittedSubclasses().orElse(Set.of())) {
    if (cases.add(permitted) && permitted.isSealed()) {
      collectCaseClasses(permitted, cases);
    }
  }
}
```
