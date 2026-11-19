import inspect
import types
import pytest
from pypara.accounting.journaling import ReadJournalEntries
from pypara.commons.zeitgeist import DateRange

def test_readjournalentries_is_protocol_subclass():
    """Ensure ReadJournalEntries is a subclass of typing.Protocol."""
    from typing import Protocol
    assert issubclass(ReadJournalEntries, Protocol), "ReadJournalEntries should inherit from Protocol"

def test_readjournalentries_has_call_method():
    """Verify that the protocol defines a __call__ method."""
    assert hasattr(ReadJournalEntries, "__call__"), "__call__ method missing in ReadJournalEntries"
    assert isinstance(ReadJournalEntries.__call__, types.FunctionType), "__call__ is not a function"

def test_readjournalentries_call_signature():
    """Check that the __call__ signature matches the expected parameters."""
    sig = inspect.signature(ReadJournalEntries.__call__)
    params = list(sig.parameters.values())
    # Expecting exactly one positional parameter named 'period' of type DateRange
    assert len(params) == 1, f"Expected 1 parameter, got {len(params)}"
    param = params[0]
    assert param.name == "period", f"Parameter name should be 'period', got {param.name}"
    assert param.annotation is DateRange, f"Parameter annotation should be DateRange, got {param.annotation}"
    assert sig.return_annotation is inspect.Signature.empty or sig.return_annotation is Iterable, \
        "Return annotation should be Iterable or unspecified"
