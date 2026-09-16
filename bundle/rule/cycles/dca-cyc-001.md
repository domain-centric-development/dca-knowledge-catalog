---
type: Rule
id: DCA-CYC-001
title: "Domain Packages must not have cyclic dependencies (package-based slice discovery)"
rule: "Domain model packages should have clear boundaries and no cycles (Acyclic Dependencies Principle)."
constraint: "Domain Packages must not have cyclic dependencies (package-based slice discovery)."
selects: "One slice per module root, holding the classes in <module>.domain.model.. of that module (segment names from the layout). A module root is the shortest package prefix whose next segment is a layer segment, so modules are found at any depth; classes outside every module or outside the domain-model package are ignored."
checks: "The slices form no dependency cycle - no two modules' domain models depend on each other, directly or via further modules' domain models. Slices are per module root, so a cycle between classes inside one module's domain model is not detected here, and dependencies into other layers do not count. DCA-CYC-005 covers the application layer per operation; no rule slices the domain model within a module. Fewer than two slices pass."
enforced_by: "CycleRules#DCA-CYC-001"
status: enforced
rule_set: cycles
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/CycleRules.java
tags: [cycles, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/CycleRules.cs
---

# Domain Packages must not have cyclic dependencies (package-based slice discovery)

## Selection

One slice per module root, holding the classes in <module>.domain.model.. of that module (segment names from the layout). A module root is the shortest package prefix whose next segment is a layer segment, so modules are found at any depth; classes outside every module or outside the domain-model package are ignored.

## Check

The slices form no dependency cycle - no two modules' domain models depend on each other, directly or via further modules' domain models. Slices are per module root, so a cycle between classes inside one module's domain model is not detected here, and dependencies into other layers do not count. DCA-CYC-005 covers the application layer per operation; no rule slices the domain model within a module. Fewer than two slices pass.

## .NET reading

**Selection.** One slice per module root, holding the types in <module>.Domain.Model of that module and below (segment names from the layout). A module root is the shortest namespace prefix whose next segment is a layer segment, so modules are found at any depth; types outside every module or outside the domain-model namespace are ignored.

**Check.** The slices form no dependency cycle - no two modules' domain models depend on each other, directly or via further modules' domain models. Slices are per module root, so a cycle between types inside one module's domain model is not detected here, and dependencies into other layers do not count. DCA-CYC-005 covers the application layer per operation; no rule slices the domain model within a module. Fewer than two slices pass.

## Implementation

```java
DcaRule.of(
        "DCA-CYC-001",
        "Domain Packages must not have cyclic dependencies (package-based slice discovery)",
        "Domain model packages should have clear boundaries and no cycles (Acyclic Dependencies"
            + " Principle)",
        arch ->
            slices()
                .assignedFrom(moduleLayerSlices(arch, layout::domainModelPackage))
                .should()
                .beFreeOfCycles()
                .allowEmptyShould(true))
    .selecting(
        "One slice per module root, holding the classes in <module>.domain.model.. of that"
            + " module (segment names from the layout). A module root is the shortest package"
            + " prefix whose next segment is a layer segment, so modules are found at any depth;"
            + " classes outside every module or outside the domain-model package are ignored.")
    .checking(
        "The slices form no dependency cycle - no two modules' domain models depend on each"
            + " other, directly or via further modules' domain models. Slices are per module"
            + " root, so a cycle between classes inside one module's domain model is not"
            + " detected here, and dependencies into other layers do not count. DCA-CYC-005"
            + " covers the application layer per operation; no rule slices the domain model"
            + " within a module. Fewer than two slices pass.")
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
    "DCA-CYC-001",
    "Domain Namespaces must not have cyclic dependencies (package-based slice discovery)",
    "Domain model namespaces should have clear boundaries and no cycles (Acyclic Dependencies Principle)",
    arch => CheckSlices(arch, layout, $"{layout.DomainSegment}.{layout.ModelSegment}", "Domain Namespaces must not have cyclic dependencies"))
    .Selecting(
        "One slice per module root, holding the types in <module>.Domain.Model of that module and "
        + "below (segment names from the layout). A module root is the shortest namespace prefix "
        + "whose next segment is a layer segment, so modules are found at any depth; types outside "
        + "every module or outside the domain-model namespace are ignored.")
    .Checking(
        "The slices form no dependency cycle - no two modules' domain models depend on each "
        + "other, directly or via further modules' domain models. Slices are per module root, so a "
        + "cycle between types inside one module's domain model is not detected here, and "
        + "dependencies into other layers do not count. DCA-CYC-005 covers the application layer "
        + "per operation; no rule slices the domain model within a module. Fewer than two slices pass.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
