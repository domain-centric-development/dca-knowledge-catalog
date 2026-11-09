---
type: Recipe
title: Adopt the rules on existing code — scope, warn, ignore or freeze
tags: [recipe, governance, archunit, archunitnet, testing]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/archunit-governance/adoption-path-tiers.md, /guide/archunit-governance/tuning-the-rule-catalog.md, /guide/archunit-governance/setup-and-configuration.md, /decision/rules-that-differ-per-context.md]
---

An existing code base switches the rule catalog on and the first run is red, often by hundreds of violations. Fixing them all before the suite may run means it never runs. Four settings let the suite run from the first day and still fail on what the team breaks from then on. Each is a decision to record with its reason; none removes a rule from the report.

## When it applies

- The architecture test is new in a project that already has code.
- A rule set is switched on in a project that has been running others.
- A new library version brings rules the code does not meet yet.

## Steps

1. **Run the whole catalog once and count per rule.** The report names every rule with its violations. Sort them: rules already green, rules with a handful of violations, rules with many.
2. **Fix the handful now.** A rule with two or three violations is cheaper to meet than to configure.
3. **Decide per remaining rule, with the team:**
   - **Scope** (`dca.rules.sets`): leave a whole set out for now when the code is far from it — adopt the sets in stages, the cycles and layer rules first.
   - **Warn** (`dca.rules.warn`): the rule is reported and does not fail the build. For a rule the team means to meet step by step.
   - **Ignore by pattern** (`dca.rule.<id>.ignore`, one regular expression per key, `.ignore.1`, `.ignore.2` for more): a documented exception — a generated package, a legacy module that will not be touched. Works for every rule.
   - **Freeze** (`dca.rules.freeze` with `dca.rules.freeze.store`): today's violations are recorded in a baseline file; only a new one fails. For a rule the code breaks in many places that nobody will fix at once. The baseline shrinks as code is fixed and never grows on its own.
4. **Commit the configuration and the baseline.** The file (`dca-archunit.properties`) and the freeze store belong in version control: they are the record of what the team accepted and why.
5. **Run again: green.** The report lists the warned, ignored and frozen rules with their reasons.

## What freezing cannot do

A rule that runs several checks internally — the context-map set, the rules that iterate over the bounded contexts — has no single rule to build a baseline from. Freezing one fails with a message naming it; lower it to a warning or scope it with an ignore pattern instead.

The baseline file is per project and per language: Java and .NET write their own format, and the same key names a different file. A project with both stacks keeps two baselines.

## Do not

- Delete or switch off a failing rule to get green. Warn, ignore, freeze and scope keep the decision visible; off hides it.
- Freeze a rule with three violations. Fix them.
- Edit the baseline by hand to make a new violation pass. That is a decision to record as an ignore pattern with its reason.

## Anchors

- Guide: [Adoption path](/guide/archunit-governance/adoption-path-tiers.md) · [Tuning the rule catalog](/guide/archunit-governance/tuning-the-rule-catalog.md) · [Setup and configuration](/guide/archunit-governance/setup-and-configuration.md)
- Decision: [Rules that differ per context](/decision/rules-that-differ-per-context.md)
