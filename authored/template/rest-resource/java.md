---
type: Template
title: "REST resource skeleton (incoming adapter injecting input ports) — Java"
parent: /template/rest-resource.md
tags: [template, adapter, rest]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-in/inputport.md, /marker/port-in/usecase.md, /marker/application/refusal.md, /marker/application/portexception.md, /marker/application/inputportexception.md, /rule/naming/dca-nam-006.md, /rule/hexagonal/dca-hex-003.md, /rule/hexagonal/dca-hex-004.md, /rule/naming/dca-nam-007.md, /guide/quick-reference/port-placement.md]
applies_to: [java]
framework: [spring]
---

The Java code of [REST resource skeleton (incoming adapter injecting input ports)](/template/rest-resource.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}Resource.java` — the controller

```java
package {basePackage}.{context}.adapter.incoming.api;

import {basePackage}.{context}.application.{usecasename}.{Name}Command;
import {basePackage}.{context}.application.{usecasename}.{Name}InputPort;
import {basePackage}.{context}.application.{usecasename}.{Name}Result;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Primary adapter exposing the {Name} use case over REST.
 * Depends on the input port interface (Dependency Inversion), not on a use-case implementation.
 */
@RestController
@RequestMapping("/api/{context}")
public class {Name}Resource {

    private final {Name}InputPort {usecasename}InputPort;

    public {Name}Resource(final {Name}InputPort {usecasename}InputPort) {
        this.{usecasename}InputPort = {usecasename}InputPort;
    }

    @PostMapping
    public ResponseEntity<{Name}Response> {usecasename}(
            @RequestBody final {Name}Request request) {

        // 1. map inbound DTO → application command
        final {Name}Command command = new {Name}Command(/* request.field(), ... */);

        // 2. drive the use case through its input port
        final {Name}Result result = {usecasename}InputPort.execute(command);

        // 3. map application result → outbound DTO
        return ResponseEntity.status(HttpStatus.CREATED).body({Name}Response.from(result));
    }
}
```

### Answering refusals — two variants

**Thrown.** The resource stays as above; the context's one `@RestControllerAdvice` maps each refusal type to its problem document:

```java
@RestControllerAdvice(basePackages = "{basePackage}.{context}.adapter.incoming.api")
public class {Context}ApiExceptionHandler {

    @ExceptionHandler({Name}NotFound.class)
    public ProblemDetail notFound(final {Name}NotFound exception) {
        return {Context}Problems.notFound(exception.{name}Id());
    }

    @ExceptionHandler({Rule}Violated.class)
    public ProblemDetail violated(final {Rule}Violated exception) {
        return {Context}Problems.violated(exception.{name}Id(), exception.requested(), exception.available());
    }
}
```

**Returned.** The resource switches over the sealed result, without a `default`; the answers live in one class of the context's adapter, so every call site answers a case the same way:

```java
    @PostMapping
    public ResponseEntity<?> {usecasename}(@RequestBody final {Name}Request request) {
        final {Name}Command command = new {Name}Command(/* request.field(), ... */);
        return switch ({usecasename}InputPort.execute(command)) {
            case {Name}Result.{Done} done ->
                    ResponseEntity.status(HttpStatus.CREATED).body({Name}Response.from(done));
            case {Name}Result.{Name}NotFound refusal ->
                    ResponseEntity.of({Context}Problems.notFound(refusal.{name}Id())).build();
            case {Name}Result.{Rule}Violated refusal ->
                    ResponseEntity.of({Context}Problems.violated(refusal.{name}Id(), refusal.requested(),
                            refusal.available())).build();
        };
    }
```

The handler stays in both for malformed input and the unexpected — a domain exception the use case does not name included, answered generically. Neither variant has a handler for `PortException` or `InputPortException`.

## `{Name}Request.java` / `{Name}Response.java` — edge DTOs

```java
package {basePackage}.{context}.adapter.incoming.api;

/** Inbound DTO — shape of the HTTP request body; the value objects built from it carry the rules. */
public record {Name}Request(/* client-facing fields, no annotation repeating a value object's rule */) {}

/** Outbound DTO — shape of the HTTP response. Maps from the use-case Result. */
public record {Name}Response(/* client-facing fields */) {
    public static {Name}Response from(final {Name}Result result) {
        return new {Name}Response(/* result.field(), ... */);
    }
}
```

The resource never touches a repository or a domain object — it converts DTOs at
the boundary and delegates all behaviour to the input port. Keep the `Resource`
suffix and keep DTOs in the adapter package, not in `domain/` or `application/`.
