---
type: Section
title: Data-Test Attributes
chapter: E2E Testing for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/e2e-testing.md
tags: [guide, section]
---

### The Problem

Brittle selectors couple tests to UI implementation details:

```java
// ❌ BAD: Breaks on text/CSS changes
page.locator("button:has-text('Add to Cart')").click();
page.locator(".product-card").first().click();
page.locator("a:has-text('View Details')").click();
```

### The Solution

Use `data-test` attributes to create a stable test contract:

```html
<!-- Template -->
<button data-test="product-add-to-cart-button">Add to Cart</button>
<a href="/products/1" data-test="product-view-details-link">View Details</a>
```

```java
// ✅ GOOD: Stable selectors
page.locator("[data-test='product-add-to-cart-button']").click();
page.locator("[data-test='product-view-details-link']").first().click();
```

### Naming Convention

Pattern: `{context}-{element}-{action}` (kebab-case)

| Element Type | Pattern | Example |
|--------------|---------|---------|
| Buttons | `{context}-{action}-button` | `product-add-to-cart-button` |
| Links | `{context}-{target}-link` | `cart-checkout-link` |
| Inputs | `{context}-{field}-input` | `buyer-email-input` |
| Containers | `{context}-{name}-container` | `product-card-container` |
| Forms | `{context}-{name}-form` | `buyer-info-form` |

### Examples by Feature

**Product Catalog:**
- `product-card-container`
- `product-view-details-link`
- `product-add-to-cart-button`
- `product-detail-container`

**Shopping Cart:**
- `cart-item-container`
- `cart-checkout-link`
- `cart-remove-item-button`

**Checkout:**
- `buyer-email-input`
- `buyer-continue-button`
- `checkout-place-order-button`
- `confirmation-message`

### Template Integration

```html
<!-- Before -->
<div class="product-card">
  <a href="/products/1">View Details</a>
  <button>Add to Cart</button>
</div>

<!-- After -->
<div class="product-card" data-test="product-card-container">
  <a href="/products/1" data-test="product-view-details-link">View Details</a>
  <button data-test="product-add-to-cart-button">Add to Cart</button>
</div>
```

---
