---
type: Reference
title: "Diagnostic: incoming adapter packages that drive a use case without translating its failures — `casesOfClosedResults`"
tags: [reference]
evidence_for: "/rule/errors/dca-err-006.md#casesofclosedresults"
---

[Full node and context](/rule/errors/dca-err-006.md#casesofclosedresults). This is an evidence excerpt; retain the parent selection and caveats.

### `casesOfClosedResults`

```java
/**
   * The names of the cases of every closed result an input port answers with: a sealed type a
   * port's method returns or its use-case interface binds as a type argument, and that type's
   * permitted subclasses, recursively through sealed cases.
   */
  private static Set<String> casesOfClosedResults(DcaArchitecture arch) {
    DescribedPredicate<JavaClass> inputPort = arch.layout().markers().is("inputPort");
    Set<String> cases = new HashSet<>();
    for (JavaClass port : arch.classes()) {
      if (!port.isInterface() || !inputPort.test(port)) {
        continue;
      }
      for (JavaClass output : TypeInspection.outputTypes(port, inputPort)) {
        if (output.isSealed()) {
          collectCases(output, cases);
        }
      }
    }
    return cases;
  }
```
