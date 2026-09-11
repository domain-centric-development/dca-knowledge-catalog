---
type: Section
title: Port placement
chapter: Quick Reference
source: guide
resource: dca-guide/architecture/quick-reference.md
tags: [guide, section]
---

```
Port type | Interface declared in | Implemented in    | Called by
----------+-----------------------+-------------------+------------------
Input     | application           | application       | adapter/incoming
Output    | application           | adapter/outgoing  | application
```

The asymmetry is the whole point: an incoming adapter *uses* an input port, an outgoing adapter
*implements* an output port. Both interfaces are declared inside, never in the adapter.
