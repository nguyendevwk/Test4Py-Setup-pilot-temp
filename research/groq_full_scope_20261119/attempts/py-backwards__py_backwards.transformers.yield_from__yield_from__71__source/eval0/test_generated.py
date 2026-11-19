import pytest
from py_backwards.transformers.yield_from import yield_from

def test_yield_from_normal_sequence(tmp_path):
    # Create a simple generator that yields numbers 0-2
    def simple_gen():
        for i in range(3):
            yield i

    assignment = []
    # Collect yielded values
    yielded = list(yield_from(simple_gen(), None, assignment))
    assert yielded == [0, 1, 2], "Yielded values should match generator output"
    # After exhaustion, assignment should be extended (empty list in this case)
    assert assignment == [], "Assignment should be extended after StopIteration"

def test_yield_from_empty_generator(tmp_path):
    # Generator that yields nothing
    def empty_gen():
        if False:
            yield

    assignment = []
    yielded = list(yield_from(empty_gen(), None, assignment))
    assert yielded == [], "No values should be yielded for empty generator"
    assert assignment == [], "Assignment should still be extended (empty) after exhaustion"

def test_yield_from_non_iterable_raises():
    # Passing a non-iterable should raise TypeError when iter() is called
    with pytest.raises(TypeError):
        list(yield_from(42, None, []))
