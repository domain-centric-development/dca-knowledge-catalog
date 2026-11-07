---
type: Reference
title: "Diagnostic: incoming adapters that read the caller's roles in their own code — Overview"
tags: [reference]
evidence_for: /rule/hexagonal/dca-hex-020.md
---

[Full node and context](/rule/hexagonal/dca-hex-020.md). This is an evidence excerpt; retain the parent selection and caveats.

# Diagnostic: incoming adapters that read the caller's roles in their own code

**Experimental.** This rule is binding only in a project that opted in to experimental rules - the architecture test calls `withExperimental()` (.NET: `WithExperimental()`) on its rule selection, or `dca-archunit.properties` sets `dca.rules.experimental = true`; without that opt-in the rule does not run and is information only, never a finding and never a reason to change code.

## Selection

Classes in the incoming adapter layer of every module root - by default <module>.adapter.incoming.. - and their method calls, lambdas and nested classes included. Nothing is selected when the configured authorization-annotation role is empty: without a declarative form there is nothing to advise.

## Check

Informational diagnostic only: lists every call of a method whose name asks whether the caller holds a role or an authority - isUserInRole, isInRole, hasRole, hasAnyRole, hasAuthority, hasAnyAuthority - on any owner, and never fails. An expression inside the authorization annotation is a string, not a call, and is not listed. A method that only hands the roles over - roles(), getAuthorities() - is not listed, so an adapter that issues a token or builds the caller's principal passes; for the same reason a role compared by the adapter itself - roles().contains("STAFF") - is not seen, nor is a helper of the project's own - isAdmin(), isStaff() - declared outside the incoming adapter.

## .NET reading

**Selection.** Non-nested types in the incoming adapter layer of every module root - by default <Module>.Adapter.Incoming - with their runtime type in the loaded assemblies, together with their nested, async state-machine and closure types, and the calls their IL makes. Nothing is selected when the configured authorization-attribute role is empty: without a declarative form there is nothing to advise.

**Check.** Informational diagnostic only: lists every call of a method whose name asks whether the caller holds a role or an authority - IsInRole, IsUserInRole, HasRole, HasAnyRole, HasAuthority, HasAnyAuthority, compared ignoring case - on any declaring type, and never fails. A policy or role named in the authorization attribute is metadata, not a call, and is not listed. A member that only hands the roles over is not listed, so an adapter that issues a token or builds the caller's principal passes; for the same reason a role compared by the adapter itself - a claim of the role type searched with FindAll or HasClaim - is not seen, nor is a helper of the project's own - IsAdmin(), IsStaff() - declared outside the incoming adapter.

## Rust reading

Unpublished (dca-rust); the suite implements it. **Held by** a lint or a test (source-test).

**Selection.** Functions and methods in the incoming module of every adapters crate, and the router expressions of those crates. Nothing is selected when [workspace.metadata.dca] names neither authorization-extractors (types whose presence in a handler's signature declares a claims-only check, such as a RequireRole<R> extractor) nor authorization-layers (functions whose call in a router's .layer(...) or .route_layer(...) declares it for the routes added before it); both are empty by default.

**Check.** Informational - lists every call in a body, as a method or as a path, named has_role, has_any_role, has_authority, has_any_authority, is_in_role or is_user_in_role, and never fails. A function whose signature names a configured extractor, or whose name appears in the receiver of a .layer(...)/.route_layer(...) call that calls a configured layer function within the same crate, is not listed. Not seen: a handler routed behind a layer in a router another crate builds, a role compared by the handler itself (roles.contains(...)), and a helper of the project's own declared outside the incoming module. Rust has no route annotation; the extractor and the layer are its declarative forms.

## Implementation

```java
DcaRule.informational(
        "DCA-HEX-020",
        "Diagnostic: incoming adapters that read the caller's roles in their own code",
        "A check that reads nothing but the caller's roles or claims - is this caller staff? -"
            + " is a property of the exposure and is declared on the route, with the"
            + " framework's authorization annotation, where a reader of the route sees it and"
            + " the framework answers an unauthenticated and an unauthorized caller apart. A"
            + " branch on the caller's roles inside the adapter's code hides the gate and"
            + " renders whatever status the branch writes. A check that needs the stored data -"
            + " is this yours? - is not claims-only and belongs to the use case",
        arch -> {
          if (layout.frameworkAnnotations().authorizationAnnotation().isEmpty()) {
            return List.of();
          }
          java.util.Set<String> observed = new java.util.TreeSet<>();
          for (JavaClass adapter : arch.classes()) {
            if (!arch.inIncomingAdapter().test(adapter)) {
              continue;
            }
            for (JavaMethodCall call : adapter.getMethodCallsFromSelf()) {
              if (call.getOrigin().getName().equals("$deserializeLambda$")
                  || !ROLE_ACCESSOR.matcher(call.getName()).matches()) {
                continue;
              }
              observed.add(
                  call.getOrigin().getFullName()
                      + " reads the caller's roles through "
                      + call.getTargetOwner().getSimpleName()
                      + "."
                      + call.getName()
                      + "() - declare a claims-only check on the route with "
                      + String.join(
                          " or ",
                          layout.frameworkAnnotations().authorizationAnnotation().stream()
                              .map(a -> "@" + a.substring(a.lastIndexOf('.') + 1))
                              .toList())
                      + "; a check that needs the stored data belongs to the use case");
            }
          }
          return new ArrayList<>(observed);
        })
    .experimental()
    .selecting(
        "Classes in the incoming adapter layer of every module root - by default"
            + " <module>.adapter.incoming.. - and their method calls, lambdas and nested"
            + " classes included. Nothing is selected when the configured"
            + " authorization-annotation role is empty: without a declarative form there is"
            + " nothing to advise.")
    .checking(
        "Informational diagnostic only: lists every call of a method whose name asks"
            + " whether the caller holds a role or an authority - isUserInRole, isInRole,"
            + " hasRole, hasAnyRole, hasAuthority, hasAnyAuthority - on any owner, and never"
            + " fails. An expression inside the authorization annotation is a string, not a"
            + " call, and is not listed. A method that only hands the roles over - roles(),"
            + " getAuthorities() - is not listed, so an adapter that issues a token or builds"
            + " the caller's principal passes; for the same reason a role compared by the"
            + " adapter itself - roles().contains(\"STAFF\") - is not seen, nor is a helper of"
            + " the project's own - isAdmin(), isStaff() - declared outside the incoming"
            + " adapter.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `classes()`, `inIncomingAdapter()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
