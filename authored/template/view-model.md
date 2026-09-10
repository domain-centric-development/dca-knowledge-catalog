---
type: Template
title: "ViewModel skeleton (page-specific, primitive-only presentation record)"
tags: [template, adapter, dto]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/java-package-structure.md, /guide/readme/rules.md, /rule/naming/dca-nam-007.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for a **ViewModel**: a page-specific record that transforms a domain read model (or a use-case `Result`) into **primitives only** for a server-rendered template. It lives in the adapter layer at `{context}/adapter/incoming/web/`, is named `{Page}PageViewModel`, and is built by a **static factory** that maps domain types (`Money`, `{Name}Id`, enriched models) to `String` / `BigDecimal` / `int` / `boolean`. Its job is to stop domain types leaking into templates and to keep presentation formatting out of the application layer. One ViewModel **per page**, carrying exactly that page's fields — not one reusable model shared across pages. Replace `{Page}` / `{context}` / `{basePackage}`.

This is the web/MVC sibling of the API `*Response` DTO in the [REST resource template](/template/rest-resource.md): both are edge DTOs mapped from a `Result`, but a `Response` serialises to JSON for an API client while a ViewModel feeds a template. Keep the three layers distinct: `Result` (application) → ViewModel (web adapter) → DTO/`Response` (api adapter).

## `{Page}PageViewModel.java` — presentation record (web adapter)

```java
package {basePackage}.{context}.adapter.incoming.web;

import {basePackage}.{context}.application.{usecasename}.{Name}Result;
import {basePackage}.{context}.domain.model.Enriched{Name};
import java.math.BigDecimal;

/** Page-specific ViewModel: primitives only, tailored to the {Page} page. */
public record {Page}PageViewModel(
    String {name}Id,
    String name,
    BigDecimal priceAmount,
    String priceCurrency,
    int stockQuantity,
    boolean isAvailable,
    String pageTitle
) {

    // Factory maps the domain read model to primitives for the template.
    public static {Page}PageViewModel fromResult(final {Name}Result result) {
        final Enriched{Name} {name} = result.{name}();   // domain read model
        return new {Page}PageViewModel(
            {name}.{name}Id().value().toString(),
            {name}.name(),
            {name}.currentPrice().amount(),
            {name}.currentPrice().currency().getCurrencyCode(),
            {name}.stockQuantity(),
            {name}.isAvailable(),
            {name}.name());
    }
}
```

```java
// Controller converts Result → ViewModel, then hands primitives to the template.
final {Page}PageViewModel viewModel = {Page}PageViewModel.fromResult(result);
model.addAttribute("{name}", viewModel);
```

The ViewModel holds **no** domain type — a template must never dereference
`Money` or a typed id. It lives in the adapter package, so it depends on the
application `Result` and the domain read model, never the other way round.
When a read needs *no* cross-context enrichment at all, map the plain
use-case `Result` straight to the ViewModel and skip the enriched model.

## When a ViewModel is the wrong tool

A ViewModel only shapes data for one presentation surface — it does not decide
*how the read is produced*. Before building the read behind it, consult
[Plain query use case or a dedicated read model](/decision/read-model-vs-domain-query.md):
if the aggregate's repository can answer the query, a plain query use case feeds
the ViewModel; only a proven read/write skew or reporting need justifies a
dedicated CQRS read side. When the display combines state from several contexts,
put the cross-context rules in an [enriched domain model](/template/enriched-domain-model.md)
and let the ViewModel flatten it — don't push formatting or cross-context logic
into the ViewModel factory beyond primitive mapping.

## Realizes / governed by

- Guide: [Java package structure](/guide/readme/java-package-structure.md) · [Layer rules](/guide/readme/rules.md)
- Rule: [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dca-nam-007.md)
- Related templates: [Enriched domain model](/template/enriched-domain-model.md) · [REST resource](/template/rest-resource.md)
- Related decision: [Plain query use case or a dedicated read model](/decision/read-model-vs-domain-query.md)
