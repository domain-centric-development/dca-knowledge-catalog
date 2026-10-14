---
type: Reference
title: "In a module grouped by feature, incoming adapters must drive the commands of one feature only — `isGroupedByFeature`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-018.md#isgroupedbyfeature"
---

[Full node and context](/rule/usecase/dca-use-018.md#isgroupedbyfeature). This is an evidence excerpt; retain the parent selection and caveats.

### `isGroupedByFeature`

```java
/** Whether an input port or use case of the module sits at application.<feature>.<usecase>. */
  private static boolean isGroupedByFeature(
      DcaArchitecture arch, DcaLayout layout, String application, String shared) {
    for (JavaClass candidate : arch.classes()) {
      String pkg = candidate.getPackageName();
      if (!DcaArchitecture.inPackageTree(pkg, application)
          || DcaArchitecture.inPackageTree(pkg, shared)
          || candidate.isNestedClass()
          || !(candidate.isAssignableTo(layout.markers().inputPort())
              || candidate.getSimpleName().endsWith(layout.useCaseSuffix()))) {
        continue;
      }
      if (useCaseSegments(pkg, application, layout).size() == 2) {
        return true;
      }
    }
    return false;
  }
```
