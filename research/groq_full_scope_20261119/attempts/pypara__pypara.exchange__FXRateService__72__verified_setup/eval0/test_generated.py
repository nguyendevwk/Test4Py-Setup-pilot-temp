import pytest
from decimal import Decimal
from pypara.exchange import FXRateService
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

# Test 1: Instantiating the abstract base class should raise a TypeError
def test_fxrate_service_abstract_instantiation():
    with pytest.raises(TypeError):
        FXRateService()

# Test 2: The default attribute should be None initially
def test_fxrate_service_default_initial_value():
    assert FXRateService.default is None

# Test 3: A minimal concrete implementation should work and return None for unknown rates
class DummyFXRateService(FXRateService):
    def query(self, ccy1: Currency, ccy2: Currency, asof: Date, strict: bool = False) -> Decimal | None:
        return None

    def queries(self, queries: Iterable[tuple[Currency, Currency, Date]], strict: bool = False) -> Iterable[Decimal | None]:
        return (None for _ in queries)

def test_dummy_fxrate_service_query_and_queries():
    service = DummyFXRateService()
    # Use arbitrary currencies and a date
    ccy1 = Currency("USD")
    ccy2 = Currency("EUR")
    asof = Date(2023, 1, 1)
    # query should return None
    assert service.query(ccy1, ccy2, asof) is None
    # queries should return an iterable of Nones
    queries = [(ccy1, ccy2, asof), (ccy2, ccy1, asof)]
    results = list(service.queries(queries))
    assert results == [None, None]
