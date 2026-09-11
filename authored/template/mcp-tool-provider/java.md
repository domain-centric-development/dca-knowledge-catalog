---
type: Template
title: "MCP tool provider skeleton (incoming adapter exposing use cases as MCP tools) — Java"
parent: /template/mcp-tool-provider.md
tags: [template, adapter, spring]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-in/inputport.md, /marker/port-in/usecase.md, /rule/hexagonal/dca-hex-007.md, /rule/hexagonal/dca-hex-004.md, /rule/hexagonal/dca-hex-003.md, /rule/naming/dca-nam-007.md, /guide/package-structure.md, /guide/elements.md]
applies_to: [java]
framework: [spring]
---

The Java code of [MCP tool provider skeleton (incoming adapter exposing use cases as MCP tools)](/template/mcp-tool-provider.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

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
