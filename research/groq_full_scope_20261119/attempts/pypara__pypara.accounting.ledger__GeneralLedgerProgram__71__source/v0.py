import datetime
import pytest
from pypara.accounting.ledger import GeneralLedgerProgram
from pypara.commons.zeitgeist import DateRange
from pypara.commons.numbers import Amount, Quantity
from pypara.accounting.generic import Balance
from pypara.accounting.journaling import JournalEntry, Posting, ReadJournalEntries
from pypara.accounting.accounts import Account
from pypara.accounting.ledger import GeneralLedger  # type: ignore

def test_general_ledger_program_is_protocol():
    """GeneralLedgerProgram should be a typing.Protocol subclass."""
    import typing
    assert issubclass(GeneralLedgerProgram, typing.Protocol), (
        "GeneralLedgerProgram must inherit from typing.Protocol"
    )

def test_general_ledger_program_instantiation_raises():
    """Attempting to instantiate a Protocol directly should raise TypeError."""
    with pytest.raises(TypeError):
        GeneralLedgerProgram()

def test_implementing_class_is_instance_of_protocol():
    """A class that implements the Protocol should be recognized as an instance."""
    class DummyProgram:
        def __call__(self, period: DateRange) -> GeneralLedger:
            # Return a minimal dummy GeneralLedger instance
            return GeneralLedger(period)

    dummy = DummyProgram()
    # Protocols support isinstance checks for structural compatibility
    assert isinstance(dummy, GeneralLedgerProgram), (
        "DummyProgram should be considered an instance of GeneralLedgerProgram"
    )
    # Verify that calling the dummy returns a GeneralLedger instance
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    result = dummy(period)
    assert isinstance(result, GeneralLedger), (
        "Result of DummyProgram.__call__ should be a GeneralLedger instance"
    )
