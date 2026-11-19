import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_attribute():
    @genty_repeat(3)
    def dummy_test():
        """Dummy test function."""
        pass

    # The decorator should attach the repeat count as an attribute.
    assert hasattr(dummy_test, "genty_repeat_count")
    assert dummy_test.genty_repeat_count == 3
    # The function should remain callable and unchanged otherwise.
    assert callable(dummy_test)
