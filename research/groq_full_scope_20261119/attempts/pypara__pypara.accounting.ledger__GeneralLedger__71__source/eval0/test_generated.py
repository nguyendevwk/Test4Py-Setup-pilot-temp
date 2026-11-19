import pytest
from pypara.accounting.ledger import GeneralLedger
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Ledger
from pypara.commons.zeitgeist import DateRange
from datetime import date

def test_general_ledger_initialization(tmp_path):
    # Create a simple date range for the period
    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))
    # Instantiate a GeneralLedger with a dummy type parameter
    gl = GeneralLedger[float](period=period, ledgers={})
    # Assert that the period attribute is set correctly
    assert gl.period.start == date(2023, 1, 1)
    assert gl.period.end == date(2023, 12, 31)
    # Assert that ledgers is an empty dict initially
    assert isinstance(gl.ledgers, dict)
    assert len(gl.ledgers) == 0

def test_general_ledger_add_account(tmp_path):
    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))
    gl = GeneralLedger[float](period=period, ledgers={})
    # Create a dummy account and ledger
    acc = Account(name="Cash")
    ledger = Ledger[float]()
    # Add the account to the ledger
    gl.ledgers[acc] = ledger
    # Assert that the account is present in the ledgers dict
    assert acc in gl.ledgers
    assert gl.ledgers[acc] is ledger

def test_general_ledger_invalid_period_type():
    # Passing an invalid period type should raise a TypeError
    with pytest.raises(TypeError):
        GeneralLedger(period="not a DateRange", ledgers={})
