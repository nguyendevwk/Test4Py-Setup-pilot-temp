import datetime
import pytest
from pypara.accounting.journaling import ReadJournalEntries
from pypara.commons.zeitgeist import DateRange

def test_readjournalentries_is_protocol():
    """The target should be a subclass of typing.Protocol."""
    from typing import Protocol
    assert issubclass(ReadJournalEntries, Protocol), "ReadJournalEntries must inherit from Protocol"

def test_readjournalentries_callable_signature():
    """A callable that matches the protocol should accept a DateRange and return an iterable."""
    # Define a minimal implementation that satisfies the protocol
    class DummyJournalReader:
        def __call__(self, period: DateRange):
            # Return a simple list of dummy entries
            return [("entry1", period.start), ("entry2", period.end)]

    reader = DummyJournalReader()
    # Ensure the instance is considered a ReadJournalEntries
    assert isinstance(reader, ReadJournalEntries), "Instance should be recognized as ReadJournalEntries"

    # Create a DateRange for testing
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 12, 31)
    period = DateRange(start, end)

    result = reader(period)
    assert isinstance(result, Iterable), "Result should be iterable"
    assert list(result) == [("entry1", start), ("entry2", end)], "Entries should match expected values"

def test_readjournalentries_invalid_input_raises():
    """Passing an invalid type to a ReadJournalEntries implementation should raise a TypeError."""
    class BadJournalReader:
        def __call__(self, period: DateRange):
            # Intentionally ignore the period and return a non-iterable
            return None

    reader = BadJournalReader()
    assert isinstance(reader, ReadJournalEntries), "Instance should be recognized as ReadJournalEntries"

    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 12, 31)
    period = DateRange(start, end)

    with pytest.raises(TypeError):
        # The protocol expects an iterable; returning None should cause a TypeError when iterated
        for _ in reader(period):
            pass
