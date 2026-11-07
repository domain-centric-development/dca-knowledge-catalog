---
type: Reference
title: "The repository of an owned aggregate declares a lookup by the aggregate's id and the owner's id — `simpleName`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-026.md#simplename"
---

[Full node and context](/rule/tactical/dca-tac-026.md#simplename). This is an evidence excerpt; retain the parent selection and caveats.

### `simpleName`

```java
/** The simple name of a configured marker, for a message a reader has to recognise. */
  private static String simpleName(String fqn) {
    return fqn.substring(fqn.lastIndexOf('.') + 1);
  }
```
