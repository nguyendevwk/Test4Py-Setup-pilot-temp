import pytest
from datetime import date
from pypara.accounting.ledger import GeneralLedger
from pypara.commons.zeitgeist import DateRange
from pypara.accounting.accounts import Account
from pypara.accounting.generic import Ledger

def test_general_ledger_initialization(tmp_path):
    """GeneralLedger should store the period and ledgers dict correctly."""
    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))
    acc = Account(name="Cash")
    ledger = Ledger[float]()
    gl = GeneralLedger(period=period, ledgers={acc: ledger})
    assert gl.period is period
    assert gl.ledgers == {acc: ledger}
    assert isinstance(gl.ledgers[acc], Ledger)

def test_general_ledger_missing_period_raises():
    """Providing None for period should raise a TypeError due to type mismatch."""
    acc = Account(name="Revenue")
    ledger = Ledger[float]()
    with pytest.raises(TypeError):
        GeneralLedger(period=None, ledgers={acc: ledger})  # type: ignore[arg-type]

def test_general_ledger_invalid_ledger_type():
    """Ledger values must be Ledger instances; passing wrong type raises TypeError."""
    period = DateRange(start=date(2023, 1, 1), end=date(2023, 12, 31))
    acc = Account(name="Expense")
    with pytest.raises(TypeError):
        GeneralLedger(period=period, ledgers={acc: "not a ledger"})  # type: ignore[arg-type]
