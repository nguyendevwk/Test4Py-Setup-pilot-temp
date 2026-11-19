import pytest
from typing import Iterable, List
from pypara.accounting.journaling import ReadJournalEntries
from pypara.commons.zeitgeist import DateRange
from pypara.commons.numbers import Amount, isum
from datetime import datetime, timedelta

# --------------------------------------------------------------------------- #
# Test 1: Verify that ReadJournalEntries is a Protocol subclass
# --------------------------------------------------------------------------- #
def test_read_journal_entries_is_protocol():
    """The ReadJournalEntries type should be a subclass of typing.Protocol."""
    from typing import Protocol
    assert issubclass(ReadJournalEntries, Protocol), "ReadJournalEntries must inherit from Protocol"

# --------------------------------------------------------------------------- #
# Test 2: Ensure that a simple function matching the protocol can be called
# --------------------------------------------------------------------------- #
def test_simple_function_matches_protocol(tmp_path):
    """A function that returns an iterable of dummy entries should satisfy the protocol."""
    # Define a minimal JournalEntry dataclass for testing
    from dataclasses import dataclass
    @dataclass
    class DummyEntry:
        date: datetime
        amount: Amount

    # Create a simple function that matches the protocol signature
    def simple_reader(period: DateRange) -> Iterable[DummyEntry]:
        start, end = period.start, period.end
        # generate one entry per day in the range
        current = start
        while current <= end:
            yield DummyEntry(date=current, amount=Amount(10))
            current += timedelta(days=1)

    # Assign to a variable typed as ReadJournalEntries[DummyEntry]
    reader: ReadJournalEntries[DummyEntry] = simple_reader

    # Call the reader and collect results
    period = DateRange(datetime(2023, 1, 1), datetime(2023, 1, 3))
    entries: List[DummyEntry] = list(reader(period))

    # Assertions on the returned entries
    assert len(entries) == 3
    assert all(isinstance(e, DummyEntry) for e in entries)
    assert entries[0].date == datetime(2023, 1, 1)
    assert entries[-1].date == datetime(2023, 1, 3)
    assert all(e.amount == Amount(10) for e in entries)

# --------------------------------------------------------------------------- #
# Test 3: Verify that the protocol can be used in a type-checking context
# --------------------------------------------------------------------------- #
def test_protocol_type_checking(tmp_path):
    """Using the protocol in a type-annotated function should not raise runtime errors."""
    # Define a function that expects a ReadJournalEntries argument
    def process_entries(reader: ReadJournalEntries[Amount]):
        period = DateRange(datetime(2023, 1, 1), datetime(2023, 1, 1))
        return list(reader(period))

    # Provide a simple implementation
    def amount_reader(period: DateRange) -> Iterable[Amount]:
        return [Amount(5)]

    # Call the processing function with the implementation
    result = process_entries(amount_reader)

    # Assertions
    assert result == [Amount(5)]
