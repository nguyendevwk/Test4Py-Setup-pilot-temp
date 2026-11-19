import datetime
import inspect
import typing
import pytest
from pypara.accounting.journaling import ReadJournalEntries
from pypara.commons.zeitgeist import DateRange

# Test 1: Verify that ReadJournalEntries is a Protocol subclass
def test_readjournalentries_is_protocol():
    assert issubclass(ReadJournalEntries, typing.Protocol), "ReadJournalEntries should inherit from typing.Protocol"

# Test 2: Ensure that a class implementing the protocol must define __call__ with the correct signature
def test_protocol_implementation_signature():
    class DummyImplementation:
        def __call__(self, period: DateRange) -> typing.Iterable[int]:
            return [1, 2, 3]

    # Instantiate and call to confirm signature works
    impl = DummyImplementation()
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    result = impl(period)
    assert isinstance(result, list) and result == [1, 2, 3], "Implementation should return the expected list"

    # Inspect the __call__ method signature
    sig = inspect.signature(DummyImplementation.__call__)
    assert sig.parameters["period"].annotation is DateRange, "Parameter 'period' should be annotated with DateRange"
    assert sig.return_annotation is typing.Iterable[int], "Return annotation should be Iterable[int]"

# Test 3: Confirm that calling a non-implementing object raises TypeError
def test_non_implementing_object_raises():
    class NonImplementing:
        pass

    non_impl = NonImplementing()
    period = DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    with pytest.raises(TypeError):
        # Attempt to call the object as if it were a ReadJournalEntries instance
        non_impl(period)
