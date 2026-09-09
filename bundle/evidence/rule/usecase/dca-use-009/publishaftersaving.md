---
type: Reference
title: "Use cases that save an aggregate must publish its domain events — `publishAfterSaving`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-009.md#publishaftersaving"
---

[Full node and context](/rule/usecase/dca-use-009.md#publishaftersaving). This is an evidence excerpt; retain the parent selection and caveats.

### `publishAfterSaving`

```java
private static ArchCondition<JavaClass> publishAfterSaving(DcaArchitecture arch) {
  return new ArchCondition<>("publish the aggregate's domain events after saving it") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        if (unit.getMethodCallsFromSelf().stream()
            .filter(
                c ->
                    c.getTarget().getName().equals("save")
                        && c.getTargetOwner().isAssignableTo(Repository.class))
            .allMatch(c -> EventFreeAggregate.repository(c.getTargetOwner(), arch))) {
          continue;
        }
        for (JavaCodeUnit entry : calls.entryPointsOf(unit)) {
          boolean publishes =
              calls.reachableFrom(entry).stream()
                  .anyMatch(u -> calls(u, DomainEventPublisher.class, "publishAndClearEvents"));
          if (!publishes) {
            events.add(
                SimpleConditionEvent.violated(
                    item,
                    item.getSimpleName()
                        + "."
                        + pathName(entry, unit)
                        + " saves an aggregate without publishing its domain events - no"
                        + " method reached from there calls publishAndClearEvents"));
          }
        }
      }
    }
  };
}
```
