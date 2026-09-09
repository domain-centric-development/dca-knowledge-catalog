---
type: Reference
title: "Use cases that publish domain events must have a transaction boundary — `beTransactionalWhenPublishing`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-012.md#betransactionalwhenpublishing"
---

[Full node and context](/rule/usecase/dca-use-012.md#betransactionalwhenpublishing). This is an evidence excerpt; retain the parent selection and caveats.

### `beTransactionalWhenPublishing`

```java
private static ArchCondition<JavaClass> beTransactionalWhenPublishing(
    List<String> transactional) {
  return new ArchCondition<>("be transactional when publishing domain events") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        if (!calls(unit, DomainEventPublisher.class)) {
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
                      + " publishes domain events without "
                      + FrameworkAnnotations.describe(
                          transactional, "declarative transaction metadata (none configured)")
                      + " on the class or on a method of that path, and without"
                      + " TransactionBoundary.inTransaction(...) on it - after-commit"
                      + " listeners are skipped"));
        }
      }
    }
  };
}
```
