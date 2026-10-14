---
type: Reference
title: "Query use cases must not write or publish — `notWriteOrPublish`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-019.md#notwriteorpublish"
---

[Full node and context](/rule/usecase/dca-use-019.md#notwriteorpublish). This is an evidence excerpt; retain the parent selection and caveats.

### `notWriteOrPublish`

```java
private static ArchCondition<JavaClass> notWriteOrPublish(DcaMarkers markers) {
  return new ArchCondition<>("write nothing and publish nothing") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        for (var call : unit.getMethodCallsFromSelf()) {
          String effect = sideEffectOf(call.getTargetOwner(), call.getTarget(), markers);
          if (effect != null) {
            events.add(
                SimpleConditionEvent.violated(
                    item,
                    item.getName()
                        + "."
                        + unit.getName()
                        + " answers a query and "
                        + effect
                        + " ("
                        + call.getTargetOwner().getSimpleName()
                        + "."
                        + call.getName()
                        + ")"));
          }
        }
      }
    }
  };
}
```
