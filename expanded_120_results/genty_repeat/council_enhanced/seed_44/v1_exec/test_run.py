import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_count():
    @genty_repeat(3)
    def dummy_test(self):
        """Dummy test function for genty_repeat."""

    # The decorator should attach the repeat count to the function
    assert hasattr(dummy_test, "genty_repeat_count")
    assert dummy_test.genty_repeat_count == 3

    # The decorator should return the original function object unchanged
    assert dummy_test.__name__ == "dummy_test"
    assert dummy_test.__doc__ == "Dummy test function for genty_repeat."
