---
type: Section
title: Anti-Patterns
chapter: E2E Testing for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/e2e-testing.md
tags: [guide, section]
---

### ❌ Brittle Selectors
```java
// ❌ BAD: Coupled to text and CSS
page.locator("button:has-text('Add to Cart')").click();
page.locator(".btn-primary").click();
```

### ❌ Assertions in Page Objects
```java
// ❌ BAD: Page object making assertions
public class CartPage extends BasePage {
    public void verifyItemCount(int expected) {
        assertEquals(expected, getItemCount()); // Don't!
    }
}

// ✅ GOOD: Return data, let tests assert
public class CartPage extends BasePage {
    public int getItemCount() {
        return page.locator("[data-test='cart-item']").count();
    }
}
```

### ❌ Hardcoded Waits
```java
// ❌ BAD: Arbitrary delay
Thread.sleep(2000);

// ✅ GOOD: Wait for condition
page.waitForURL(BASE_URL + "/checkout/buyer");
waitFor("buyer-info-form");
```

### ❌ Testing Everything with E2E
```java
// ❌ BAD: Testing validation logic with E2E
@Test
void shouldRejectInvalidEmailFormat() { ... }

// ✅ GOOD: Test validation in unit tests, E2E for happy paths
```

### ❌ Duplicate Selectors
```java
// ❌ BAD: Selectors scattered across tests
page.locator("[data-test='product-add-to-cart-button']").click();
// ... later in another test
page.locator("[data-test='product-add-to-cart-button']").click();

// ✅ GOOD: Centralized in page object
public class ProductDetailPage extends BasePage {
    private static final String ADD_TO_CART_BUTTON = "product-add-to-cart-button";

    public void addToCart() {
        click(ADD_TO_CART_BUTTON);
    }
}
```

---
