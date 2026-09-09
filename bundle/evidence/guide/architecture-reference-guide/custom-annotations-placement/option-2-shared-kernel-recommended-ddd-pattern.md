---
type: Reference
title: "Custom Annotations Placement — Option 2: Shared Kernel (Recommended - DDD Pattern)"
tags: [reference]
evidence_for: "/guide/architecture-reference-guide/custom-annotations-placement.md#option-2-shared-kernel-recommended---ddd-pattern"
---

[Full node and context](/guide/architecture-reference-guide/custom-annotations-placement.md#option-2-shared-kernel-recommended---ddd-pattern). This is an evidence excerpt; retain the parent selection and caveats.

### Option 2: Shared Kernel (Recommended - DDD Pattern)

**For cross-context concerns** (used by multiple bounded contexts):

```
sharedkernel/
└── common/
    └── annotation/
        └── AsyncInitialize.java              ← Annotation definition

infrastructure/
└── config/
    └── AsyncInitializationProcessor.java     ← Processor implementation
```

**For context-specific concerns** (used by single bounded context only):

```
product/                                       ← One bounded context
└── common/
    └── annotation/
        └── ProductLifecycle.java              ← Context-specific annotation

infrastructure/
└── config/
    └── ProductLifecycleProcessor.java         ← Processor implementation
```

**Dependency flow**:
```
Domain (no deps)
  ↑
Application (depends on sharedkernel)
  ↑
Adapters (depends on sharedkernel)
  ↑
Infrastructure (depends on sharedkernel, processes annotation)
```

**Benefits**:
- Application layer can use it (accessible from any layer)
- Still framework-agnostic (pure Java metadata, no framework dependencies)
- Infrastructure provides the processing logic (follows DIP)
- Portable across frameworks (annotation definition is framework-independent)
- Follows DDD Shared Kernel pattern (shared across bounded contexts)
- Clear distinction between shared vs context-specific concerns
