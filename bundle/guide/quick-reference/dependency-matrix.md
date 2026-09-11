---
type: Section
title: Dependency matrix
chapter: Quick Reference
source: guide
resource: dca-guide/architecture/quick-reference.md
tags: [guide, section]
---

```
Layer          | May depend on
---------------+-----------------------------------------------------------
Domain         | nothing, or shared-kernel domain concepts
Application    | domain, shared kernel
Adapter (in)   | application, domain, shared kernel, external libraries
Adapter (out)  | the same, plus global and own-module infrastructure
Infrastructure | all of the above
Shared kernel  | nothing — framework-independent
```

Your own infrastructure layer is not the same thing as an external framework: every adapter may use
Spring. Your `infrastructure/` package is a different question, and the answer depends on direction —
an incoming adapter reaches none of it (`DCA-HEX-004`), an outgoing adapter reaches the global and
its own module's, but never another module's (`DCA-HEX-005`).
