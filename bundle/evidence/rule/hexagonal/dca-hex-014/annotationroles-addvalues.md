---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `AnnotationRoles.addValues`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#annotationrolesaddvalues"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#annotationrolesaddvalues). This is an evidence excerpt; retain the parent selection and caveats.

### `AnnotationRoles.addValues`

```java
private static void addValues(Object attributeValue, Set<String> values) {
  if (attributeValue instanceof Object[] array) {
    for (Object each : array) {
      addValues(each, values);
    }
    return;
  }
  values.add(
      attributeValue instanceof JavaEnumConstant constant
          ? constant.name()
          : String.valueOf(attributeValue));
}
```
