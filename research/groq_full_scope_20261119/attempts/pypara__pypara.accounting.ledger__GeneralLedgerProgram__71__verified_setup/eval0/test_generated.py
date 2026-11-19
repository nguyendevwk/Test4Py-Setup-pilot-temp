import pytest
from datetime import datetime
from decimal import Decimal
from pypara.accounting.ledger import GeneralLedgerProgram
from pypara.commons.zeitgeist import DateRange
from pypara.commons.numbers import Amount, Quantity
from pypara.accounting.generic import Balance
from pypara.accounting.journaling import JournalEntry, Posting, ReadJournalEntries
from pypara.accounting.accounts import Account
from pypara.accounting.ledger import GeneralLedger


def test_general_ledger_program_is_protocol():
    """
    Verify that GeneralLedgerProgram is a typing.Protocol subclass.
    """
    import typing
    assert issubclass(GeneralLedgerProgram, typing.Protocol)
    # Protocols are not meant to be instantiated directly
    with pytest.raises(TypeError):
        GeneralLedgerProgram()


def test_protocol_structural_compatibility():
    """
    A class that implements the __call__ signature should be considered an instance
    of GeneralLedgerProgram due to structural typing.
    """
    class DummyProgram:
        def __call__(self, period: DateRange) -> GeneralLedger:
            # Return a minimal stub of GeneralLedger for the test
            return GeneralLedger(period)

    dummy = DummyProgram()
    # Structural typing: isinstance should succeed
    assert isinstance(dummy, GeneralLedgerProgram)
    # The callable returns a GeneralLedger instance
    period = DateRange(datetime(2023, 1, 1), datetime(2023, 12, 31))
    result = dummy(period)
    assert isinstance(result, GeneralLedger)
    assert result.period == period


def test_general_ledger_program_call_returns_expected_structure():
    """
    Ensure that a concrete implementation of GeneralLedgerProgram returns a
    GeneralLedger with the correct period and that its internal structures
    are initialized properly.
    """
    class ConcreteProgram:
        def __call__(self, period: DateRange) -> GeneralLedger:
            return GeneralLedger(period)

    program = ConcreteProgram()
    period = DateRange(datetime(2024, 1, 1), datetime(2024, 12, 31))
    ledger = program(period)

    # Check that the ledger period matches the input
    assert ledger.period == period

    # The ledger should have an empty list of entries initially
    assert ledger.entries == []

    # Adding a dummy entry should reflect in the ledger
    account = Account("Cash")
    posting = Posting(account, Amount(Decimal("100.00")))
    entry = JournalEntry([posting])
    ledger.entries.append(entry)

    assert len(ledger.entries) == 1
    assert ledger.entries[0] is entry
    assert ledger.entries[0].postings[0].account == account
    assert ledger.entries[0].postings[0].amount == Amount(Decimal("100.00"))
