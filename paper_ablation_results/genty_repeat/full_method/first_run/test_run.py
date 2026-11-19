import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_repeat_count():
    count = 5

    def dummy_test(self):
        """Dummy test method to be decorated."""
        pass

    # Ensure attribute is not present before decoration
    assert not hasattr(dummy_test, "genty_repeat_count")

    # Apply the decorator
    wrapped = genty_repeat(count)(dummy_test)

    # The decorator should return the original function
    assert wrapped is dummy_test

    # The attribute should be set to the provided count
    assert getattr(wrapped, "genty_repeat_count") == count
