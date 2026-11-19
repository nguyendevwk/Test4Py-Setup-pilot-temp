import pytest
from datetime import date
from decimal import Decimal
from pypara.accounting.ledger import GeneralLedger
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Balance
from pypara.commons.zeitgeist import DateRange

def test_general_ledger_initialization(tmp_path):
    # Create a simple period and ledger mapping
    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))
    account = Account(name="Cash")
    ledger = Balance(amount=Decimal("100.00"))
    gl = GeneralLedger(period=period, ledgers={account: ledger})
    assert gl.period.start == date(2023, 1, 1)
    assert gl.period.end == date(2023, 12, 31)
    assert gl.ledgers[account].amount == Decimal("100.00")

def test_general_ledger_missing_account(tmp_path):
    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))
    gl = GeneralLedger(period=period, ledgers={})
    account = Account(name="Revenue")
    with pytest.raises(KeyError):
        _ = gl.ledgers[account]

def test_general_ledger_balance_update(tmp_path):
    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))
    account = Account(name="Expense")
    ledger = Balance(amount=Decimal("50.00"))
    gl = GeneralLedger(period=period, ledgers={account: ledger})
    # Update balance
    gl.ledgers[account].amount += Decimal("25.00")
    assert gl.ledgers[account].amount == Decimal("75.00")
