---
type: Reference
title: Custom Annotations Placement — Understanding Shared Kernel Common Layer
tags: [reference]
evidence_for: "/guide/architecture-reference-guide/custom-annotations-placement.md#understanding-shared-kernel-common-layer"
---

[Full node and context](/guide/architecture-reference-guide/custom-annotations-placement.md#understanding-shared-kernel-common-layer). This is an evidence excerpt; retain the parent selection and caveats.

### Understanding Shared Kernel Common Layer

Before discussing placement options, it's important to understand the **Shared Kernel** pattern from Domain-Driven Design:

**Shared Kernel** = Code shared across ALL bounded contexts in your application

Within the Shared Kernel, we distinguish between:

1. **`sharedkernel.domain`** - Domain concepts shared across contexts
   - Example: `Money`, `ProductId`, `CustomerId`
   - Represents business concepts needed by multiple contexts

2. **`sharedkernel.common`** - Technical utilities shared across contexts
   - Example: `@AsyncInitialize`, `Clock`, utility interfaces
   - NOT business logic, but cross-cutting technical concerns
   - Framework-agnostic (no Spring, no JPA, pure Java)

3. **`[context].common`** - Context-specific utilities (alternative)
   - Example: `product.common.annotation.ProductLifecycle`
   - Only needed within one bounded context
   - Use when the concern is specific to that context

**Key Difference from "Infrastructure"**:
- `sharedkernel.common` = Accessible by ALL layers, ALL contexts, framework-agnostic
- `infrastructure` = Framework wiring, configuration, Spring beans, NOT accessible by domain/application

**Why this matters for `@AsyncInitialize`**:
- It's NOT a framework annotation (not from Spring/Jakarta)
- It's NOT infrastructure code (no Spring dependencies)
- It IS technical metadata (like `@Nullable`, `@NonNull`)
- It SHOULD be accessible across all contexts and layers
- Therefore → belongs in `sharedkernel.common.annotation`
