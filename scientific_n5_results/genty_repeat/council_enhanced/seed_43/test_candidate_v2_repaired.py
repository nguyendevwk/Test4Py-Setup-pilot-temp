import importlib
import importlib.util
import pathlib
import pytest

def test_genty_repeat_sets_repeat_count_attribute():
    """
    Verify that genty_repeat attaches the correct repeat count to the wrapped test method
    and returns the original function unchanged.
    """
    # Dynamically load genty_repeat without importing the genty package (avoids missing six)
    root = pathlib.Path(__file__).parents[5]  # go up to repository root
    module_path = root / "genty" / "genty_repeat.py"
    spec = importlib.util.spec_from_file_location("genty_repeat", module_path)
    genty_repeat_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(genty_repeat_module)

    genty_repeat = genty_repeat_module.genty_repeat

    original_count = 4

    def original_test(self):
        """Dummy test method."""

    wrapped_test = genty_repeat(original_count)(original_test)

    assert wrapped_test is original_test, "Decorator should return the original function unchanged."
    assert hasattr(wrapped_test, "genty_repeat_count"), "Wrapped function must have genty_repeat_count attribute."
    assert wrapped_test.genty_repeat_count == original_count, (
        f"Expected genty_repeat_count to be {original_count}, got {wrapped_test.genty_repeat_count}"
    )
