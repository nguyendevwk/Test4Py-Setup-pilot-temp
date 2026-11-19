import importlib
import pathlib
import importlib.util

import pytest

# Load the genty_repeat module without importing the package __init__
root = pathlib.Path(__file__).resolve().parents[5]  # root of the repo
spec = importlib.util.spec_from_file_location(
    "genty_repeat", root / "genty" / "genty_repeat.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
genty_repeat = module.genty_repeat


def test_genty_repeat_sets_count_and_preserves_function():
    @genty_repeat(3)
    def dummy_test(self):
        """Dummy test function for genty_repeat."""
        pass

    # The decorator should attach the repeat count to the function
    assert hasattr(dummy_test, "genty_repeat_count")
    assert dummy_test.genty_repeat_count == 3

    # The decorator should return the original function object unchanged
    assert dummy_test.__name__ == "dummy_test"
    assert dummy_test.__doc__ == "Dummy test function for genty_repeat."
