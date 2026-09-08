---
type: Rule
id: DCA-MAP-013
title: "Diagnostic: Display declared context map"
rule: Printing the declared edges makes the executable context map reviewable at a glance.
constraint: "Diagnostic: Display declared context map."
selects: "Every @Upstream, @ExternalUpstream and @Partnership declaration on the package-info of every package carrying @BoundedContext, reading context() or name(), translation(), and via() or interaction()."
checks: "Informational - prints every declared edge to standard output and never fails; it carries no assertion. status() is not printed, so a PLANNED edge is listed like an implemented one."
enforced_by: "ContextMapRules#DCA-MAP-013"
status: informational
rule_set: contextmap
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/ContextMapRules.java
tags: [contextmap, archunit]
---

## Selection

Every @Upstream, @ExternalUpstream and @Partnership declaration on the package-info of every package carrying @BoundedContext, reading context() or name(), translation(), and via() or interaction().

## Check

Informational - prints every declared edge to standard output and never fails; it carries no assertion. status() is not printed, so a PLANNED edge is listed like an implemented one.

## .NET reading

**Selection.** Every [Upstream], [ExternalUpstream] and [Partnership] declaration on the marker class of every namespace carrying [BoundedContext], reading Context or Name, Translation, and Via or Interaction.

**Check.** Informational - prints every declared edge to standard output and never fails; it carries no assertion. Status is not printed, so a Planned edge is listed like an implemented one.

## Implementation

```java
DcaRule.check(
        "DCA-MAP-013",
        "Diagnostic: Display declared context map",
        "Printing the declared edges makes the executable context map reviewable at a glance",
        arch -> {
          System.out.println("=== Context Map (declared) ===");
          for (String pkg : arch.boundedContextPackages()) {
            String source = arch.contextName(pkg);
            for (Upstream u : arch.packageAnnotations(pkg, Upstream.class)) {
              for (Upstream.Consumes channel : u.via()) {
                System.out.println(
                    "  "
                        + source
                        + " --["
                        + u.translation()
                        + " / "
                        + channelName(arch, channel)
                        + "]--> "
                        + u.context());
              }
            }
            for (ExternalUpstream e : arch.packageAnnotations(pkg, ExternalUpstream.class)) {
              System.out.println(
                  "  "
                      + source
                      + " --["
                      + e.translation()
                      + " / "
                      + e.interaction()
                      + "]--> (external) "
                      + e.name());
            }
            for (Partnership p : arch.packageAnnotations(pkg, Partnership.class)) {
              System.out.println("  " + source + " <--[PARTNERSHIP]--> " + p.context());
            }
          }
          System.out.println("==============================");
        })
    .selecting(
        "Every @Upstream, @ExternalUpstream and @Partnership declaration on the"
            + " package-info of every package carrying @BoundedContext, reading context()"
            + " or name(), translation(), and via() or interaction().")
    .checking(
        "Informational - prints every declared edge to standard output and never"
            + " fails; it carries no assertion. status() is not printed, so a PLANNED edge"
            + " is listed like an implemented one.")
```

## Helpers

### `channelName`

```java
private static String channelName(DcaArchitecture arch, Upstream.Consumes channel) {
  return arch.layout().channelSubpackage(channel);
}
```

### `name`

```java
public String name() {
  return "contextmap";
}
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `boundedContextPackages()`, `contextName()`, `layout()`, `packageAnnotations()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [@ExternalUpstream](/marker/strategic/externalupstream.md)
- [@Partnership](/marker/strategic/partnership.md)
- [@Upstream](/marker/strategic/upstream.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
