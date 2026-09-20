---
type: Pitfall
title: "An architecture suite that imported nothing: green because it looked at no code"
tags: [pitfall, governance, archunit, archunitnet, testing]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/strategic/dca-str-011.md, /rule/strategic/dca-str-001.md, /reference/architecture.md]
---

An architecture test that passes every rule while the set of classes it selects over is empty. The suite reports success, the build stays green, and nothing in the report says that no production class was read. Three shapes produce it:

- **The import found nothing.** The base package is misspelt, the production code is not compiled, or the test source set sees no production module.
- **The import found only part of the code.** In a multi-module build the other modules reach the test class path as jars; a class-path filter that excludes jars leaves those modules unimported. The rules then govern the one module that happens to hold the test.
- **Nothing declares a bounded context.** Rules that select over the declared contexts — the context map, the isolation rules between contexts — have an empty selection, and an empty selection has no violations.

## Why it is wrong

- A green suite is read as evidence. Nobody re-reads a test that passes, so the gap survives every later change and grows with the code it never looked at.
- The failure is silent by construction. A rule reports what it found; it cannot report what it was never shown.
- It is most likely exactly where governance matters most: the day a second module is split off, or the day a project adopts the rules on a code base that has not declared its contexts yet.

## How to spot it

- Compare the number of imported classes with the size of the code base — the diagnostic rule that prints the discovered contexts is the cheapest place to see both.
- Read the discovered contexts in the report. A build with eight modules and one discovered context is not a passing suite, it is an incomplete one.
- Switch off a rule you know the code violates, then switch it back on. A suite that stays green either way is not reading your code.

## What forbids it

- [DCA-STR-011](/rule/strategic/dca-str-011.md) — at least one bounded context is declared.
- [DCA-STR-001](/rule/strategic/dca-str-001.md) — the discovered contexts appear in the report, so an empty model is visible rather than implied.

## Do instead

- Let the loader refuse an empty import instead of running rules over nothing: an import that found no class below the base package, or assemblies that hold no type below the root namespace, is a setup error and belongs in the failure report.
- Let the module that runs the architecture test depend on every module that holds production code, and import jars as well — in a multi-module build the other modules *are* jars on that class path. Narrow the import only where a third-party artifact ships the project's own base package, and say so at the call site.
- Declare the contexts. A single-context application declares its base package; without a declaration the context-map rules have nothing to govern.
- Where a code base deliberately declares no context, switch the rule off with a recorded reason. A recorded decision is visible in the report; a silent empty selection is not.
