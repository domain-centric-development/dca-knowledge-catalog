---
type: Pitfall
title: "Cookies that do not travel together: a request that arrives half-authenticated"
tags: [pitfall, adapter, security]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/jwt-implementation-guide/7-cookie-requirements.md, /guide/jwt-implementation-guide/7a-framing-a-second-question-not-a-consequence-of-the-first.md, /guide/jwt-implementation-guide/8-csrf-protection.md]
---

One request needs two cookies: the one that says who the caller is, and the one that carries the form token proving the request was intended. They are configured in two different places — the application sets the first, the framework writes the second — and only one of them was given a policy. The pair then behaves identically until the day the request comes from somewhere unusual: an iframe, a redirect from another site, a page served over a different scheme. There the browser applies each cookie's own rule, one arrives and the other does not, and the request is refused for a reason that names neither.

The symptom is misleading. Nothing reports "a cookie was withheld". The server sees a request without a token and answers as it must — *missing token*, not *forbidden* — so the trail leads to form handling, to the template, to the token generator, to anywhere but the cookie attribute that actually decided it.

## Why it happens

- **The framework writes the second cookie, so nobody configures it.** A CSRF or antiforgery cookie is created by the security framework with a default of its own. That default is not derived from the application's other cookies and differs between stacks — no `SameSite` attribute at all in one, `Strict` in another. Two implementations of the same design therefore behave differently at the edge while both look correct in review.
- **The policies are written far apart.** The identity cookie is built where the adapter issues a token; the token cookie is a line in a security configuration. Nothing puts the two next to each other, so nothing shows that they disagree.
- **Defaults are invisible in a diff.** A cookie that is never mentioned has no wrong line to spot. The gap survives every review that reads what is written rather than what is emitted.

## How it shows up

- A form works on the application's own pages and fails from every embedding, with a token error.
- A flow works over one scheme and fails over the other, because one cookie is marked `Secure` and the other is not.
- Two ports of the same host behave differently from two different domains, and nobody can say why — the first pair is the same site, the second is not.
- A twin implementation in another stack passes the same manual test and fails the same automated one, or the reverse.

## Do instead

- **Give every cookie of one exchange the same policy, from one place.** The token cookie takes its `SameSite` and `Secure` from the same configuration as the identity cookie it protects, rather than from the framework's default. Where the framework offers a customiser for its own cookie, that is what it is for.
- **List every cookie the application emits, the framework's included.** A cookie contract that names only the ones written by hand is the gap in documented form.
- **Assert the attributes on the wire, not in the configuration.** Read the `Set-Cookie` headers of a real response in a test. Mock request layers commonly keep a cookie as an object and drop `SameSite` on the way out, so a test at that level can pass while the browser sees something else.
- **Keep unrelated switches unrelated.** Whether another page may frame the application is an *origin* question, where the port counts; whether cookies travel there is a *site* question, where it does not. Deriving one from the other produces a setting that is either too weak or unusable — see the framing section of the guide.

## Anchors

- Guide: [Cookie requirements](/guide/jwt-implementation-guide/7-cookie-requirements.md) · [Framing: a second question](/guide/jwt-implementation-guide/7a-framing-a-second-question-not-a-consequence-of-the-first.md) · [CSRF protection](/guide/jwt-implementation-guide/8-csrf-protection.md)
- Related pitfalls: [Authorization in the domain layer](/pitfall/authorization-in-domain-layer.md)
