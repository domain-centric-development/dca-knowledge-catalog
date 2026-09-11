---
type: Section
title: Where a custom annotation lives
chapter: Java Package Structure
source: guide
resource: dca-guide/architecture/package-structure.md
tags: [guide, section]
---

A custom annotation is neither a framework annotation nor infrastructure code: it is technical
metadata, like `@Nullable`. It has three possible homes, and the question that decides between them
is *who needs to read it*.

| | Infrastructure only | Shared kernel | One context |
|---|---|---|---|
| Application layer uses it | no | yes | yes, within that context |
| Several contexts use it | — | yes | no |
| Framework-independent | less so | yes | yes |
| Package | `infrastructure/annotation/` | `sharedkernel/common/annotation/` | `{context}/common/annotation/` |
| Example | `@Internal` | `@AsyncInitialize` | `@ProductLifecycle` |

**Shared kernel** when the annotation is framework-agnostic, carries no business rule and is read
across contexts and layers. The processor that acts on it is a different matter: it belongs to
infrastructure, because it is framework wiring.

**One context** when only that context's language contains the concept.

**Infrastructure only** when adapters and configuration are the sole readers. Note the limit this
imposes: the application layer may not depend on infrastructure, so an annotation placed there can
never be used on a use case.
