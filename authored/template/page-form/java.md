---
type: Template
title: "Form skeleton (the form object of a page adapter, named after its command) — Java"
parent: /template/page-form.md
tags: [template, adapter, dto, naming, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/naming/dca-nam-007.md, /rule/hexagonal/dca-hex-011.md, /guide/rules/domain-layer-rules.md, /guide/rules/error-handling-rules.md, /guide/rules/application-layer-rules.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [Form skeleton (the form object of a page adapter, named after its command)](/template/page-form.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Operation}{Aggregate}Form.java` — form record (web adapter)

```java
package {basePackage}.{context}.adapter.incoming.web;

/**
 * The form of the {Operation}{Aggregate}Command: the fields as the person typed them.
 * What they may hold is the value objects' rule, not this record's.
 */
public record {Operation}{Aggregate}Form(
        String title,
        String note) {

    /** The form a page renders before anything was typed. */
    public static {Operation}{Aggregate}Form empty() {
        return new {Operation}{Aggregate}Form("", "");
    }
}
```

No annotation of Bean Validation, no domain type, no method that builds the command. A field the browser restricts may bind to the type its control yields — `Integer` for a number field, `boolean` for a checkbox — and the controller's `BindingResult` answers what does not parse.

## The translation — in the page controller

```java
@PostMapping("/{context}/{aggregate}s")
public String {operation}(@ModelAttribute("form") final {Operation}{Aggregate}Form form,
                          final BindingResult binding,
                          final Model model,
                          final RedirectAttributes redirect) {
    // form → command: each raw field into the value object that carries its rule
    final var command = new {Operation}{Aggregate}Command(
            {Title}.fromInput(form.title()),
            {Note}.fromInput(form.note()));

    final var result = {operation}{Aggregate}.execute(command);
    // ... answer the result, POST–redirect–GET (see the page controller template)
}
```

A value object that refuses its input throws its named failure here, before the use case runs. The page controller answers it at its one translation site for that failure and renders the page again with `form` as submitted and the refusal at its field — in Spring MVC, `binding.rejectValue("title", <the refusal's message key>)` before the view is returned. The form record, the controller and the ViewModel sit in `adapter/incoming/web/`; the command and the value objects never import from there.
