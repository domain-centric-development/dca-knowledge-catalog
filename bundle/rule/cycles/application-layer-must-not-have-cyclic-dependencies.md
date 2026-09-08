---
type: Rule
id: DCA-CYC-002
title: Application Layer must not have cyclic dependencies
rule: Application services should have clear boundaries and no cycles.
constraint: Application Layer must not have cyclic dependencies.
selects: "One slice per module root, holding the classes in <module>.application.. of that module (application.shared included); classes outside every module or outside the application layer are ignored."
checks: "The slices form no dependency cycle between modules' application layers. Cycles between use cases or features inside one module do not count here (see DCA-CYC-005), nor do dependencies into domain or adapter classes."
enforced_by: "CycleRules#DCA-CYC-002"
status: enforced
rule_set: cycles
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/CycleRules.java
tags: [cycles, archunit]
---

## Selection

One slice per module root, holding the classes in <module>.application.. of that module (application.shared included); classes outside every module or outside the application layer are ignored.

## Check

The slices form no dependency cycle between modules' application layers. Cycles between use cases or features inside one module do not count here (see DCA-CYC-005), nor do dependencies into domain or adapter classes.

## .NET reading

**Selection.** One slice per module root, holding the types in <module>.Application of that module and below (Application.Shared included); types outside every module or outside the application layer are ignored.

**Check.** The slices form no dependency cycle between modules' application layers. Cycles between use cases or features inside one module do not count here (see DCA-CYC-005), nor do dependencies into domain or adapter types.

## Implementation

```java
DcaRule.of(
        "DCA-CYC-002",
        "Application Layer must not have cyclic dependencies",
        "Application services should have clear boundaries and no cycles",
        arch ->
            slices()
                .assignedFrom(
                    moduleLayerSlices(
                        arch, root -> root + "." + layout.applicationSubpackage()))
                .should()
                .beFreeOfCycles()
                .allowEmptyShould(true))
    .selecting(
        "One slice per module root, holding the classes in <module>.application.. of that"
            + " module (application.shared included); classes outside every module or outside"
            + " the application layer are ignored.")
    .checking(
        "The slices form no dependency cycle between modules' application layers. Cycles"
            + " between use cases or features inside one module do not count here (see"
            + " DCA-CYC-005), nor do dependencies into domain or adapter classes.")
```

## Helpers

### `moduleLayerSlices`

```java
/**
   * One slice per module, holding that module's classes in the layer {@code layerOf} names.
   *
   * <p>Replaces {@code slices().matching(base + ".(*)." + layer + "..")}. A slice pattern needs a
   * capture group to derive the slice identity, and {@code (*)} is exactly one segment — so the
   * matching form only ever sliced modules that were direct children of the base package, and a
   * grouped or nested one was silently excluded from the cycle check. Assigning slices explicitly
   * uses {@link DcaArchitecture#moduleRootOf(String)} and therefore holds at any depth.
   */
  private static SliceAssignment moduleLayerSlices(
      DcaArchitecture arch, UnaryOperator<String> layerOf) {
    return new SliceAssignment() {

      @Override
      public SliceIdentifier getIdentifierOf(JavaClass javaClass) {
        String root = arch.moduleRootOf(javaClass.getPackageName());
        if (root == null) {
          return SliceIdentifier.ignore();
        }
        String layer = layerOf.apply(root);
        String pkg = javaClass.getPackageName();
        return pkg.equals(layer) || pkg.startsWith(layer + ".")
            ? SliceIdentifier.of(root)
            : SliceIdentifier.ignore();
      }

      @Override
      public String getDescription() {
        return "modules";
      }
    };
  }
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `moduleRootOf()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
