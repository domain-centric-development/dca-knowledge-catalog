---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — `isEnumImplicit`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#isenumimplicit"
---

[Full node and context](/rule/tactical/dca-tac-025.md#isenumimplicit). This is an evidence excerpt; retain the parent selection and caveats.

### `isEnumImplicit`

```java
/** The {@code values()} and {@code valueOf(String)} the language declares on every enum. */
  private static boolean isEnumImplicit(JavaClass type, JavaMethod method) {
    return type.isEnum()
        && (isEnumValueOf(type, method)
            || (method.getName().equals("values") && method.getRawParameterTypes().isEmpty()));
  }
```
