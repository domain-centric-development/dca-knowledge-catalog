---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types — `isEnumValueOf`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#isenumvalueof"
---

[Full node and context](/rule/tactical/dca-tac-025.md#isenumvalueof). This is an evidence excerpt; retain the parent selection and caveats.

### `isEnumValueOf`

```java
/**
   * The {@code valueOf(String)} the language declares on every enum - not a factory of the model.
   */
  private static boolean isEnumValueOf(JavaClass type, JavaMethod method) {
    return type.isEnum()
        && method.getName().equals("valueOf")
        && method.getRawParameterTypes().size() == 1
        && method.getRawParameterTypes().get(0).getName().equals("java.lang.String");
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()`, `classes()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
