---
type: Template
title: "REST resource skeleton (incoming adapter injecting input ports)"
tags: [template, adapter, rest]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-in/inputport.md, /marker/port-in/usecase.md, /rule/naming/dca-nam-006.md, /rule/hexagonal/dca-hex-003.md, /rule/hexagonal/dca-hex-004.md, /rule/naming/dca-nam-007.md, /guide/architecture-reference-guide/ports-and-adapters.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for a REST resource: a primary (incoming) adapter that exposes use cases over HTTP. It lives in `adapter/incoming/api/`, is named `{Name}Resource`, depends only on **input port interfaces** (never on repositories or the domain directly), and maps each use case `Result` to a `*Response` record at the adapter edge. Request/response DTOs stay in the adapter package. Replace `{Name}` / `{usecasename}` / `{context}` / `{basePackage}`.

## `{Name}Resource.java` — the controller

```java
package {basePackage}.{context}.adapter.incoming.api;

import {basePackage}.{context}.application.{usecasename}.{Name}Command;
import {basePackage}.{context}.application.{usecasename}.{Name}InputPort;
import {basePackage}.{context}.application.{usecasename}.{Name}Result;
import jakarta.validation.Valid;
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
            @Valid @RequestBody final {Name}Request request) {

        // 1. map inbound DTO → application command
        final {Name}Command command = new {Name}Command(/* request.field(), ... */);

        // 2. drive the use case through its input port
        final {Name}Result result = {usecasename}InputPort.execute(command);

        // 3. map application result → outbound DTO
        return ResponseEntity.status(HttpStatus.CREATED).body({Name}Response.from(result));
    }
}
```

## `{Name}Request.java` / `{Name}Response.java` — edge DTOs

```java
package {basePackage}.{context}.adapter.incoming.api;

/** Inbound DTO — shape of the HTTP request body. */
public record {Name}Request(/* client-facing fields + validation annotations */) {}

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

## Realizes / governed by

- Markers: [InputPort](/marker/port-in/inputport.md) · [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- Rules: [REST controllers must end with 'Resource'](/rule/naming/dca-nam-006.md) · [Controllers and Resources must never access repositories directly](/rule/hexagonal/dca-hex-003.md) · [Incoming adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/dca-hex-004.md) · [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dca-nam-007.md)
- Guide: [Ports and adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- Recipe: [Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md)
