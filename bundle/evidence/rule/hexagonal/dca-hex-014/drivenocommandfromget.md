---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `driveNoCommandFromGet`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#drivenocommandfromget"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#drivenocommandfromget). This is an evidence excerpt; retain the parent selection and caveats.

### `driveNoCommandFromGet`

```java
private static ArchCondition<JavaClass> driveNoCommandFromGet(
    List<String> getMapping, DcaMarkers markers) {
  return new ArchCondition<>("drive no command from a GET handler") {
    @Override
    public void check(JavaClass item, ConditionEvents events) {
      IntraClassCalls calls = new IntraClassCalls(item);
      for (JavaCodeUnit handler : item.getCodeUnits()) {
        String mapping = AnnotationRoles.matchingEntry(handler, getMapping);
        if (mapping == null) {
          continue;
        }
        java.util.Set<String> commands = new java.util.TreeSet<>();
        for (JavaCodeUnit unit : calls.reachableFrom(handler)) {
          for (JavaMethodCall call : unit.getMethodCallsFromSelf()) {
            JavaClass owner = call.getTargetOwner();
            if (markers.is("inputPort").test(owner) && takesCommand(call, markers)) {
              commands.add(owner.getSimpleName() + "." + call.getName());
            }
          }
        }
        if (!commands.isEmpty()) {
          events.add(
              SimpleConditionEvent.violated(
                  item,
                  item.getName()
                      + "."
                      + handler.getName()
                      + " handles "
                      + FrameworkAnnotations.describe(mapping)
                      + " and drives a command through "
                      + String.join(", ", commands)));
        }
      }
    }
  };
}
```
