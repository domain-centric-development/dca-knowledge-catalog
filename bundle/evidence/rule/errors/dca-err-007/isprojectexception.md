---
type: Reference
title: "Diagnostic: failures that carry display data or objects instead of ids and figures — `isProjectException`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-007.md#isprojectexception"
---

[Full node and context](/rule/errors/dca-err-007.md#isprojectexception). This is an evidence excerpt; retain the parent selection and caveats.

### `isProjectException`

```java
/** A project's own exception type: assignable to a base type, outside the building blocks. */
  private static boolean isProjectException(JavaClass type, DcaMarkers markers) {
    return (markers.is("domainException").test(type) || markers.is("useCaseException").test(type))
        && !markers.declaresTypesIn(type.getPackageName());
  }
```
