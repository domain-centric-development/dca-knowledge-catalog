---
type: Section
title: Infrastructure is not the same as framework
chapter: Dependency Structure
source: guide
resource: dca-guide/architecture/dependency-structure.md
tags: [guide, section]
---

An external framework is a library you depend on; your infrastructure layer is code you wrote to
wire that framework up. The two are governed differently. `@RestController` on an incoming adapter is
a framework annotation and always correct; a reference from that same controller to your own
`MetricsConfiguration` is a dependency on infrastructure and is not. Read a complaint about
"infrastructure" as being about your own wiring code, never about the library it configures.
