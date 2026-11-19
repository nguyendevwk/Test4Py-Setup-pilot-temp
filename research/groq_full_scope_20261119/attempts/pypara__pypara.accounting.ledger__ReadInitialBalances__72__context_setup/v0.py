import inspect
import typing
import datetime
import pytest

from pypara.accounting.ledger import ReadInitialBalances, InitialBalances
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.accounting.zeitgeist import DateRange


def test_initialbalances_origin_and_args():
    """
    Verify that the type alias `InitialBalances` is a dictionary mapping
    `Account` to `Balance` and that its origin and arguments are correct.
    """
    origin = typing.get_origin(InitialBalances)
    args = typing.get_args(InitialBalances)
    assert origin is dict, f"Expected origin dict, got {origin}"
    assert args == (Account, Balance), f"Expected args (Account, Balance), got {args}"


def test_readinitialbalances_signature():
    """
    Verify that the protocol `ReadInitialBalances` defines a __call__ method
    accepting a single `DateRange` argument and returning an `InitialBalances`.
    """
    # Retrieve the __call__ method from the protocol
    call_method = getattr(ReadInitialBalances, "__call__", None)
    assert call_method is not None, "__call__ not defined on ReadInitialBalances"

    # Inspect the signature
    sig = inspect.signature(call_method)
    params = sig.parameters
    assert len(params) == 2, f"Expected 2 parameters (self, period), got {len(params)}"
    period_param = params["period"]
    assert period_param.annotation is DateRange, (
        f"Expected period annotation DateRange, got {period_param.annotation}"
    )
    assert sig.return_annotation is InitialBalances, (
        f"Expected return annotation InitialBalances, got {sig.return_annotation}"
    )


def test_dummy_implementation_of_readinitialbalances(tmp_path):
    """
    Create a dummy function that satisfies the `ReadInitialBalances` protocol,
    invoke it with a sample `DateRange`, and assert that the returned value
    is an `InitialBalances` instance with expected contents.
    """
    # Create a minimal Account and Balance instance
    acct = Account(name="Cash")
    bal = Balance(amount=100, currency="USD")

    # Define a dummy implementation
    def dummy_reader(period: DateRange) -> InitialBalances:
        # The period is not used in this dummy implementation
        return {acct: bal}

    # Ensure the dummy function conforms to the protocol
    assert isinstance(dummy_reader, ReadInitialBalances.__class__), (
        "Dummy reader does not conform to ReadInitialBalances protocol"
    )

    # Create a sample DateRange
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 12, 31)
    period = DateRange(start=start, end=end)

    # Call the dummy reader and verify the result
    result = dummy_reader(period)
    assert isinstance(result, dict), "Result should be a dict"
    assert acct in result, "Account key missing in result"
    assert result[acct] == bal, "Balance value does not match expected"
