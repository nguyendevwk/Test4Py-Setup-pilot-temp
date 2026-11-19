import datetime
import pytest
from typing import Iterable, List

from pypara.accounting.journaling import ReadJournalEntries, DateRange
from pypara.commons.zeitgeist import DateRange as ZDateRange


def sample_func(period: ZDateRange) -> Iterable[int]:
    """A minimal function that matches the ReadJournalEntries protocol."""
    return [1, 2, 3]


def wrong_func(period: ZDateRange) -> List[int]:
    """A function that returns a list instead of an iterable of JournalEntry."""
    return [1, 2, 3]


def test_read_journal_entries_protocol_instance_check():
    """The protocol should recognize a matching function as an instance."""
    assert isinstance(sample_func, ReadJournalEntries)


def test_read_journal_entries_protocol_non_instance():
    """A function with a mismatched return type should not be considered an instance."""
    assert not isinstance(wrong_func, ReadJournalEntries)


def test_read_journal_entries_protocol_call_error():
    """Attempting to instantiate the protocol directly should raise a TypeError."""
    with pytest.raises(TypeError):
        ReadJournalEntries()
