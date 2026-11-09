---
type: Pitfall
title: "A rule that selects nothing reports green: it held over no element"
tags: [pitfall, governance, archunit, archunitnet, testing]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/strategic/dca-str-005.md, /rule/hexagonal/dca-hex-010.md, /rule/usecase/dca-use-001.md, /pitfall/architecture-suite-that-imported-nothing.md]
---

A rule selects the elements of one concept — the classes that carry a role, the modules of a layer, the types
named after a pattern — and checks each of them. Where the code carries the concept but not the sign the rule
selects by, the selection is empty, an empty selection has no violations, and the rule passes. The report shows the
same green for a rule that held over forty use cases and for one that saw none. Three shapes produce it:

- **The role is not named.** The code has use cases, ports or gateways, but no class names the marker that gives
  it the role: an implementation fits its interface by shape (a structural protocol) and never declares it. Every
  rule that selects by that role is silent.
- **The concept has a shape no marker fits.** A published interface written as a package of functions has no class
  to carry a class marker; a closed result written as a union of cases has no class named after the result. The
  rules that select the class see nothing.
- **The project has none of it.** No factory, no partnership, no external system. This is the honest case — but
  in the report it looks exactly like the other two.

## Why it is wrong

- A green rule is read as a rule that held. Nobody re-reads a passing rule, so a missing marker hides every rule
  that depends on it, for as long as the marker stays missing.
- The gap is invisible from the code as well: nothing is wrong with the classes, only with what the suite can see of
  them. A review of the code finds nothing; only the selection's size tells.
- The three shapes need different answers — add the marker, give the shape a marker it can carry, or state that
  the project has none — and a green report cannot tell them apart.

## How to spot it

- Read each rule's selection size beside its findings. A rule over the use cases that selected zero elements in a
  code base with use cases is not passing.
- Count the roles the code carries per marker and compare them with what the code has. A role with zero carriers
  is either a statement about the project or a gap; decide which.
- Remove the marker from one class you know a rule governs. A rule whose outcome does not change was never reading
  that class.

## What forbids it

- The suite itself, not one rule: a suite that reports each rule's selection fails an empty one by default — as
  ArchUnit fails an empty `should` unless the rule allows it — and lets the project allow an empty selection per
  rule, only with a reason. "No class is a factory" is then a statement about the project, read in every report.
- A rule that holds roles nominal: an implementation names the port it implements, so the rules over ports see it.
- [DCA-STR-005](/rule/strategic/dca-str-005.md) places an Open Host Service wherever it is marked — on the class, or
  on the package that publishes functions.

## Do instead

- Name the role. An implementation names its port, a use case its input port, a refusal its marker — the type
  checker's structural fit is not a role the rules can read.
- Give a concept the marker its shape can carry: a package of functions declares itself as a module, the way a
  bounded context does.
- Allow an empty selection rule by rule, with the reason, and only where the project truly has none of the concept.
  Revisit the list when the code grows: an allowed rule that selects something again is a statement that is no
  longer true.

The suite-wide form — an import that found no code at all — is
[An architecture suite that imported nothing](/pitfall/architecture-suite-that-imported-nothing.md).
