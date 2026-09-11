---
type: Section
title: Testing
chapter: Spring Modulith Implementation
source: guide
resource: dca-guide/topics/spring-modulith.md
tags: [guide, section]
---

### Module Structure Verification

Modulith's `ApplicationModules.verify()` is not an ArchUnit rule and needs `spring-modulith-core` at compile
time, so it ships in its own test artifact next to the rule catalog, `dev.domaincentric:dca-archunit-spring-modulith`.
Two base classes, two test classes, the same layout:

```kotlin
testImplementation("dev.domaincentric:dca-archunit:0.3.0")
testImplementation("dev.domaincentric:dca-archunit-spring-modulith:0.1.0")
```

```java
class ModulithTest extends DcaSpringModulithTest {
    @Override
    protected DcaLayout layout() {
        return DcaLayout.forBasePackage("com.company.project");
    }
}
```

The base class runs `verify()` and lists the discovered modules with their named interfaces. Its one piece
of knowledge is the test-class filter: architecture tests living directly in the base package would
otherwise become a synthetic *root module* that Modulith reports as depending on non-exposed types. The
filter matches the **full** class name, so inner and Groovy closure classes (`FooTest$1`,
`FooSpec$_check_closure1`) are excluded with their owner. `SpringModulithModules.of(layout)` returns the filtered
`ApplicationModules` for assertions of your own — the raw form, for reference:

```java
class ModularityTests {

    ApplicationModules modules = ApplicationModules.of("com.company.project", SpringModulithModules.testClasses());

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
