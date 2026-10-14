---
type: Reference
title: "In a module grouped by feature, incoming adapters must drive the commands of one feature only — `checkOneFeaturePerAdapter`"
tags: [reference]
evidence_for: "/rule/usecase/dca-use-018.md#checkonefeatureperadapter"
---

[Full node and context](/rule/usecase/dca-use-018.md#checkonefeatureperadapter). This is an evidence excerpt; retain the parent selection and caveats.

### `checkOneFeaturePerAdapter`

```java
private static void checkOneFeaturePerAdapter(DcaArchitecture arch, DcaLayout layout) {
  List<String> violations = new ArrayList<>();
  for (String root : arch.moduleRoots()) {
    String application = root + "." + layout.applicationSubpackage();
    String shared = application + "." + layout.sharedSubpackage();
    String incoming = root + "." + layout.adapterSubpackage() + "." + layout.incomingSubpackage();
    if (!isGroupedByFeature(arch, layout, application, shared)) {
      continue;
    }
    for (JavaClass adapter : arch.classes()) {
      if (adapter.isInterface()
          || !DcaArchitecture.inPackageTree(adapter.getPackageName(), incoming)) {
        continue;
      }
      Map<String, TreeSet<String>> portsByFeature = new TreeMap<>();
      for (var dependency : adapter.getDirectDependenciesFromSelf()) {
        JavaClass target = dependency.getTargetClass();
        String pkg = target.getPackageName();
        if (!target.isAssignableTo(layout.markers().inputPort())
            || !TypeInspection.takesInputEndingWith(
                target, layout.markers().inputPort(), "Command")
            || !DcaArchitecture.inPackageTree(pkg, application)
            || DcaArchitecture.inPackageTree(pkg, shared)) {
          continue;
        }
        List<String> segments = useCaseSegments(pkg, application, layout);
        if (segments.size() < 2) {
          continue;
        }
        portsByFeature
            .computeIfAbsent(segments.get(0), feature -> new TreeSet<>())
            .add(target.getSimpleName());
      }
      if (portsByFeature.size() > 1) {
        violations.add(
            adapter.getName()
                + " drives the commands of "
                + portsByFeature.size()
                + " features "
                + portsByFeature
                + " - cut it along the features");
      }
    }
  }
  if (!violations.isEmpty()) {
    throw new DcaRuleViolation(
        "In a module grouped by feature, incoming adapters must drive the commands of one"
            + " feature only",
        violations);
  }
}
```
