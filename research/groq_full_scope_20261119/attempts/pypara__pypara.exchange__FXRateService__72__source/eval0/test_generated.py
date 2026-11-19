import pytest
from decimal import Decimal
from pypara.exchange import FXRateService
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

# 1. Ensure FXRateService is abstract and cannot be instantiated directly
def test_fx_rate_service_cannot_be_instantiated():
    with pytest.raises(TypeError):
        FXRateService()

# 2. Implement a minimal concrete subclass and test query returns a Decimal
class DummyFXRateService(FXRateService):
    def query(self, ccy1: Currency, ccy2: Currency, asof: Date, strict: bool = False) -> Decimal:
        return Decimal("1.23")

    def queries(self, queries, strict: bool = False):
        return (self.query(*q, strict=strict) for q in queries)

def test_dummy_fx_rate_service_query_returns_decimal():
    service = DummyFXRateService()
    rate = service.query(Currency("USD"), Currency("EUR"), Date(2023, 1, 1))
    assert isinstance(rate, Decimal)
    assert rate == Decimal("1.23")

# 3. Test that queries returns an iterable of the same length as input
def test_dummy_fx_rate_service_queries_length(tmp_path):
    service = DummyFXRateService()
    queries = [
        (Currency("USD"), Currency("EUR"), Date(2023, 1, 1)),
        (Currency("GBP"), Currency("JPY"), Date(2023, 2, 1)),
    ]
    results = list(service.queries(queries))
    assert len(results) == len(queries)
    assert all(isinstance(r, Decimal) for r in results)
    assert all(r == Decimal("1.23") for r in results)
