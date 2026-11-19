import pytest
import typing
from pypara.accounting.ledger import ReadInitialBalances
from pypara.accounting.zeitgeist import DateRange
from pypara.accounting.ledger import InitialBalances


def test_read_initial_balances_is_protocol():
    """The imported ReadInitialBalances should be a typing.Protocol subclass."""
    assert isinstance(ReadInitialBalances, type)
    assert issubclass(ReadInitialBalances, typing.Protocol)


def test_read_initial_balances_call_signature():
    """The __call__ method of the protocol should have the correct annotations."""
    # Retrieve the __call__ method from the protocol
    call_method = getattr(ReadInitialBalances, "__call__", None)
    assert call_method is not None, "__call__ method missing in ReadInitialBalances"

    # Get type hints for the __call__ method
    hints = typing.get_type_hints(call_method)
    # The first hint corresponds to the 'period' parameter
    period_type = hints.get("period")
    return_type = hints.get("return")

    assert period_type is DateRange, f"Expected period type DateRange, got {period_type}"
    assert return_type is InitialBalances, f"Expected return type InitialBalances, got {return_type}"


def test_protocol_can_be_subclassed_and_implemented():
    """A concrete class implementing the protocol should be accepted by isinstance checks."""
    class DummyImplementation(ReadInitialBalances):
        def __call__(self, period: DateRange) -> InitialBalances:
            return InitialBalances()

    dummy = DummyImplementation()
    # The instance should be considered an instance of the protocol
    assert isinstance(dummy, ReadInitialBalances)
    # Calling the instance should return an InitialBalances object
    result = dummy(DateRange())
    assert isinstance(result, InitialBalances)
