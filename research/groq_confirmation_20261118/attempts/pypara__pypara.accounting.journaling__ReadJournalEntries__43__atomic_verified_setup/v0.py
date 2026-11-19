import inspect
import pytest
from pypara.accounting.journaling import ReadJournalEntries
from pypara.commons.zeitgeist import DateRange

def test_readjournalentries_is_protocol():
    """Ensure ReadJournalEntries is a Protocol subclass."""
    assert hasattr(ReadJournalEntries, "__mro__")
    assert ReadJournalEntries.__mro__[0].__name__ == "ReadJournalEntries"
    # Protocols are subclasses of typing.Protocol
    import typing
    assert issubclass(ReadJournalEntries, typing.Protocol)

def test_readjournalentries_call_signature():
    """Verify the __call__ method signature matches the expected parameters."""
    sig = inspect.signature(ReadJournalEntries.__call__)
    params = list(sig.parameters.values())
    # Expect one parameter named 'period' of type DateRange
    assert len(params) == 1
    assert params[0].name == "period"
    assert params[0].annotation is DateRange
    # Return annotation should be Iterable[JournalEntry[_T]] but we cannot check generic
    assert sig.return_annotation is not inspect.Signature.empty

def test_readjournalentries_callable_example():
    """Create a minimal callable that satisfies the protocol and test its behavior."""
    class DummyJournalEntry:
        pass

    def dummy_reader(period: DateRange) -> list[DummyJournalEntry]:
        return [DummyJournalEntry()]

    # The dummy function should be considered an instance of the protocol
    assert isinstance(dummy_reader, ReadJournalEntries)
    # Calling the function should return a list of DummyJournalEntry instances
    entries = dummy_reader(DateRange(2023, 1, 1, 2023, 12, 31))
    assert isinstance(entries, list)
    assert all(isinstance(e, DummyJournalEntry) for e in entries)
