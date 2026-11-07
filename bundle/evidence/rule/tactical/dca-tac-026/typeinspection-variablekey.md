---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — `TypeInspection.variableKey`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#typeinspectionvariablekey"
---

[Full node and context](/rule/tactical/dca-tac-026.md#typeinspectionvariablekey). This is an evidence excerpt; retain the parent selection and caveats.

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

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `layout()`, `rootContextPackage()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
