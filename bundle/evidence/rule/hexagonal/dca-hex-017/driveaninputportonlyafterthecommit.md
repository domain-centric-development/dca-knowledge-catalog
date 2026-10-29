---
type: Reference
title: "Event listeners that drive an input port must run after the commit in their own transaction — `driveAnInputPortOnlyAfterTheCommit`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-017.md#driveaninputportonlyafterthecommit"
---

[Full node and context](/rule/hexagonal/dca-hex-017.md#driveaninputportonlyafterthecommit). This is an evidence excerpt; retain the parent selection and caveats.

### `driveAnInputPortOnlyAfterTheCommit`

```java
private static ArchCondition<JavaClass> driveAnInputPortOnlyAfterTheCommit(
    FrameworkAnnotations roles, DcaMarkers markers) {
  return new ArchCondition<>("drive an input port only after the commit") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      if (roles.eventListener().isEmpty() || roles.transactionalEventListener().isEmpty()) {
        return;
      }
      IntraClassCalls calls = null;
      for (JavaCodeUnit listener : item.getCodeUnits()) {
        if (AnnotationRoles.listenerEntry(listener, roles.eventListener()) == null) {
          continue;
        }
        if (calls == null) {
          calls = new IntraClassCalls(item);
        }
        java.util.Set<String> ports = new java.util.TreeSet<>();
        for (JavaCodeUnit unit : calls.reachableFrom(listener)) {
          for (JavaMethodCall call : unit.getMethodCallsFromSelf()) {
            JavaClass owner = call.getTargetOwner();
            if (markers.is("inputPort").test(owner)) {
              ports.add(owner.getSimpleName() + "." + call.getName());
            }
          }
        }
        if (ports.isEmpty()) {
          continue;
        }
        boolean afterCommit =
            AnnotationRoles.listenerEntry(listener, roles.transactionalEventListener()) != null;
        boolean ownTransaction =
            AnnotationRoles.isMetaAnnotatedWithAny(listener, roles.transactional())
                || AnnotationRoles.isMetaAnnotatedWithAny(item, roles.transactional());
        if (!afterCommit || !ownTransaction) {
          events.add(
              SimpleConditionEvent.violated(
                  item,
                  item.getName()
                      + "."
                      + listener.getName()
                      + " drives "
                      + String.join(", ", ports)
                      + (afterCommit
                          ? " after the commit without a transaction of its own"
                          : " outside the phase after a successful commit - inside the"
                              + " transaction that raised the event, or whatever its outcome")));
        }
      }
    }
  };
}
```
