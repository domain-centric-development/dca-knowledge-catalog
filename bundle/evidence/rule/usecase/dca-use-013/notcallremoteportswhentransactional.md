---
type: Reference
title: "Declaratively transactional use cases must not call remote-capable output ports — `notCallRemotePortsWhenTransactional`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-013.md#notcallremoteportswhentransactional"
---

[Full node and context](/rule/usecase/dca-use-013.md#notcallremoteportswhentransactional). This is an evidence excerpt; retain the parent selection and caveats.

### `notCallRemotePortsWhenTransactional`

```java
private static ArchCondition<JavaClass> notCallRemotePortsWhenTransactional(
    List<String> transactional, DcaMarkers markers) {
  return new ArchCondition<>("not call remote-capable output ports while transactional") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit unit : item.getCodeUnits()) {
        if (!isTransactional(item, unit, calls, transactional)) {
          continue;
        }
        List<String> remotePorts =
            unit.getMethodCallsFromSelf().stream()
                .map(call -> call.getTargetOwner())
                .filter(owner -> owner.isAssignableTo(markers.outputPort()))
                .filter(owner -> !isTransactionalResource(owner, markers))
                .map(JavaClass::getSimpleName)
                .distinct()
                .sorted()
                .toList();
        if (!remotePorts.isEmpty()) {
          events.add(
              SimpleConditionEvent.violated(
                  item,
                  item.getSimpleName()
                      + "."
                      + unit.getName()
                      + " runs under "
                      + FrameworkAnnotations.describe(transactional, "a transaction annotation")
                      + " and calls "
                      + String.join(", ", remotePorts)
                      + " inside the transaction - call it before, or draw the boundary with"
                      + " TransactionBoundary.inTransaction(...)"));
        }
      }
    }
  };
}
```
