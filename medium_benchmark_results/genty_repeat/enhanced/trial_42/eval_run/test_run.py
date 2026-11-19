import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_attribute():
    """genty_repeat should attach the correct repeat count to the test method."""
    @genty_repeat(3)
    def dummy_test_method():
        pass

    # The decorator returns the original function unchanged
    assert dummy_test_method is not None
    # The attribute should be set to the provided count
    assert getattr(dummy_test_method, "genty_repeat_count", None) == 3
