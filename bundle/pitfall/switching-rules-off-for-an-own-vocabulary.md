---
type: Pitfall
title: Switching rules off because the project names things its own way
tags: [pitfall, governance, archunit, archunitnet]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/archunit-governance/setup-and-configuration.md, /guide/archunit-governance/tuning-the-rule-catalog.md, /rule/hexagonal/dca-hex-007.md, /rule/usecase/dca-use-001.md, /rule/usecase/dca-use-013.md, /rule/strategic/dca-str-011.md]
---

An existing code base adopts the rule library. It already has its own marker interfaces, its own context
annotation, a start-up module, a naming convention. The first run reports thousands of lines, and the quick way to a
green build is `dca.rules.off` or an `ignore` pattern per finding. The rules that were switched off then check
nothing, although the code they were written for is there under another name.

## Why it is wrong

- **Silence instead of governance.** A rule switched off because it could not *find* the code is not a rule the
  project rejected. The report shows an exemption with a reason that is really "the library did not know our names".
- **The real findings drown.** Configuration noise and genuine violations arrive in the same list; whoever thins the
  list by switching rules off removes both.
- **Ignore patterns rot.** A pattern per class or package holds only for the names that existed on the day it was
  written.

## How to spot it

`dca.rules.off` or `dca.rule.<id>.ignore` entries whose reason names a type, an annotation, a suffix or a package
layout rather than a decision about the code; a module-isolation rule (`DCA-HEX-007`, `DCA-HEX-002`) failing for every
pair of contexts at once; the context-declaration rule (`DCA-STR-011`) failing although the project declares its
contexts with its own annotation.

## Do instead

**Tell the layout once, then read what is left as findings about the code.**

- **Own markers** — point the marker roles at the project's types (`DcaMarkers`: aggregate root, value, repository,
  output port, …). A role names one type, matched by assignability; where the project has two shapes, name their
  common supertype.
- **Own context annotations** — the context, shared-kernel and integration-event-type annotations are roles too; the
  rules read their members by name. The relationship annotations stay the library's.
- **A start-up module named like a layer** — exclude it from the import; otherwise the base package becomes a module
  beside the contexts and every context a neighbour of every other.
- **Own suffixes** — the use-case, input-port, controller and REST-adapter suffixes are layout settings.
- **Ports that never leave the process** — declare them local; the rule about remote calls inside a transaction
  (`DCA-USE-013`) then reports only the ports that call out.

After that, an `off` entry carries a reason about the code or a convention the project deliberately does not adopt
(for example in-process published contracts), and every remaining failure is a statement about the code.

## Anchors

- Guide: [Setup and configuration](/guide/archunit-governance/setup-and-configuration.md) · [Tuning the rule catalog](/guide/archunit-governance/tuning-the-rule-catalog.md)
- Pitfall: [An architecture suite that imported nothing](/pitfall/architecture-suite-that-imported-nothing.md)
- Rules: [DCA-HEX-007](/rule/hexagonal/dca-hex-007.md) · [DCA-USE-001](/rule/usecase/dca-use-001.md) · [DCA-USE-013](/rule/usecase/dca-use-013.md) · [DCA-STR-011](/rule/strategic/dca-str-011.md)
