---
type: Reference
title: "GET handlers must not drive an input port that takes a command — `takesCommand`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-014.md#takescommand"
---

[Full node and context](/rule/hexagonal/dca-hex-014.md#takescommand). This is an evidence excerpt; retain the parent selection and caveats.

### `takesCommand`

```java
private static boolean takesCommand(JavaMethodCall call, DcaMarkers markers) {
  return call.getTarget().getRawParameterTypes().stream().anyMatch(markers.is("command"))
      || TypeInspection.takesInput(
          call.getTargetOwner(), markers.is("inputPort"), markers.is("command"));
}
```
