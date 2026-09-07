---
type: Section
title: Tuning the Rule Catalog
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: dca-guide/archunit-governance.md
tags: [guide, section]
---

Whether the rules are hand-written or come from a rule library, a team adopting them on an existing
code base needs four dials. Without them the rule set is an all-or-nothing proposition, and a single
rule a team disagrees with is enough to make them abandon the whole thing.

| Dial | What it does | When to use it |
|------|--------------|----------------|
| **Scope** | run only some rule sets or rule ids | staged adoption — start with cycles and layer dependencies |
| **Severity** | report a violation without failing the build | a rule the team has committed to but not yet satisfied |
| **Exceptions** | tolerate individual violations of an otherwise enforced rule | one legacy package, generated code, a documented carve-out |
| **Baseline** | accept today's violations, fail only on new ones | large existing code bases, rule by rule |

Two properties matter more than the mechanism:

1. **A lowered rule stays visible.** Deleting a test for a rule the team decided against loses the
   decision. Reporting the rule as skipped, together with the reason, keeps it in the run and in the
   report where the next reader will find it.
2. **A typo must fail.** Configuration that silently ignores an unknown rule id will eventually leave
   a rule enforced that someone believes is switched off. Identifiers are therefore written in full
   (`DCA-NAM-002`, never the abbreviated `NAM-002`), and an unknown one aborts the run.

A rule library implements this as a selection object plus, for teams that would rather not touch test
code, a properties file:

```java
selection = RuleSelection.all()
    .onlySets("cycles", "layered", "hexagonal")             // scope
    .excluding("DCA-NAM-002", "no DI framework in this project")   // off, with the reason
    .warning("DCA-TAC-009", "value objects are being made final")  // reported, does not fail
    .ignoringViolationsMatching("DCA-STR-003", ".*legacy.*")       // documented exception
    .frozen("DCA-ONI-002");                                        // baseline
```

```properties
rules.sets              = cycles,layered,hexagonal
rules.off               = DCA-NAM-002
rule.DCA-NAM-002.reason = no DI framework in this project
rules.warn              = DCA-TAC-009
rule.DCA-STR-003.ignore = .*legacy.*
rule.DCA-STR-003.ignore.1 = Generated.{1,3}Client
rules.freeze            = DCA-ONI-002
```

An `ignore` value is one regular expression as written — commas are part of it — and a second
exception for the same rule uses an indexed key (`.ignore.1`, `.ignore.2`, …). Lists of rule ids and
set names are comma-separated.

With hand-written rules the same dials exist in cruder form: scope is which test classes you keep,
severity is a rule you evaluate and log instead of asserting, exceptions are extra `and()` predicates
or ArchUnit's `archunit_ignore_patterns.txt`, and the baseline is `FreezingArchRule` (see
[Freeze Violations for Legacy Code](#4-freeze-violations-for-legacy-code)).

**What none of the dials should be used for:** hiding a rule that is genuinely violated in new code.
Every lowered rule carries a reason, and the reason is the thing worth reviewing.

---
