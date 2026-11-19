import inspect
import types
import pytest
from pypara.accounting.ledger import ReadInitialBalances
from pypara.commons.zeitgeist import DateRange

def test_read_initial_balances_protocol_defined():
    """The ReadInitialBalances protocol should be defined in the ledger module."""
    assert hasattr(ReadInitialBalances, "__call__"), "Protocol must define __call__"
    assert inspect.isfunction(ReadInitialBalances.__call__), "__call__ should be a function"

def test_read_initial_balances_signature():
    """The protocol's __call__ should accept a single DateRange argument and return InitialBalances."""
    sig = inspect.signature(ReadInitialBalances.__call__)
    params = list(sig.parameters.values())
    assert len(params) == 1, "Protocol __call__ should have exactly one parameter"
    param = params[0]
    assert param.annotation is DateRange, f"Parameter annotation should be DateRange, got {param.annotation}"
    assert sig.return_annotation is not inspect.Signature.empty, "Return annotation should be defined"

def test_protocol_callable_with_incorrect_signature():
    """A function that does not match the protocol's signature should raise a TypeError when called via the protocol."""
    # Define a function that incorrectly accepts no arguments
    def bad_func():
        return None

    # Attempt to call it through the protocol's __call__ signature
    with pytest.raises(TypeError):
        ReadInitialBalances.__call__(bad_func, DateRange(start=None, end=None))
