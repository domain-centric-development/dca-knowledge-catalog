---
type: Template
title: "MCP tool provider skeleton (incoming adapter exposing use cases as MCP tools)"
tags: [template, adapter, spring]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-in/inputport.md, /marker/port-in/usecase.md, /rule/hexagonal/dca-hex-007.md, /rule/hexagonal/dca-hex-004.md, /rule/hexagonal/dca-hex-003.md, /rule/naming/dca-nam-007.md, /guide/readme/java-package-structure.md, /guide/architecture-reference-guide/layer-structure.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for an **MCP tool provider**: a primary (incoming) adapter that exposes a bounded context's use cases as [Model Context Protocol](https://modelcontextprotocol.io) tools an AI model can invoke. It is the AI-facing sibling of a REST `*Resource` — same shape, different transport: it lives in `{context}/adapter/incoming/mcp/`, is named `{Context}McpToolProvider`, is a Spring `@Component`, depends only on **input port interfaces**, and maps each use-case `Result` to an edge DTO. Each tool method carries an `@McpTool(name, description)` — the description is the AI's only guide to the tool, so write it for a model, not a human. Read-only query tools are the safe default. Replace `{Context}` / `{Name}` / `{usecasename}` / `{basePackage}`.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`mcp-tool-provider/java.md`](/template/mcp-tool-provider/java.md)

## Realizes / governed by

- Markers: [InputPort](/marker/port-in/inputport.md) · [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md)
- Rules: [Incoming adapters must only access their own bounded context](/rule/hexagonal/dca-hex-007.md) · [Incoming adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/dca-hex-004.md) · [Controllers and Resources must never access repositories directly](/rule/hexagonal/dca-hex-003.md) · [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dca-nam-007.md)
- Guide: [Java Package Structure](/guide/readme/java-package-structure.md) · [Layer structure](/guide/architecture-reference-guide/layer-structure.md)
- Sibling template: [REST resource](/template/rest-resource.md)
- Recipe: [Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md)
