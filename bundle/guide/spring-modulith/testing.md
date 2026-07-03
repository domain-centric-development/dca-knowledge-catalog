---
type: Section
title: Testing
chapter: Spring Modulith Implementation
source: guide
resource: implementing-domain-centric-architecture/spring-modulith.md
tags: [guide, section]
---

### Module Structure Verification

```java
@Modulith
class ModularityTests {

    ApplicationModules modules = ApplicationModules.of(EcommerceApplication.class);

    @Test
    void verifiesModularStructure() {
        modules.verify();
    }

    @Test
    void documentsModules() throws IOException {
        new Documenter(modules)
            .writeDocumentation()
            .writeIndividualModulesAsPlantUml();
    }
}
```

### Module Integration Tests

```java
@ApplicationModuleTest
class OrderModuleIntegrationTest {

    @Autowired
    OrderApi orderApi;

    @Autowired
    ScenarioCustomizer scenarioCustomizer;

    @Test
    void shouldPublishOrderCreatedEvent() {
        var request = new CreateOrderRequest(...);

        // Verify event was published
        scenarioCustomizer
            .scenario("order-creation")
            .stimulate(() -> orderApi.createOrder(request))
            .andWaitForEventOfType(OrderCreatedEvent.class)
            .matching(event -> event.orderId().equals("123"))
            .toArriveAndVerify(event ->
                assertThat(event.totalAmount()).isEqualTo(new BigDecimal("99.99"))
            );
    }
}
```
