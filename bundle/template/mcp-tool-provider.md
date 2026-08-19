---
type: Template
title: "MCP tool provider skeleton (incoming adapter exposing use cases as MCP tools)"
tags: [template, adapter, spring]
---

Domain-free skeleton for an **MCP tool provider**: a primary (incoming) adapter that exposes a bounded context's use cases as [Model Context Protocol](https://modelcontextprotocol.io) tools an AI model can invoke. It is the AI-facing sibling of a REST `*Resource` — same shape, different transport: it lives in `{context}/adapter/incoming/mcp/`, is named `{Context}McpToolProvider`, is a Spring `@Component`, depends only on **input port interfaces**, and maps each use-case `Result` to an edge DTO. Each tool method carries an `@McpTool(name, description)` — the description is the AI's only guide to the tool, so write it for a model, not a human. Read-only query tools are the safe default. Replace `{Context}` / `{Name}` / `{usecasename}` / `{basePackage}`.

## `{Context}McpToolProvider.java` — incoming adapter

```java
package {basePackage}.{context}.adapter.incoming.mcp;

import {basePackage}.{context}.adapter.incoming.api.{Name}Dto;
import {basePackage}.{context}.application.{usecasename}.{Name}InputPort;
import {basePackage}.{context}.application.{usecasename}.{Name}Query;
import {basePackage}.{context}.application.{usecasename}.{Name}Result;
import java.util.List;
import org.springaicommunity.mcp.annotation.McpTool;
import org.springframework.stereotype.Component;

/**
 * Primary (incoming) adapter exposing {context} use cases as MCP tools for AI models.
 * Depends on input port interfaces (Dependency Inversion), not on use-case implementations,
 * and never on repositories or the domain directly — exactly like a REST resource.
 */
@Component
public class {Context}McpToolProvider {

    private final {Name}InputPort {usecasename}InputPort;

    public {Context}McpToolProvider(final {Name}InputPort {usecasename}InputPort) {
        this.{usecasename}InputPort = {usecasename}InputPort;
    }

    @McpTool(
        name = "{tool-name}",
        description = "What the tool does and what it returns — written for the AI model to decide when to call it.")
    public {Name}Dto {usecasename}(final String id) {
        final {Name}Result result = {usecasename}InputPort.execute(new {Name}Query(id));
        // map application Result → edge DTO; never expose domain types to the model
        return {Name}Dto.from(result);
    }
}
```

The provider converts inputs and results at the boundary and delegates all
behaviour to the input port. Keep the `McpToolProvider` suffix, keep the class in
`adapter/incoming/mcp/`, and return DTOs (the same edge DTOs the REST adapter
uses) — an MCP tool must not hand a `Money`, a typed id, or an aggregate to the
model. Like the `Store` marker, the `*McpToolProvider` naming is a **convention,
not an enforced ArchUnit rule** — hold it by discipline.

## Realizes / governed by

- Markers: [InputPort](/marker/port-in/inputport.md) · [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md)
- Rules: [Incoming adapters must only access their own bounded context](/rule/hexagonal/incoming-adapters-must-only-access-their-own-bounded-context-except-event-consumers-and-open-host-services.md) · [Incoming adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/incoming-adapters-must-only-use-outbound-ports-not-infrastructure-implementations.md) · [Controllers and Resources must never access repositories directly](/rule/hexagonal/controllers-and-resources-must-never-access-repositories-directly.md) · [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dtos-must-reside-in-the-adapter-layer-not-in-domain-or-application.md)
- Guide: [Java Package Structure](/guide/readme/java-package-structure.md) · [Layer structure](/guide/architecture-reference-guide/layer-structure.md)
- Sibling template: [REST resource](/template/rest-resource.md)
- Recipe: [Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md)
