import pytest
import datetime
from pypara.accounting.journaling import ReadJournalEntries
from pypara.commons.zeitgeist import DateRange

def test_read_journal_entries_has_call_attribute():
    """The ReadJournalEntries protocol should expose a __call__ attribute."""
    assert hasattr(ReadJournalEntries, "__call__"), "Protocol missing __call__"

def test_read_journal_entries_callable_behavior():
    """Calling the protocol directly should raise a TypeError because it is not a concrete implementation."""
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    with pytest.raises(TypeError):
        ReadJournalEntries(period)

def test_read_journal_entries_subclassing_and_call():
    """A concrete function that matches the protocol can be called and returns an iterable."""
    def dummy_reader(period: DateRange):
        return [("entry1", period.start), ("entry2", period.end)]

    # Ensure the dummy function satisfies the protocol
    assert isinstance(dummy_reader, ReadJournalEntries), "Function does not match protocol"

    period = DateRange(datetime.date(2024, 1, 1), datetime.date(2024, 1, 31))
    result = dummy_reader(period)
    assert isinstance(result, list), "Result should be a list"
    assert result == [("entry1", period.start), ("entry2", period.end)], "Unexpected entries returned"
