---
type: Reference
title: "Use cases that save an aggregate or publish domain events must have a transaction boundary — `beTransactionalWhenMutating`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#betransactionalwhenmutating"
---

[Full node and context](/rule/usecase/dca-use-012.md#betransactionalwhenmutating). This is an evidence excerpt; retain the parent selection and caveats.

### `beTransactionalWhenMutating`

```java
private static ArchCondition<JavaClass> beTransactionalWhenMutating(
    List<String> transactional) {
  return new ArchCondition<>("be transactional when saving an aggregate or publishing domain events") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        String effect = transactionalEffectOf(unit);
        if (effect == null) {
          continue;
        }
        for (JavaCodeUnit entry : calls.entryPointsOf(unit)) {
          if (pathIsTransactional(item, entry, unit, calls, transactional)) {
            continue;
          }
          events.add(
              SimpleConditionEvent.violated(
                  item,
                  item.getSimpleName()
                      + "."
                      + pathName(entry, unit)
                      + " "
                      + effect
                      + " without "
                      + FrameworkAnnotations.describe(
                          transactional, "declarative transaction metadata (none configured)")
                      + " on the class or on a method of that path, and without"
                      + " TransactionBoundary.inTransaction(...) on it"));
        }
      }
    }
  };
}
```
