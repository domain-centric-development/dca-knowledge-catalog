---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `AnnotationRoles.holds`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#annotationrolesholds"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#annotationrolesholds). This is an evidence excerpt; retain the parent selection and caveats.

### `AnnotationRoles.holds`

```java
private static boolean holds(Object attributeValue, String value) {
  if (attributeValue instanceof Object[] values) {
    for (Object each : values) {
      if (holds(each, value)) {
        return true;
      }
    }
    return false;
  }
  String actual =
      attributeValue instanceof JavaEnumConstant constant
          ? constant.name()
          : String.valueOf(attributeValue);
  return actual.equalsIgnoreCase(value);
}
```
