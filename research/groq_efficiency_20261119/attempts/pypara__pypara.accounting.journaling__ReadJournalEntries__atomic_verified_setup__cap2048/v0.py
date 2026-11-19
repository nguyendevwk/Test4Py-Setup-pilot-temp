import pytest
import typing
from pypara.accounting.journaling import ReadJournalEntries
from datetime import datetime
from pypara.commons.zeitgeist import DateRange

def test_readjournalentries_is_protocol():
    """The target should be a typing.Protocol subclass."""
    assert isinstance(ReadJournalEntries, type)
    assert issubclass(ReadJournalEntries, typing.Protocol)

def test_readjournalentries_has_call_signature():
    """The protocol must declare a __call__ method with the expected signature."""
    # The __call__ attribute should be a function descriptor
    assert hasattr(ReadJournalEntries, "__call__")
    call = getattr(ReadJournalEntries, "__call__")
    # The __call__ should be a function defined in the protocol
    assert isinstance(call, typing.Callable)
    # Inspect the signature: it should accept a DateRange and return an Iterable
    import inspect
    sig = inspect.signature(call)
    params = sig.parameters
    assert "period" in params
    assert params["period"].annotation is DateRange
    assert sig.return_annotation is typing.Iterable

def test_readjournalentries_protocol_usage(tmp_path):
    """A concrete class implementing the protocol should be accepted by type checks."""
    from pypara.commons.zeitgeist import DateRange
    from pypara.commons.guid import Guid, makeguid
    from pypara.accounting.journaling import JournalEntry
    from typing import Iterable

    class DummyJournalEntry(JournalEntry[int]):
        def __init__(self, id: int):
            self.id = id

    class DummyReader(ReadJournalEntries[int]):
        def __call__(self, period: DateRange) -> Iterable[DummyJournalEntry]:
            # Return a simple list of entries for the given period
            return [DummyJournalEntry(1), DummyJournalEntry(2)]

    reader = DummyReader()
    period = DateRange(datetime(2023, 1, 1), datetime(2023, 12, 31))
    entries = list(reader(period))
    assert len(entries) == 2
    assert all(isinstance(e, DummyJournalEntry) for e in entries)
    assert entries[0].id == 1
    assert entries[1].id == 2
