---
type: Pitfall
title: "State kept in one instance: the next request reaches another"
tags: [pitfall, adapter, infrastructure, security]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/adapter-layer-rules.md, /guide/jwt-implementation-guide/8-csrf-protection.md]
---

A request leaves something behind for the request after it: a message for the page after a redirect, a half-filled form, the step a visitor came from. The adapter puts it where the framework makes it easiest — the server session, a flash attribute, `TempData` — and every test passes, because every test runs against one instance. Then the application runs as several instances behind a load balancer without sticky sessions. The POST lands on one, the redirected GET on another, and the message is gone, or the form starts empty, or the request is refused.

Nothing reports it. The second instance does not know that something was expected, so it renders the page as if nothing had happened. The symptom is a notice that appears on some clicks and not on others, which reads like a template bug and is a deployment fact.

## Why it happens

- **The convenient place is local.** A server session and a flash attribute live in the memory of the instance that wrote them (Spring MVC keeps flash attributes in the session). `TempData` in ASP.NET Core travels in a cookie by default, but that cookie is protected with a key ring: an instance with a key ring of its own cannot read what another one wrote, and the same holds for the authentication and antiforgery cookies.
- **One instance hides it.** Locally, in the test suite and on a single container the next request always comes back to the same process. The defect needs a second instance to show, and the first one to have it is production.
- **Two stacks differ by default.** The same design behaves differently: one framework loses the message without a second instance's session, the other loses it only without a shared key ring. Two implementations of one story each look correct, and fail at different places.

## How it shows up

- A confirmation after a redirect appears in development and only sometimes in production.
- Scaling from one instance to two breaks a flow that no code change touched.
- A cookie written by one instance is rejected by the next as unreadable, and the visitor is logged out or the form is refused.
- Turning on sticky sessions "fixes" it, and the next deployment that drains an instance brings it back.

## Do instead

- **Carry it in the request.** A message for the next page is a fixed code in the redirect URL (`?notice=saved`), never the sentence. The page maps the code through an enum of the incoming adapter — one value per notice, with its code and its text or message key — and ignores a code it does not know. The code names *which* notice, never data: a person can bookmark or edit the URL.
- **Or keep it in a store every instance reads.** State that does not fit a URL — a draft, a multi-step form — goes into the database or a shared cache, behind the same port as any other state, not into the session of one process.
- **Share what protects the cookies.** Where the framework encrypts or signs cookies with keys of its own (ASP.NET Core's data protection), every instance uses the same key ring, persisted where all of them read it. A stateless token chain needs no session at all; keep it that way.
- **Write the runtime down.** The project's technical description says whether the application runs as several instances and without sticky sessions. Then the choice above is a consequence, not a discovery.
- **Test it with two instances.** One end-user test that sends the POST to one instance and the GET to another is the only test that sees this defect.

## Anchors

- Guide: [Adapter layer rules](/guide/rules/adapter-layer-rules.md) — input adapter rules, state across requests · [CSRF protection](/guide/jwt-implementation-guide/8-csrf-protection.md) — the token strategy that needs no server-side session
- Template: [Page controller](/template/page-controller.md) — the notice as a code in the redirect
- Related pitfalls: [Cookies that do not travel together](/pitfall/cookies-that-do-not-travel-together.md) · [State-changing GET endpoint](/pitfall/state-changing-get-endpoint.md)
