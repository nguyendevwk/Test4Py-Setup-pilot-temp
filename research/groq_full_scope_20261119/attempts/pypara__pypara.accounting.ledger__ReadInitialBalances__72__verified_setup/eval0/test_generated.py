import inspect
import pytest
from pypara.accounting.ledger import ReadInitialBalances
from pypara.commons.zeitgeist import DateRange
from datetime import datetime

def test_read_initial_balances_is_protocol():
    """The imported ReadInitialBalances should be a typing.Protocol."""
    assert isinstance(ReadInitialBalances, type)
    # Protocols are subclasses of typing.Protocol
    from typing import Protocol
    assert issubclass(ReadInitialBalances, Protocol)

def test_read_initial_balances_signature():
    """The protocol defines a __call__ method with a single DateRange argument."""
    # Retrieve the __call__ method from the Protocol
    call_method = getattr(ReadInitialBalances, "__call__", None)
    assert call_method is not None, "__call__ not defined on the protocol"
    sig = inspect.signature(call_method)
    params = list(sig.parameters.values())
    # Expect exactly one parameter named 'period' of type DateRange
    assert len(params) == 1
    param = params[0]
    assert param.name == "period"
    assert param.annotation is DateRange

def test_calling_protocol_raises_type_error():
    """Attempting to call the Protocol directly should raise a TypeError."""
    period = DateRange(datetime.now(), datetime.now())
    with pytest.raises(TypeError):
        ReadInitialBalances(period)
