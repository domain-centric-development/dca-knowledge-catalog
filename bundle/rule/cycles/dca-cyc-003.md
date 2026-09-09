---
type: Rule
id: DCA-CYC-003
title: Outgoing Adapter Packages must not have cyclic dependencies
rule: Outgoing adapters should have clear boundaries and no cycles.
constraint: Outgoing Adapter Packages must not have cyclic dependencies.
selects: "One slice per module root, holding the classes in <module>.adapter.outgoing.. of that module; everything else is ignored."
checks: The slices form no dependency cycle between modules' outgoing adapters. Cycles inside one module's outgoing adapters and dependencies into other layers do not count.
enforced_by: "CycleRules#DCA-CYC-003"
status: enforced
rule_set: cycles
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/CycleRules.java
tags: [cycles, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/CycleRules.cs
---

# Outgoing Adapter Packages must not have cyclic dependencies

## Selection

One slice per module root, holding the classes in <module>.adapter.outgoing.. of that module; everything else is ignored.

## Check

The slices form no dependency cycle between modules' outgoing adapters. Cycles inside one module's outgoing adapters and dependencies into other layers do not count.

## .NET reading

**Selection.** One slice per module root, holding the types in <module>.Adapter.Outgoing of that module and below; everything else is ignored.

**Check.** The slices form no dependency cycle between modules' outgoing adapters. Cycles inside one module's outgoing adapters and dependencies into other layers do not count.

## Implementation

```java
DcaRule.of(
        "DCA-CYC-003",
        "Outgoing Adapter Packages must not have cyclic dependencies",
        "Outgoing adapters should have clear boundaries and no cycles",
        arch ->
            slices()
                .assignedFrom(
                    moduleLayerSlices(
                        arch,
                        root ->
                            root
                                + "."
                                + layout.adapterSubpackage()
                                + "."
                                + layout.outgoingSubpackage()))
                .should()
                .beFreeOfCycles()
                .allowEmptyShould(true))
    .selecting(
        "One slice per module root, holding the classes in <module>.adapter.outgoing.. of"
            + " that module; everything else is ignored.")
    .checking(
        "The slices form no dependency cycle between modules' outgoing adapters. Cycles"
            + " inside"
            + " one module's outgoing adapters and dependencies into other layers do not"
            + " count.")
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
### C# expression

```csharp
DcaRule.Check(
    "DCA-CYC-003",
    "Outgoing Adapter Namespaces must not have cyclic dependencies",
    "Outgoing adapters should have clear boundaries and no cycles",
    arch => CheckSlices(arch, layout, $"{layout.AdapterSegment}.{layout.OutgoingSegment}", "Outgoing Adapter Namespaces must not have cyclic dependencies"))
    .Selecting(
        "One slice per module root, holding the types in <module>.Adapter.Outgoing of that module "
        + "and below; everything else is ignored.")
    .Checking(
        "The slices form no dependency cycle between modules' outgoing adapters. Cycles inside "
        + "one module's outgoing adapters and dependencies into other layers do not count.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
