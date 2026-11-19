import datetime
import pytest
from pypara.accounting.ledger import GeneralLedgerProgram, GeneralLedger, DateRange

def test_general_ledger_program_returns_ledger(tmp_path):
    """Calling the program with a valid DateRange returns a GeneralLedger instance."""
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 12, 31)
    period = DateRange(start, end)
    ledger = GeneralLedgerProgram()(period)
    assert isinstance(ledger, GeneralLedger)
    assert ledger.period == period

def test_general_ledger_program_invalid_input():
    """Passing an invalid period type raises a TypeError."""
    with pytest.raises(TypeError):
        GeneralLedgerProgram()(None)

def test_general_ledger_program_period_consistency(tmp_path):
    """The returned ledger's period attribute matches the input period."""
    start = datetime.date(2024, 6, 1)
    end = datetime.date(2024, 6, 30)
    period = DateRange(start, end)
    ledger = GeneralLedgerProgram()(period)
    assert ledger.period.start == start
    assert ledger.period.end == end
