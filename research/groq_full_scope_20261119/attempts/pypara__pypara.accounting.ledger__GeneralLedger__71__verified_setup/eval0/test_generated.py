import datetime
import pytest
from pypara.accounting.ledger import GeneralLedger
from pypara.commons.zeitgeist import DateRange
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.accounting.ledger import Ledger

def test_general_ledger_initialization(tmp_path):
    # Create a simple date range for the accounting period
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 12, 31)
    period = DateRange(start, end)

    # Create a dummy account and ledger
    acc = Account(name="Cash")
    bal = Balance(amount=0)
    ledger = Ledger(account=acc, balance=bal)

    # Initialize the general ledger with the period and a single ledger
    gl = GeneralLedger(period=period, ledgers={acc: ledger})

    # Assertions: attributes are stored correctly
    assert gl.period is period
    assert isinstance(gl.ledgers, dict)
    assert acc in gl.ledgers
    assert gl.ledgers[acc] is ledger

def test_general_ledger_with_multiple_ledgers(tmp_path):
    period = DateRange(datetime.date(2024, 1, 1), datetime.date(2024, 12, 31))

    # Create multiple accounts and ledgers
    acc1 = Account(name="Revenue")
    acc2 = Account(name="Expense")
    ledger1 = Ledger(account=acc1, balance=Balance(amount=100))
    ledger2 = Ledger(account=acc2, balance=Balance(amount=50))

    gl = GeneralLedger(period=period, ledgers={acc1: ledger1, acc2: ledger2})

    # Verify that all ledgers are present and correctly mapped
    assert len(gl.ledgers) == 2
    assert gl.ledgers[acc1] is ledger1
    assert gl.ledgers[acc2] is ledger2

def test_general_ledger_invalid_ledgers_type(tmp_path):
    period = DateRange(datetime.date(2025, 1, 1), datetime.date(2025, 12, 31))

    # Pass a non-dict type for ledgers to trigger a TypeError
    with pytest.raises(TypeError):
        GeneralLedger(period=period, ledgers=[("not", "a", "dict")])
