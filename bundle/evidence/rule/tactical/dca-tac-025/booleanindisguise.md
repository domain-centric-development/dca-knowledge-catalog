---
type: Reference
title: "Domain types must not hold bare primitives, strings or time types; a boolean only as a field or a predicate — `booleanInDisguise`"
tags: [reference]
evidence_for: "/rule/tactical/dca-tac-025.md#booleanindisguise"
---

[Full node and context](/rule/tactical/dca-tac-025.md#booleanindisguise). This is an evidence excerpt; retain the parent selection and caveats.

### `booleanInDisguise`

```java
/**
   * The finding for an enum of exactly two constants that name one fact and its negation - a
   * boolean in disguise - or {@code null}.
   */
  private static String booleanInDisguise(JavaClass type) {
    if (!type.isEnum() || type.getEnumConstants().size() != 2) {
      return null;
    }
    List<String> names =
        type.getEnumConstants().stream().map(constant -> constant.name()).sorted().toList();
    String first = normalisedConstant(names.get(0));
    String second = normalisedConstant(names.get(1));
    boolean pair =
        NEGATION_PAIRS.contains(Set.of(first, second))
            || negates(first, second)
            || negates(second, first);
    return pair
        ? "enum with the constants "
            + names.get(0)
            + " and "
            + names.get(1)
            + " names one fact and its negation - a boolean in disguise"
        : null;
  }
```
