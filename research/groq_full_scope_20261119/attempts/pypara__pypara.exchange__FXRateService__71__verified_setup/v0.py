import pytest
from decimal import Decimal
from pypara.exchange import FXRateService
from pypara.exchange.commons.zeitgeist import Date
from pypara.exchange.currencies import Currency

# Test that the default service is set and is an instance of FXRateService
def test_default_service_exists():
    assert FXRateService.default is not None
    assert isinstance(FXRateService.default, FXRateService)

# Test that querying a known currency pair returns a Decimal
def test_query_known_pair_returns_decimal(tmp_path):
    # Use a date that is likely to have data; adjust if needed
    asof = Date(2023, 1, 1)
    rate = FXRateService.default.query(Currency('USD'), Currency('EUR'), asof)
    assert isinstance(rate, Decimal)
    # The rate should be positive
    assert rate > Decimal('0')

# Test that querying an unknown pair returns None and raises LookupError when strict=True
def test_query_unknown_pair_behavior(tmp_path):
    asof = Date(2023, 1, 1)
    # Use a pair that is unlikely to exist
    unknown_rate = FXRateService.default.query(Currency('AAA'), Currency('BBB'), asof)
    assert unknown_rate is None
    with pytest.raises(LookupError):
        FXRateService.default.query(Currency('AAA'), Currency('BBB'), asof, strict=True)
