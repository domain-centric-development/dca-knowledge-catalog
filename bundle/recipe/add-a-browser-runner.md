---
type: Recipe
title: Add a browser runner to an existing project
tags: [recipe, testing, bootstrap]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/e2e-testing/one-test-per-acceptance-criterion.md, /guide/e2e-testing/page-object-pattern.md, /guide/e2e-testing/data-test-attributes.md]
---

A project shows pages and has no way to drive a browser in its tests. Every story about a page then falls back to reading markup or script as text, which proves the wording and not the behaviour. Set the runner up once, as its own step, before the next story that needs it.

## Steps

1. **Pick the runner the build already speaks** — a test dependency for a JVM or .NET build, a package for a JavaScript build; pin the version and install the browser builds that release expects.
2. **Give the browser tests their own source set or test project and one command**, apart from the fast unit suite, and decide whether the application is started by the test or beside it (the guide's *Where the application runs*).
3. **Write one smoke test** — open the start page, assert its title through a stable `data-test` selector, through the Page Object and base class later tests share.
4. **Show that it can fail** — empty the title, see the smoke test red, restore it, see it green. A browser test that was never red may test nothing.
5. **Record the command and the runner's name** where the project keeps its build facts, so the next plan takes browser tests as the shape for a page.

## Anchors

- Guide: [One test per acceptance criterion](/guide/e2e-testing/one-test-per-acceptance-criterion.md) — *Adding a browser runner to an existing project*, *When there is no browser to drive*, *Where the application runs* · [Page Object Pattern](/guide/e2e-testing/page-object-pattern.md) · [Data-test attributes](/guide/e2e-testing/data-test-attributes.md)
- From zero instead: [Bootstrap a new application](/recipe/bootstrap-a-new-application.md)
