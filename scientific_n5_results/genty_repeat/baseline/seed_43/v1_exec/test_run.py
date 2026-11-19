import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_count():
    def dummy_test(self):
        """A placeholder test method."""
        pass

    wrapped = genty_repeat(5)(dummy_test)

    # The wrapper should attach the repeat count to the function
    assert hasattr(wrapped, "genty_repeat_count")
    assert wrapped.genty_repeat_count == 5

    # The wrapper returns the original function object
    assert wrapped is dummy_test
