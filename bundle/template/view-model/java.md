---
type: Template
title: "ViewModel skeleton (page-specific, primitive-only presentation record) — Java"
parent: /template/view-model.md
tags: [template, adapter, dto]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/java-package-structure.md, /guide/readme/rules.md, /rule/naming/dca-nam-007.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [ViewModel skeleton (page-specific, primitive-only presentation record)](/template/view-model.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

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
