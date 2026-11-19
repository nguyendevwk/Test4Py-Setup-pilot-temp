import datetime
import pytest
from pypara.accounting.journaling import (
    ReadJournalEntries,
    JournalEntry,
    Posting,
    Direction,
    Account,
    AccountType,
)
from pypara.commons.guid import makeguid
from pypara.commons.numbers import Quantity, Amount


# Helper account for testing
class DummyAccount(Account):
    def __init__(self, name: str, acc_type: AccountType):
        super().__init__(name, acc_type)


def test_read_journal_entries_returns_expected_entries(tmp_path):
    """A function matching the ReadJournalEntries protocol should return
    an iterable of JournalEntry objects with correct postings."""
    # Create a simple source object
    class Source:
        def __init__(self, name):
            self.name = name

    source = Source("TestSource")

    # Define a concrete reader function
    def reader(period):
        entry = JournalEntry[Source]()
        entry.date = period.start
        entry.description = "Test entry"
        entry.source = source
        entry.post(
            period.start,
            DummyAccount("Cash", AccountType.ASSET),
            Quantity(100),
        ).post(
            period.start,
            DummyAccount("Revenue", AccountType.REVENUE),
            Quantity(-100),
        )
        return [entry]

    # Ensure the reader conforms to the protocol
    assert isinstance(reader, ReadJournalEntries)

    # Use the reader
    period = type("DateRange", (), {"start": datetime.date(2023, 1, 1), "end": datetime.date(2023, 1, 31)})
    entries = list(reader(period))
    assert len(entries) == 1
    entry = entries[0]
    assert entry.description == "Test entry"
    assert entry.source is source
    assert len(entry.postings) == 2
    inc_postings = list(entry.increments)
    dec_postings = list(entry.decrements)
    assert len(inc_postings) == 1
    assert len(dec_postings) == 1
    inc = inc_postings[0]
    dec = dec_postings[0]
    assert inc.amount == Amount(100)
    assert dec.amount == Amount(100)
    assert inc.is_debit
    assert dec.is_credit


def test_direction_of_raises_on_zero_quantity():
    """Direction.of should raise an AssertionError when quantity is zero."""
    zero_qty = Quantity(0)
    with pytest.raises(AssertionError, match="Encountered a `0` quantity"):
        Direction.of(zero_qty)


def test_journal_entry_validation_ensures_equal_debits_and_credits():
    """JournalEntry.validate should raise an AssertionError if debits and credits differ."""
    entry = JournalEntry[object]()
    entry.date = datetime.date.today()
    entry.description = "Imbalanced entry"
    entry.source = object()
    # Post an imbalance: debit 50, credit 30
    entry.post(
        entry.date,
        DummyAccount("Asset", AccountType.ASSET),
        Quantity(50),
    ).post(
        entry.date,
        DummyAccount("Revenue", AccountType.REVENUE),
        Quantity(-30),
    )
    with pytest.raises(AssertionError, match="Total Debits and Credits are not equal"):
        entry.validate()
