import datetime
import pytest
from pypara.dcc import dcc, DCCRegistry, DCC
from pypara.currencies import Currency

# Helper: a simple day count fraction calculator that returns a constant
def dummy_calculator(start: datetime.date, end: datetime.date, ref: datetime.date, freq: float = None) -> float:
    return 1.0

def test_dcc_registers_default():
    """Decorator registers a DCC with default parameters."""
    # Apply decorator
    decorated = dcc("ACT/360")(dummy_calculator)
    # The function should now have a __dcc attribute
    assert hasattr(decorated, "__dcc")
    dcc_obj = getattr(decorated, "__dcc")
    assert isinstance(dcc_obj, DCC)
    # The registry should contain the new DCC
    assert dcc_obj in DCCRegistry._registry  # type: ignore[attr-defined]

def test_dcc_registers_with_altnames_and_ccys():
    """Decorator registers a DCC with alternative names and currencies."""
    alt_names = {"Actual/360", "ACT/360"}
    # Use a real Currency instance
    usd = Currency("USD")
    ccys = {usd}
    decorated = dcc("ACT/360", altnames=alt_names, ccys=ccys)(dummy_calculator)
    dcc_obj = getattr(decorated, "__dcc")
    assert dcc_obj.name == "ACT/360"
    assert dcc_obj.altnames == alt_names
    assert dcc_obj.ccys == ccys
    assert dcc_obj in DCCRegistry._registry  # type: ignore[attr-defined]

def test_dcc_decorator_returns_original_function():
    """Decorator returns the original function unchanged."""
    decorated = dcc("ACT/360")(dummy_calculator)
    # The returned object should be the same callable as the original
    assert decorated is dummy_calculator
    # Calling the function should produce the expected constant result
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 12, 31)
    ref = datetime.date(2023, 1, 1)
    assert decorated(start, end, ref) == 1.0
