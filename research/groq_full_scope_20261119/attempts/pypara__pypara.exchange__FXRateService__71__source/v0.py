import pytest
import inspect
from pypara.exchange import FXRateService
from decimal import Decimal

# Test 1: Instantiating the abstract base class should raise a TypeError
def test_fxrate_service_cannot_be_instantiated():
    with pytest.raises(TypeError):
        FXRateService()

# Test 2: The class is correctly marked as abstract
def test_fxrate_service_is_abstract():
    assert inspect.isabstract(FXRateService)

# Test 3: A concrete subclass must implement the abstract methods
def test_concrete_subclass_implements_methods(tmp_path):
    # Define a minimal concrete implementation
    class DummyFXRateService(FXRateService):
        def query(self, ccy1, ccy2, asof, strict=False):
            return Decimal("1.2345")

        def queries(self, queries, strict=False):
            return (self.query(*q) for q in queries)

    # Instantiate the concrete subclass
    service = DummyFXRateService()

    # Verify that the query method returns the expected Decimal
    result = service.query("USD", "EUR", "2023-01-01")
    assert isinstance(result, Decimal)
    assert result == Decimal("1.2345")

    # Verify that the queries method yields the same result for each input
    queries = [
        ("USD", "EUR", "2023-01-01"),
        ("GBP", "JPY", "2023-01-02"),
    ]
    results = list(service.queries(queries))
    assert results == [Decimal("1.2345"), Decimal("1.2345")]
