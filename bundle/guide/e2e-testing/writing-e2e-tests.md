---
type: Section
title: Writing E2E Tests
chapter: E2E Testing for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/e2e-testing.md
tags: [guide, section]
---

### Complete Test Example

```java
@DisplayName("Guest Checkout E2E Tests")
class CheckoutGuestE2ETest extends BaseE2ETest {

    @Test
    @DisplayName("Complete checkout flow as guest user")
    void completeGuestCheckoutFlow() {
        // Step 1: Browse catalog and add product
        ProductCatalogPage catalog = ProductCatalogPage.navigateTo(page);
        ProductDetailPage detail = catalog.viewFirstProduct();
        detail.addToCart();

        // Step 2: Verify cart and start checkout
        CartPage cart = CartPage.navigateTo(page);
        assertTrue(cart.hasItems(), "Cart should have at least one item");

        // Step 3: Fill buyer information
        BuyerInfoPage buyer = cart.proceedToCheckout();
        DeliveryPage delivery = buyer
            .fillBuyerInfo("guest@example.com", "Test", "Guest", "+1-555-0100")
            .continueToDelivery();

        // Step 4: Fill delivery information
        PaymentPage payment = delivery
            .fillAddress("123 Main Street", "Springfield", "12345", "US", "IL")
            .selectFirstShippingOption()
            .continueToPayment();

        // Step 5: Select payment
        ReviewPage review = payment
            .selectFirstPaymentProvider()
            .continueToReview();

        // Step 6: Verify and place order
        assertTrue(review.showsEmail("guest@example.com"));
        ConfirmationPage confirmation = review.placeOrder();

        // Step 7: Verify confirmation
        assertTrue(confirmation.isOrderConfirmed());
    }
}
```

### Test Characteristics

- **Readable** - Tests read like user stories
- **Isolated** - Each test starts with fresh browser context
- **Focused** - One flow per test
- **Verifiable** - Clear assertions at key points

---
