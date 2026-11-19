import inspect
import types
import pytest
from pypara.accounting.ledger import ReadInitialBalances, DateRange, InitialBalances


def test_read_initial_balances_protocol_exists():
    """The ReadInitialBalances protocol should be defined in the module."""
    assert hasattr(ReadInitialBalances, "__call__"), "Protocol must define __call__"
    assert isinstance(ReadInitialBalances, type), "ReadInitialBalances should be a class"
    # Ensure the protocol is a subclass of Protocol
    from typing import Protocol
    assert issubclass(ReadInitialBalances, Protocol), "ReadInitialBalances must inherit from Protocol"


def test_read_initial_balances_signature():
    """A function matching the ReadInitialBalances protocol should accept a DateRange and return InitialBalances."""
    # Define a dummy implementation that matches the protocol
    def dummy_impl(period: DateRange) -> InitialBalances:
        return InitialBalances()

    # Inspect the signature
    sig = inspect.signature(dummy_impl)
    params = sig.parameters
    assert len(params) == 1, "Protocol requires exactly one parameter"
    param = next(iter(params.values()))
    assert param.annotation is DateRange, "Parameter must be annotated as DateRange"
    assert sig.return_annotation is InitialBalances, "Return type must be InitialBalances"

    # Call the dummy implementation and verify the return type
    period = DateRange(start=None, end=None)  # using None for simplicity
    result = dummy_impl(period)
    assert isinstance(result, InitialBalances), "Returned object must be an InitialBalances instance"


def test_read_initial_balances_callable_behavior(tmp_path):
    """Ensure that a callable matching the protocol can be stored and invoked via the protocol type."""
    # Create a simple callable that records its input
    class Recorder:
        def __init__(self):
            self.called_with = None

        def __call__(self, period: DateRange) -> InitialBalances:
            self.called_with = period
            return InitialBalances()

    recorder = Recorder()
    # Assign to a variable typed as ReadInitialBalances
    typed_callable: ReadInitialBalances = recorder  # type: ignore
    period = DateRange(start=None, end=None)
    result = typed_callable(period)
    assert recorder.called_with is period, "Callable should receive the period argument"
    assert isinstance(result, InitialBalances), "Callable should return InitialBalances"
