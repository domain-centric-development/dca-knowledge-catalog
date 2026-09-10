---
type: Reference
title: "Custom Annotations Placement — Option 1: Infrastructure Only (If only adapters/infrastructure need it)"
tags: [reference]
evidence_for: "/guide/architecture-reference-guide/custom-annotations-placement.md#option-1-infrastructure-only-if-only-adaptersinfrastructure-need-it"
---

[Full node and context](/guide/architecture-reference-guide/custom-annotations-placement.md#option-1-infrastructure-only-if-only-adaptersinfrastructure-need-it). This is an evidence excerpt; retain the parent selection and caveats.

### Option 1: Infrastructure Only (If only adapters/infrastructure need it)

```
infrastructure/
├── annotations/
│   └── AsyncInitialize.java              ← Annotation definition
└── lifecycle/
    └── AsyncInitializationProcessor.java  ← Processor implementation
```

**Use case**: Only adapters and infrastructure components need async initialization

**Limitation**: Application layer cannot use it (would violate dependency rules)
