---
type: Pitfall
title: State-changing GET endpoint
tags: [pitfall, adapter, rest, security, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules.md, /guide/jwt-implementation-guide/8-csrf-protection.md, /marker/port-in/usecase.md]
---

A `@GetMapping` (or an HTTP GET action) that executes a command use case: a "Proceed to checkout" **link** to `/checkout/start?cartId=…` that creates a checkout session, a `GET /orders/{id}/cancel`, a logout link. Convenient — one `href` instead of a form — and wrong in three independent ways.

## Why it is wrong

- GET is defined as safe: browsers prefetch it, link previews and crawlers follow it, a bookmark or a page reload repeats it. Every one of those *changes state* on the user's behalf.
- No CSRF protection can cover it: a token travels in a form field or header, and a GET link carries neither. Any page on the web can embed `<img src="https://shop/checkout/start?cartId=…">` and the browser fires it with the user's cookies.
- The incoming adapter's job is to translate protocol semantics into a command; choosing GET for a command mistranslates the protocol.

## What forbids it

- [Layer rules](/guide/rules.md) — input adapter rules: a state-changing use case is reached only by an unsafe method (`POST`, `PUT`, `DELETE`); links never create sessions, carts or orders.

## Do instead

A form with `method="post"`, the identifier as a hidden field and the CSRF token, rendered as a button styled like a link if the design wants it. The handler is `@PostMapping` and redirects afterwards (POST → redirect → GET). Keep `GET` for queries only; if a handler with `@GetMapping` depends on a `*Command`-taking input port, that is the review signal.

- Related pitfall: [CSRF-exempt API that accepts cookie authentication](/pitfall/csrf-exempt-api-that-accepts-cookies.md)

## Anchors

- Guide: [Layer rules](/guide/rules.md) · [CSRF protection](/guide/jwt-implementation-guide/8-csrf-protection.md)
- Markers: [UseCase](/marker/port-in/usecase.md)
