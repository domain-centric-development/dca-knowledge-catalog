---
type: Reference
title: "Query use cases must not write or publish — `takingAQuery`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-019.md#takingaquery"
---

[Full node and context](/rule/usecase/dca-use-019.md#takingaquery). This is an evidence excerpt; retain the parent selection and caveats.

### `takingAQuery`

```java
private static DescribedPredicate<JavaClass> takingAQuery(DcaLayout layout) {
  return DescribedPredicate.describe(
      "take an input ending with Query",
      type -> TypeInspection.takesInputEndingWith(type, layout.markers().inputPort(), "Query"));
}
```
