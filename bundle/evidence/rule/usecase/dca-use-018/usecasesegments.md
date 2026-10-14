---
type: Reference
title: "In a module grouped by feature, incoming adapters must drive the commands of one feature only — `useCaseSegments`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-018.md#usecasesegments"
---

[Full node and context](/rule/usecase/dca-use-018.md#usecasesegments). This is an evidence excerpt; retain the parent selection and caveats.

### `useCaseSegments`

```java
/**
   * The segments of a package below the module's application package, configured operation
   * containers removed: {@code [placeorder]} for a flat use case package, {@code [ordering,
   * placeorder]} for a grouped one, empty for the application package itself.
   */
  private static List<String> useCaseSegments(String pkg, String application, DcaLayout layout) {
    if (pkg.equals(application)) {
      return List.of();
    }
    return java.util.Arrays.stream(pkg.substring(application.length() + 1).split("\\."))
        .filter(segment -> !layout.operationContainers().contains(segment))
        .toList();
  }
```
