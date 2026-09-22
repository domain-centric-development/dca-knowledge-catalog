---
type: Decision
title: Rules that differ per context — scope them in the suite, not in the selection
tags: [decision, governance, bounded-context, subdomain]
review: draft
owner: DCA catalog maintainers
evidence: [/reference/architecture.md, /decision/pattern-style-per-subdomain.md, /guide/archunit-governance.md]
---

Not every context earns the same rules. A context with a rich domain model wants the tactical set in full;
one that is a transaction script over lookup data would spend its days fighting rules about aggregates it
does not have. The question is not *whether* rules differ per context — they do — but *where* that
difference is written down.

**Not in the rule selection.** A selection today answers four questions: which rule ids run, which rule sets
run, at what severity, and which existing violations are tolerated. Adding "and in which context" multiplies
that surface by the number of modules, and every answer becomes a pair. The configuration file stops being
readable in one glance, and the question "does this rule hold here?" needs two lookups instead of one.

**In the architecture suite, as plain rules.** A project that wants the tactical rules only for its
domain-model contexts writes them there, scoped to those packages, with the reason in the `because` clause
and the decision in an ADR. That is a handful of lines, it reads as what it is, and the scoping is visible
next to the rule instead of hidden in a properties file three directories away.

**Three reasons this is the better place.**

1. **The structural baseline must not become negotiable.** Layer dependencies, cycles and context isolation
   hold for every context, whatever style it is written in. A per-context dial invites switching them off
   module by module, and each of those decisions is invisible in the next code review.
2. **Comparable verdicts are the point.** Two implementations of the same system should reach the same
   verdict; a rule that holds in one module and not in another makes "the suite is green" mean something
   different per module, and the difference lives in configuration rather than in the code.
3. **The escape hatches already exist and are narrower.** A single id can be lowered to a warning or
   switched off with a recorded reason, and an individual violation can be tolerated by pattern — which
   includes a package pattern, so a genuinely local exception is expressible without a new mechanism.

**When to revisit.** If the tolerated-violation patterns in real projects decay into lists of module names,
the selection is being used as a per-context dial through the back door, and the decision deserves another
look. Until then the cost of the mechanism is higher than the cost of writing the scoped rules out.

- [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md)
- [Architecture reference](/reference/architecture.md)
- [ArchUnit governance](/guide/archunit-governance.md)
