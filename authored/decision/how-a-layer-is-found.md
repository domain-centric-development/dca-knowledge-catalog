---
type: Decision
title: How a layer is found — by its package path, by a named package, or by an annotation
tags: [decision, governance, archunit, archunitnet]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/archunit-governance/setup-and-configuration.md, /rule/layered/dca-lay-007.md, /rule/hexagonal/dca-hex-019.md, /pitfall/switching-rules-off-for-an-own-vocabulary.md]
---

Every rule written for a layer — what the domain may depend on, where an output port's implementation lives, what an
incoming adapter may call — selects by the layer a class is placed in. The rule library has to be told how to find
that layer. Three ways answer it, and they can be combined per layer.

## Options

1. **The package path (the default).** A layer is its package below a module root: `domain`, `application`,
   `adapter.incoming`, `adapter.outgoing`, `infrastructure`. Nothing to configure; a project laid out as the
   templates show is placed completely.
2. **A named package.** The project keeps its layers in packages of another name (`adapter.out` instead of
   `adapter.outgoing`). The layout names that package per layer; the path rule stays, only the segment changes.
3. **An annotation the project already has.** The project marks its layers — with its own annotations or a
   library's (jMolecules, for example). The layout names that annotation per layer, usually beside the package
   (`anyOf`) during a migration. On a package declaration it holds for the package tree below; on a class it places
   that class. In .NET the attribute sits on the type, on the assembly, or as an assembly attribute that names a
   namespace.

## How to decide

- **The layout follows the templates** → the default. Configure nothing.
- **The layout is consistent but named differently** → a named package. One line per layer, no change to the code.
- **The layers are already declared in the code** → name the annotation. Do not add an annotation to the project for
  this: the library ships none, and an annotation that exists only to please the rules is a second layout to keep
  in step with the first.
- **There are no layers yet** → run without the layer rule sets (`hexagonal`, `layered`) and say why, until they
  stand. A layer rule over code without layers reports every class or none — neither is a statement about the code.

## Consequences

- **Precedence per class:** an annotation on the class, then the nearest declaration on a package above it, then the
  path. In .NET: the type's own attribute, then a namespace named by an assembly attribute, then the whole assembly,
  then the path. An annotation that contradicts the path wins; the report lists every such package, and every
  package that declares another layer than a package above it — one layer per subtree.
- **A class placed in no layer is seen by no layer rule.** A mapper beside the adapter packages, a class whose layer
  is declared only on its neighbour: `DCA-LAY-007` (experimental, informational) lists them per module. Run it once
  after changing how layers are found.
- **An output port implementation in no layer is still reported** (`DCA-HEX-019`): the implemented port says it is an
  outgoing adapter, so a class outside every layer is misplaced, not exempt.
- **Building blocks are never found by package.** A layer is a place; a value, an aggregate or a repository is what a
  type *is* — it is recognised by its supertype or an annotation, and a command or a query also by its name.

## Anchors

- Guide: [Setup and configuration](/guide/archunit-governance/setup-and-configuration.md)
- Pitfall: [Switching rules off because the project names things its own way](/pitfall/switching-rules-off-for-an-own-vocabulary.md)
- Rules: [DCA-LAY-007](/rule/layered/dca-lay-007.md) · [DCA-HEX-019](/rule/hexagonal/dca-hex-019.md)
