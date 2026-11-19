import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_repeat_count_attribute():
    """
    Verify that genty_repeat attaches the correct repeat count to the wrapped test method
    and returns the original function unchanged.
    """
    # Arrange
    original_count = 4

    def original_test(self):
        """Dummy test method."""

    # Act
    wrapped_test = genty_repeat(original_count)(original_test)

    # Assert
    assert wrapped_test is original_test, "Decorator should return the original function unchanged."
    assert hasattr(wrapped_test, "genty_repeat_count"), "Wrapped function must have genty_repeat_count attribute."
    assert wrapped_test.genty_repeat_count == original_count, (
        f"Expected genty_repeat_count to be {original_count}, got {wrapped_test.genty_repeat_count}"
    )
