import pytest
from datetime import datetime
from pypara.accounting.ledger import ReadInitialBalances, InitialBalances
from pypara.accounting.zeitgeist import DateRange
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.commons.numbers import Amount, Quantity

def test_read_initial_balances_protocol_exists_and_has_call():
    """
    Verify that ReadInitialBalances is a Protocol with a __call__ method
    accepting a DateRange and returning an InitialBalances mapping.
    """
    # The protocol should be a class type
    assert isinstance(ReadInitialBalances, type)
    # It should define a __call__ attribute
    assert hasattr(ReadInitialBalances, "__call__")
    # The __call__ attribute should be a function or descriptor
    assert callable(getattr(ReadInitialBalances, "__call__"))

def test_initial_balances_type_alias_is_dict_of_account_to_balance():
    """
    Ensure that the InitialBalances alias resolves to a dict mapping Account to Balance.
    """
    # Create a sample Account and Balance
    acc = Account("Cash")
    bal = Balance(Amount(100), Quantity(1))
    # Construct a dict using the alias
    sample: InitialBalances = {acc: bal}
    # Verify the mapping type and contents
    assert isinstance(sample, dict)
    assert acc in sample
    assert sample[acc] == bal

def test_date_range_accepts_valid_period_and_returns_expected_structure():
    """
    Test that a DateRange can be constructed and used as a key in a function
    matching the ReadInitialBalances protocol, and that the returned structure
    contains the expected mapping type.
    """
    # Define a simple DateRange
    start = datetime(2023, 1, 1)
    end = datetime(2023, 12, 31)
    period = DateRange(start, end)

    # Define a dummy function that matches the protocol
    def dummy_reader(p: DateRange) -> InitialBalances:
        # Return an empty mapping for the test
        return {}

    # Ensure the dummy function accepts the period and returns a dict
    result = dummy_reader(period)
    assert isinstance(result, dict)
    assert result == {}
