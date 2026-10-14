---
type: Template
title: "Page controller skeleton (server-rendered web adapter) — Java"
parent: /template/page-controller.md
tags: [template, adapter, spring, use-case, security]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-in/inputport.md, /marker/port-in/usecase.md, /rule/naming/dca-nam-005.md, /rule/hexagonal/dca-hex-003.md, /rule/hexagonal/dca-hex-011.md, /rule/hexagonal/dca-hex-012.md, /rule/naming/dca-nam-011.md, /rule/usecase/dca-use-008.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [Page controller skeleton (server-rendered web adapter)](/template/page-controller.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}PageController.java` — the controller

```java
package {basePackage}.{context}.adapter.incoming.web;

import {basePackage}.{context}.application.{usecasename}.{Name}Command;
import {basePackage}.{context}.application.{usecasename}.{Name}InputPort;
import {basePackage}.{context}.application.{usecasename}.{Name}Result;
import {basePackage}.{context}.application.show{name}.Show{Name}InputPort;
import {basePackage}.{context}.application.show{name}.Show{Name}Query;
import {basePackage}.{context}.domain.model.{Name}Id;
import {basePackage}.{context}.domain.model.{Name}NotFound;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import java.util.UUID;

/**
 * Primary adapter for the {Name} pages. Injects input port interfaces only:
 * no repository, no use-case class, no domain service.
 */
@Controller
@RequestMapping("/{context}/{name}s")
public class {Name}PageController {

    private final Show{Name}InputPort show{Name};
    private final {Name}InputPort {usecasename};

    public {Name}PageController(final Show{Name}InputPort show{Name},
                                final {Name}InputPort {usecasename}) {
        this.show{Name} = show{Name};
        this.{usecasename} = {usecasename};
    }

    /** Read: GET renders, changes nothing. A notice arrives as a code in the URL. */
    @GetMapping("/{id}")
    public String show(@PathVariable final UUID id,
                       @RequestParam(name = "notice", required = false) final String notice,
                       final Model model) {
        final var result = show{Name}.execute(new Show{Name}Query(new {Name}Id(id)));
        model.addAttribute("{name}", {Name}PageViewModel.fromResult(result));
        model.addAttribute("form", {Name}Form.empty());
        {Name}PageNotice.fromCode(notice).ifPresent(known -> model.addAttribute("notice", known));
        return "{context}/{name}";
    }

    /** Write: only an unsafe method reaches a command use case. */
    @PostMapping("/{id}/{usecasename}")
    public String {usecasename}(@PathVariable final UUID id,
                                @Valid @ModelAttribute("form") final {Name}Form form,
                                final BindingResult binding,
                                final Model model) {
        if (binding.hasErrors()) {
            // re-render the same page with the submitted form and its messages
            final var result = show{Name}.execute(new Show{Name}Query(new {Name}Id(id)));
            model.addAttribute("{name}", {Name}PageViewModel.fromResult(result));
            return "{context}/{name}";
        }

        // 1. form → application command
        final {Name}Command command = new {Name}Command(new {Name}Id(id) /*, form.field(), ... */);

        // 2. drive the use case through its input port
        final {Name}Result result = {usecasename}.execute(command);

        // 3. POST–redirect–GET: a refresh must not repeat the change; the notice travels as a code
        return "redirect:/{context}/{name}s/" + id + "?notice=" + {Name}PageNotice.DONE.code();
    }

    /** Domain exception → transport: a missing aggregate is a 404 page, not a stack trace. */
    @ExceptionHandler({Name}NotFound.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public String notFound(final {Name}NotFound ex, final Model model) {
        model.addAttribute("{name}Id", ex.{name}Id().value().toString());
        return "{context}/{name}-not-found";
    }
}
```

The two `show{Name}.execute(...)` calls are the read path — a re-render after a validation failure asks the same query the GET does. An `@GetMapping` never calls a command port: a link that creates, cancels or deletes is the [state-changing GET endpoint](/pitfall/state-changing-get-endpoint.md) pitfall. Mapping and formatting is all the controller does; combining fields into a new business fact or checking an invariant here is [business logic in the adapter](/pitfall/business-logic-in-adapter.md).

The notice after the redirect is a code in the URL, not a flash attribute: a flash attribute lives in the session of the instance that wrote it, and behind a load balancer the GET may reach another one — see [State kept in one instance](/pitfall/state-kept-in-one-instance.md).

## `{Name}PageNotice.java` — the codes a redirect may carry (web adapter)

```java
package {basePackage}.{context}.adapter.incoming.web;

import java.util.Arrays;
import java.util.Optional;

/**
 * The notices a {Name} page shows after a redirect. The URL carries the code, never the
 * sentence; the page maps it here and shows nothing for a code it does not know.
 */
public enum {Name}PageNotice {

    DONE("done", "{name}.{usecasename}.done");

    private final String code;
    private final String messageKey;

    {Name}PageNotice(final String code, final String messageKey) {
        this.code = code;
        this.messageKey = messageKey;
    }

    public String code() {
        return code;
    }

    public String messageKey() {
        return messageKey;
    }

    public static Optional<{Name}PageNotice> fromCode(final String code) {
        return Arrays.stream(values()).filter(notice -> notice.code.equals(code)).findFirst();
    }
}
```

One value per notice the pages of this controller show, each with its code and its text — here a message key the translations resolve. A code is part of a URL a person can bookmark or edit, so it names *which* notice, never data, and an unknown or stale one is ignored rather than rendered.

## `{Name}Form.java` — form record with Bean Validation (web adapter)

```java
package {basePackage}.{context}.adapter.incoming.web;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/** Shape of the HTML form. Syntactic validation only — business rules stay in the domain. */
public record {Name}Form(
        @NotBlank @Size(max = 120) String label,
        @Min(1) int quantity) {

    public static {Name}Form empty() {
        return new {Name}Form("", 1);
    }
}
```

Bean Validation on the form checks *shape*: required, length, range, format. It does not check whether the change is allowed — that invariant belongs to the aggregate, which throws a domain exception the controller maps below. The form record is an edge DTO and stays in `adapter/incoming/web/`, next to the ViewModel; neither belongs in `application/` or `domain/`.

## The template — form, CSRF token, messages

```html
<form method="post" th:action="@{/{context}/{name}s/{id}/{usecasename}(id=${{name}.{name}Id})}"
      th:object="${form}">
    <input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
    <label>Label <input type="text" th:field="*{label}"/></label>
    <p th:if="${#fields.hasErrors('label')}" th:errors="*{label}"></p>
    <label>Quantity <input type="number" th:field="*{quantity}"/></label>
    <p th:if="${#fields.hasErrors('quantity')}" th:errors="*{quantity}"></p>
    <button type="submit">Apply</button>
</form>
<p th:if="${notice}" th:text="#{${notice.messageKey()}}"></p>
```

Every browser form that changes state carries the CSRF token (Spring Security's Thymeleaf integration adds it to `th:action` forms automatically; the explicit hidden field shows what must be there). Errors and the notice are rendered by the server, so the page degrades to plain HTML — no script is needed to submit, validate or confirm.
