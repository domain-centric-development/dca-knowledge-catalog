---
type: Section
title: Table of Contents
chapter: Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/README.md
tags: [guide, section]
---

- [Key Points](#key-points)
- [Related Documentation](#related-documentation)
- [ELEMENTS](#elements)
  - [Domain Layer (Enterprise Business Rules)](#domain-layer-enterprise-business-rules)
  - [Application Layer (Use Cases / Application Business Rules)](#application-layer-use-cases--application-business-rules)
  - [Adapter Layer (Interface Adapters)](#adapter-layer-interface-adapters)
  - [Infrastructure Layer (Frameworks & Drivers)](#infrastructure-layer-frameworks--drivers)
  - [Strategic Architecture](#strategic-architecture)
- [RULES](#rules)
  - [The Fundamental Dependency Rule](#the-fundamental-dependency-rule)
  - [Domain Layer Rules](#domain-layer-rules)
  - [Application Layer Rules](#application-layer-rules)
  - [Adapter Layer Rules](#adapter-layer-rules)
  - [Infrastructure Layer Rules](#infrastructure-layer-rules)
  - [Strategic Design Rules](#strategic-design-rules)
  - [Boundary Crossing Rules](#boundary-crossing-rules)
  - [Testing Rules](#testing-rules)
  - [Packaging Rules](#packaging-rules)
- [JAVA PACKAGE STRUCTURE](#java-package-structure)
  - [Standard Structure (Fully Elaborated)](#standard-structure-fully-elaborated)
  - [Structure Evolution Example: From Startup to Maturity](#structure-evolution-example-from-startup-to-maturity)
- [DEPENDENCY STRUCTURE](#dependency-structure)
  - [Layer Dependency Flow](#layer-dependency-flow)
  - [Request Flow with Dependency Inversion](#request-flow-with-dependency-inversion)
  - [Cross-Bounded Context Communication](#cross-bounded-context-communication)
- [INTEGRATION PATTERNS](#integration-patterns)
  - [Same Bounded Context](#same-bounded-context)
  - [Different Bounded Contexts](#different-bounded-contexts)
  - [Open Host Service Pattern](#open-host-service-pattern)
  - [Composite Adapter Pattern](#composite-adapter-pattern)
  - [Resolver Pattern](#resolver-pattern)
  - [Enriched Read Model Pattern](#enriched-read-model-pattern)
  - [Factory for Cross-Context Assembly](#factory-for-cross-context-assembly)
- [DEVIATIONS FROM THE LITERATURE](#deviations-from-the-literature)
- [GENERAL PRINCIPLES](#general-principles)
- [ADDITIONAL TOPICS](#additional-topics)
- [REFERENCES & FURTHER READING](#references--further-reading)

## Related markers

- [Factory](/marker/tactical/factory.md)
