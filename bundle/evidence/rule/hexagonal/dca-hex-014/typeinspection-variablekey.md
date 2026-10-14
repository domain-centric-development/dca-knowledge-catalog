---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `TypeInspection.variableKey`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#typeinspectionvariablekey"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#typeinspectionvariablekey). This is an evidence excerpt; retain the parent selection and caveats.

### `TypeInspection.variableKey`

```java
/** A type variable is identified by its owner and name; {@code T} of two classes differ. */
  private static String variableKey(JavaTypeVariable<?> variable) {
    Object owner = variable.getOwner();
    String ownerName =
        owner instanceof JavaClass javaClass
            ? javaClass.getName()
            : owner instanceof JavaMethod method ? method.getFullName() : String.valueOf(owner);
    return ownerName + "#" + variable.getName();
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
