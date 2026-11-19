import datetime
import pytest
from pypara.accounting.journaling import (
    ReadJournalEntries,
    JournalEntry,
    Posting,
    Direction,
    Amount,
    Quantity,
    Account,
    AccountType,
)
from pypara.commons.guid import makeguid
from pypara.commons.numbers import isum
from pypara.commons.zeitgeist import DateRange


# Helper account for tests
class DummyAccount(Account):
    def __init__(self, name: str, acc_type: AccountType):
        super().__init__(name, acc_type)


def test_read_journal_entries_returns_iterable_of_entries(tmp_path):
    """Normal scenario: a ReadJournalEntries implementation returns a list of JournalEntry objects."""
    # Define a simple implementation of the protocol
    def reader(period: DateRange) -> list[JournalEntry[DummyAccount]]:
        entry = JournalEntry[DummyAccount](date=period.start, description="Test", source=DummyAccount("Cash", AccountType.ASSET))
        entry.post(period.start, entry.source, Quantity(100))
        return [entry]

    # Ensure the function satisfies the protocol
    assert isinstance(reader, ReadJournalEntries)

    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 1, 31))
    entries = reader(period)

    assert isinstance(entries, list)
    assert len(entries) == 1
    entry = entries[0]
    assert entry.date == period.start
    assert entry.description == "Test"
    assert entry.source.name == "Cash"
    assert len(entry.postings) == 1
    posting = entry.postings[0]
    assert posting.account.name == "Cash"
    assert posting.amount == Amount(100)
    assert posting.direction == Direction.INC
    assert entry.debits == [posting]
    assert entry.credits == []


def test_journal_entry_validation_raises_on_unbalanced_entries():
    """Boundary scenario: validation should raise when debits and credits are not equal."""
    entry = JournalEntry[DummyAccount](date=datetime.date.today(), description="Unbalanced", source=DummyAccount("Revenue", AccountType.REVENUE))
    # Post a debit of 50
    entry.post(datetime.date.today(), DummyAccount("Cash", AccountType.ASSET), Quantity(50))
    # Post a credit of 30 (unbalanced)
    entry.post(datetime.date.today(), DummyAccount("Revenue", AccountType.REVENUE), Quantity(-30))
    with pytest.raises(AssertionError, match="Total Debits and Credits are not equal"):
        entry.validate()


def test_direction_of_raises_on_zero_quantity():
    """Error scenario: Direction.of should raise when quantity is zero."""
    zero_qty = Quantity(0)
    with pytest.raises(AssertionError, match="Encountered a `0` quantity"):
        Direction.of(zero_qty)
