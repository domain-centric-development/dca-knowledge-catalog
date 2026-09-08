---
type: Template
title: "Page controller skeleton (server-rendered web adapter)"
tags: [template, adapter, spring, use-case, security]
---

Domain-free skeleton for a **page controller**: a primary (incoming) adapter that drives use cases from a server-rendered browser page. It lives in `adapter/incoming/web/`, is named `{Name}PageController`, and depends only on **input port interfaces** — never on a repository, a use-case class or a domain service. Reads are `@GetMapping` methods that map a query `*Result` to a page-specific [ViewModel](/template/view-model.md); every state change is a `@PostMapping` on a form record that answers with a `redirect:` (POST–redirect–GET). The page works without JavaScript: plain HTML forms, a CSRF token in each of them, validation messages rendered by the server. Replace `{Name}` / `{name}` / `{usecasename}` / `{context}` / `{basePackage}`.

This is the browser sibling of the [REST resource](/template/rest-resource.md): the same input ports, the same rule that the adapter converts at the edge and decides nothing, but the edge types are a form record and a ViewModel instead of a `*Request`/`*Response` pair.

## `{Name}PageController.java` — the controller

```java
package {basePackage}.{context}.adapter.incoming.web;

import {basePackage}.{context}.application.{usecasename}.{Name}Command;
import {basePackage}.{context}.application.{usecasename}.{Name}InputPort;
import {basePackage}.{context}.application.{usecasename}.{Name}Result;
import {basePackage}.{context}.application.show{name}.Show{Name}InputPort;
import {basePackage}.{context}.application.show{name}.Show{Name}Query;
import {basePackage}.{context}.domain.{name}.{Name}Id;
import {basePackage}.{context}.domain.{name}.{Name}NotFound;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
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

    /** Read: GET renders, changes nothing. */
    @GetMapping("/{id}")
    public String show(@PathVariable final UUID id, final Model model) {
        final var result = show{Name}.execute(new Show{Name}Query(new {Name}Id(id)));
        model.addAttribute("{name}", {Name}PageViewModel.fromResult(result));
        model.addAttribute("form", {Name}Form.empty());
        return "{context}/{name}";
    }

    /** Write: only an unsafe method reaches a command use case. */
    @PostMapping("/{id}/{usecasename}")
    public String {usecasename}(@PathVariable final UUID id,
                                @Valid @ModelAttribute("form") final {Name}Form form,
                                final BindingResult binding,
                                final Model model,
                                final RedirectAttributes redirect) {
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

        // 3. POST–redirect–GET: a refresh must not repeat the change
        redirect.addFlashAttribute("notice", "{name}.{usecasename}.done");
        return "redirect:/{context}/{name}s/" + id;
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
<p th:if="${notice}" th:text="#{${notice}}"></p>
```

Every browser form that changes state carries the CSRF token (Spring Security's Thymeleaf integration adds it to `th:action` forms automatically; the explicit hidden field shows what must be there). Errors and the flash notice are rendered by the server, so the page degrades to plain HTML — no script is needed to submit, validate or confirm.

## Realizes / governed by

- Markers: [InputPort](/marker/port-in/inputport.md) · [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- Rules: [Controller classes must end with 'Controller'](/rule/naming/controller-classes-must-end-with-controller.md) · [Controllers and Resources must never access repositories directly](/rule/hexagonal/controllers-and-resources-must-never-access-repositories-directly.md) · [Incoming Adapters must depend on input port interfaces, not on use case classes](/rule/hexagonal/incoming-adapters-must-depend-on-input-port-interfaces-not-on-use-case-classes.md) · [Incoming Adapters must not depend on domain services](/rule/hexagonal/incoming-adapters-must-not-depend-on-domain-services.md) · [ViewModels must reside in adapter.incoming.web packages](/rule/naming/viewmodels-must-reside-in-adapter-incoming-web-packages.md) · [HTTP Response Models must end with 'Response' and reside in adapter incoming package](/rule/usecase/http-response-models-must-end-with-response-and-reside-in-adapter-incoming-package.md) · [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dtos-must-reside-in-the-adapter-layer-not-in-domain-or-application.md)
- Guide: [Layer rules](/guide/readme/rules.md) (input adapter rules, exception flow) · [Ports and adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- Pitfalls: [State-changing GET endpoint](/pitfall/state-changing-get-endpoint.md) · [Business logic in adapter](/pitfall/business-logic-in-adapter.md)
- Related templates: [ViewModel](/template/view-model.md) · [Domain exception](/template/domain-exception.md) · [REST resource](/template/rest-resource.md)
