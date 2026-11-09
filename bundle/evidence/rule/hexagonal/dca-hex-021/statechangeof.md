---
type: Reference
title: "Outgoing adapters must not call state-changing methods of aggregate roots — `stateChangeOf`"
tags: [reference]
evidence_for: "/rule/hexagonal/dca-hex-021.md#statechangeof"
---

[Full node and context](/rule/hexagonal/dca-hex-021.md#statechangeof). This is an evidence excerpt; retain the parent selection and caveats.

### `stateChangeOf`

```java
/**
   * How the called method changes the aggregate, worded for the violation, or {@code null} for a
   * query. A method of the vocabulary's own base - declared in the package of the aggregate-root
   * role's marker, such as the domain-event bookkeeping - is none. A method that cannot be resolved
   * is judged by its return type alone.
   */
  private static String stateChangeOf(JavaMethodCall call, String vocabulary) {
    java.util.Optional<JavaMethod> resolved = call.getTarget().resolveMember();
    if (resolved.isPresent()) {
      JavaMethod method = resolved.get();
      if (method.getModifiers().contains(JavaModifier.STATIC)
          || method.getOwner().getPackageName().equals(vocabulary)) {
        return null;
      }
      if (method.getRawReturnType().getName().equals("void")) {
        return "returns void and changes its state";
      }
      JavaClass root = call.getTargetOwner();
      for (JavaFieldAccess access : method.getFieldAccesses()) {
        if (access.getAccessType() == JavaFieldAccess.AccessType.SET
            && root.isAssignableTo(access.getTargetOwner().getName())) {
          return "sets the field " + access.getName();
        }
      }
      return null;
    }
    return call.getTarget().getRawReturnType().getName().equals("void")
        ? "returns void and changes its state"
        : null;
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `inOutgoingAdapter()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
