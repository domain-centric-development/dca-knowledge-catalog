---
type: Reference
title: "Diagnostic: failures that carry display data or objects instead of ids and figures — `fieldFinding`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-007.md#fieldfinding"
---

[Full node and context](/rule/errors/dca-err-007.md#fieldfinding). This is an evidence excerpt; retain the parent selection and caveats.

### `fieldFinding`

```java
/** What is wrong with a type a failure's field involves, or {@code null} when it is fine. */
  private static String fieldFinding(JavaClass type, DcaArchitecture arch) {
    DcaMarkers markers = arch.layout().markers();
    String name = type.getName();
    if (markers.is("aggregateRoot").test(type) || markers.is("entity").test(type)) {
      return "an aggregate or entity";
    }
    if (type.isAssignableTo(CharSequence.class)) {
      return "a plain string";
    }
    if (type.isPrimitive()
        || type.isEnum()
        || type.isAssignableTo(Number.class)
        || markers.is("id").test(type)
        || markers.is("value").test(type)
        || name.equals("java.lang.Boolean")
        || name.equals("java.lang.Character")
        || type.getPackageName().equals("java.time")
        || arch.layout().timestampTypes().contains(name)
        || type.getPackageName().equals("java.util")
        || name.equals("java.lang.Object")) {
      return null;
    }
    return "neither an id, a value nor a number";
  }
```
