---
type: Reference
title: "Diagnostic: closed use-case results without a case marked as a refusal — `closedResultsOf`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-008.md#closedresultsof"
---

[Full node and context](/rule/errors/dca-err-008.md#closedresultsof). This is an evidence excerpt; retain the parent selection and caveats.

### `closedResultsOf`

```java
/**
   * Every closed result an input port answers with, mapped to the ports that answer with it: a
   * sealed type a port's public method returns or its use-case interface binds as a type argument,
   * commands and queries excluded.
   */
  private static Map<JavaClass, Set<JavaClass>> closedResultsOf(DcaArchitecture arch) {
    DcaMarkers markers = arch.layout().markers();
    DescribedPredicate<JavaClass> inputPort = markers.is("inputPort");
    Map<JavaClass, Set<JavaClass>> results =
        new TreeMap<>(java.util.Comparator.comparing(JavaClass::getName));
    for (JavaClass port : arch.classes()) {
      if (!port.isInterface() || !inputPort.test(port)) {
        continue;
      }
      for (JavaClass output : TypeInspection.outputTypes(port, inputPort)) {
        if (output.isSealed()
            && !markers.is("command").test(output)
            && !markers.is("query").test(output)) {
          results.computeIfAbsent(output, key -> new LinkedHashSet<>()).add(port);
        }
      }
    }
    return results;
  }
```
