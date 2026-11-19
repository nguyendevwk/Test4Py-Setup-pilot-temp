import inspect
import pytest
from pypara.accounting.journaling import ReadJournalEntries
from pypara.commons.zeitgeist import DateRange
from pypara.commons.guid import Guid, makeguid
from pypara.accounting.accounts import Account, AccountType
from pypara.commons.numbers import Amount, Quantity, isum
from typing import Iterable, List, Protocol, TypeVar

# Helper type variable for tests
_T = TypeVar("_T")

def test_readjournalentries_signature():
    """Verify that the Protocol defines the expected __call__ signature."""
    sig = inspect.signature(ReadJournalEntries.__call__)
    params = list(sig.parameters.values())
    # Expect one positional argument named 'period' of type DateRange
    assert len(params) == 1
    assert params[0].name == "period"
    assert params[0].annotation is DateRange
    # Return annotation should be Iterable[JournalEntry[_T]]
    assert sig.return_annotation.__origin__ is Iterable

def test_readjournalentries_implementation():
    """A concrete class that implements the Protocol should be callable."""
    class DummyJournalEntry:
        def __init__(self, id: Guid, amount: Amount):
            self.id = id
            self.amount = amount

    class DummyReadJournalEntries(ReadJournalEntries[DummyJournalEntry]):
        def __call__(self, period: DateRange) -> Iterable[DummyJournalEntry]:
            # Return a simple list of entries for the given period
            return [
                DummyJournalEntry(makeguid(), Amount(100)),
                DummyJournalEntry(makeguid(), Amount(200)),
            ]

    reader = DummyReadJournalEntries()
    period = DateRange(start=DateRange.now(), end=DateRange.now())
    entries = list(reader(period))
    assert isinstance(entries, list)
    assert all(isinstance(e, DummyJournalEntry) for e in entries)
    assert len(entries) == 2
    assert entries[0].amount == Amount(100)
    assert entries[1].amount == Amount(200)

def test_readjournalentries_wrong_signature_raises():
    """Implementing the Protocol with an incorrect signature should raise TypeError."""
    with pytest.raises(TypeError):
        class BadReadJournalEntries(ReadJournalEntries[int]):
            # Missing required 'period' parameter
            def __call__(self) -> Iterable[int]:
                return [1, 2, 3]
