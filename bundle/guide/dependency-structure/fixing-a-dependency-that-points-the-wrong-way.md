---
type: Section
title: Fixing a dependency that points the wrong way
chapter: Dependency Structure
source: guide
resource: dca-guide/architecture/dependency-structure.md
tags: [guide, section]
---

When an adapter needs something that sits in infrastructure, one of three moves resolves it:

1. **Declare it as an output port** — when a use case needs the capability. The interface goes into
   the application layer, the implementation into `adapter/outgoing`, and the use case is its caller.

   ```java
   // {context}/application/shared/MetricsPublisher.java
   public interface MetricsPublisher extends OutputPort {
       void increment(String metric);
   }

   // {context}/adapter/outgoing/metrics/PrometheusMetricsAdapter.java
   class PrometheusMetricsAdapter implements MetricsPublisher { /* … */ }
   ```

2. **Move it into the shared kernel** when it is framework-agnostic and every context needs it.

3. **Move the concern into the use case, or keep it in the adapter.** Often the adapter should not
   have had it at all — the application layer is where the decision belongs. What remains adapter
   mechanics (a cookie, a header, a token) stays a class in the adapter package without a port marker.

## Related mentions (heuristic)

- [OutputPort](/marker/port-out/outputport.md)
