---
type: Section
title: Core Concepts
chapter: Spring Modulith Implementation
source: guide
resource: implementing-domain-centric-architecture/spring-modulith.md
tags: [guide, section]
---

### Module

**Definition:** In Spring Modulith, **one top-level package = one module**

```
com.company.ecommerce
├── order/          ← Module (= Bounded Context)
├── customer/       ← Module (= Bounded Context)
└── inventory/      ← Module (= Bounded Context)
```

**Alignment:**
- One module = one bounded context (typical)
- One team owns one module (recommended)
- Module follows [Domain-Centric Architecture layers](/guide/readme/dependency-structure.md)

### Module Types

**Application Module** (default, recommended):
```java
@org.springframework.modulith.ApplicationModule
package com.company.ecommerce.order;
```
- Main business module
- Implements a bounded context
- Only specified packages are public

**Open Module** (use sparingly):
```java
@org.springframework.modulith.ApplicationModule(
    type = Type.OPEN
)
package com.company.ecommerce.shared;
```
- All packages are public
- Use only for shared kernel
- Requires team coordination

### Module API Surface

Modules expose clear API surfaces through specific packages:

**Published Package (`api/`):**
```java
// order/api/package-info.java
@org.springframework.modulith.NamedInterface("api")
package com.company.ecommerce.order.api;
```
- Public API of module
- Synchronous integration point
- Contains interfaces and DTOs

**Event Package (`events/`):**
```java
// order/events/package-info.java
@org.springframework.modulith.NamedInterface("events")
package com.company.ecommerce.order.events;
```
- Events published by module
- Asynchronous integration point
- Contains integration event DTOs

**Internal Package (`internal/`):**
- Hidden implementation
- Contains domain, application, adapter layers (see [Domain-Centric Architecture](/guide/readme/java-package-structure.md))
- Other modules CANNOT access
