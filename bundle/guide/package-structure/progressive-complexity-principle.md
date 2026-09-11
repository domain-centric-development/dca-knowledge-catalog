---
type: Section
title: Progressive Complexity Principle
chapter: Java Package Structure
source: guide
resource: dca-guide/architecture/package-structure.md
tags: [guide, section]
---

This structure shows **ALL possible subdivisions** for a fully-featured bounded context with significant complexity. However, you should **START SIMPLE** and add structure incrementally:

**🎯 Start Minimal**
- Begin with the 4 core layers (domain, application, adapter, infrastructure) without deep nesting
- Place files directly in layer directories until organization becomes difficult
- A simple bounded context may only need 5-10 files total

**📈 Add When Needed**
- Introduce subdirectories only when you have enough files that organization provides clear benefit
- Typically: >10 files in a directory suggests subdividing
- Let pain points guide structure, not theoretical perfection

**🔄 Refactor Later**
- It's easier to add structure later than to maintain unnecessary complexity early
- Moving files into new subdirectories is a simple refactoring
- IDEs handle this automatically with refactoring tools

**The structure below is a REFERENCE showing all options, not a prescription to use everything from day one.**
