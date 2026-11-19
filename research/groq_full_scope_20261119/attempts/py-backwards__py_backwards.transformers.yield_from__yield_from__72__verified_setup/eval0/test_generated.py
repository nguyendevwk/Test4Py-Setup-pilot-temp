import pytest
from py_backwards.transformers.yield_from import yield_from

def test_yield_from_normal_iteration():
    # Generator that yields three values
    def gen():
        for i in range(3):
            yield i
    assignment = []
    # Collect values from the yield_from generator
    result = list(yield_from(gen(), None, assignment))
    assert result == [0, 1, 2], "yield_from should yield all values from the generator"
    # After exhaustion, assignment should have been extended (non-empty)
    assert assignment, "assignment should be extended after StopIteration"

def test_yield_from_immediate_stop():
    # Generator that yields nothing
    def empty_gen():
        if False:
            yield
    assignment = []
    result = list(yield_from(empty_gen(), None, assignment))
    assert result == [], "yield_from should yield nothing for an empty generator"
    assert assignment, "assignment should be extended even if generator is empty"

def test_yield_from_unexpected_exception():
    # Generator that raises a ValueError
    def bad_gen():
        raise ValueError("unexpected")
    assignment = []
    with pytest.raises(ValueError, match="unexpected"):
        list(yield_from(bad_gen(), None, assignment))
    # assignment should remain unchanged because StopIteration was not reached
    assert assignment == [], "assignment should not be extended if an unexpected exception occurs"
