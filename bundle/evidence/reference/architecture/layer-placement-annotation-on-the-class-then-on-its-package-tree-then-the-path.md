---
type: Reference
title: "DcaArchitecture — Layer placement — annotation on the class, then on its package tree, then the path"
tags: [reference]
evidence_for: "/reference/architecture.md#layer-placement--annotation-on-the-class-then-on-its-package-tree-then-the-path"
---

[Full node and context](/reference/architecture.md#layer-placement--annotation-on-the-class-then-on-its-package-tree-then-the-path). This is an evidence excerpt; retain the parent selection and caveats.

### Layer placement — annotation on the class, then on its package tree, then the path

#### `Optional<Placement> placement(JavaClass javaClass)`

The layer a class sits in, or empty. A layer annotation the layout names on the class wins;
then one on the `package-info` of its package or the nearest package above it (a
declaration holds for its whole subtree); then the path below its module root. Without layer
annotations in the layout this is the path alone, exactly the packages the `all…Patterns`
name.

#### `String moduleRootOf(JavaClass javaClass)`

The module root a class belongs to — by its placement, else by its path; null for neither.

#### `DescribedPredicate<JavaClass> inLayer(DcaLayout.Layer layer)`

Classes the layout places in the given layer.

#### `DescribedPredicate<JavaClass> inLayerOf(DcaLayout.Layer layer, String moduleRoot)`

Classes the layout places in the given layer of the given module root.

#### `DescribedPredicate<JavaClass> inLayerSegment(DcaLayout.Layer layer, String segment)`

Classes in a sub-package of their layer's package — `...`.

#### `DescribedPredicate<JavaClass> inDomain()`

#### `DescribedPredicate<JavaClass> inDomainModel()`

The domain model: `...`.

#### `DescribedPredicate<JavaClass> inApplication()`

#### `DescribedPredicate<JavaClass> inSharedOutputPorts()`

The output ports shared by one context's use cases: `...`.

#### `DescribedPredicate<JavaClass> inIncomingAdapter()`

#### `DescribedPredicate<JavaClass> inOutgoingAdapter()`

#### `DescribedPredicate<JavaClass> inAdapter()`

Classes in either adapter layer, or below a module root's adapter package outside both — the
`.adapter..` the path rules have always meant.

#### `DescribedPredicate<JavaClass> inInfrastructure()`

#### `List<String> layerNotices()`

Findings about the layout's layer declarations: a package whose annotation names another layer
than its path, and a package that declares another layer than a package above it. Notices in
the report, not failures — a migration keeps path and annotation side by side.
