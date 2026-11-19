import importlib
import pytest
import importlib.util
from pathlib import Path

def load_genty_repeat():
    """Load genty_repeat from source file without importing the package."""
    # Resolve the path to genty/genty_repeat.py relative to this test file
    root = Path(__file__).resolve().parents[5]  # root of the repository
    module_path = root / "genty" / "genty_repeat.py"
    spec = importlib.util.spec_from_file_location("genty_repeat", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.genty_repeat

def test_genty_repeat_behavior():
    genty_repeat = load_genty_repeat()

    # Positive count: decorator should set attribute and return the same function
    def dummy(self):  # pragma: no cover
        pass

    count = 3
    decorator = genty_repeat(count)
    decorated = decorator(dummy)
    assert decorated is dummy
    assert getattr(decorated, "genty_repeat_count") == count

    # Zero count: still valid, attribute set to 0
    zero_decorator = genty_repeat(0)
    zero_decorated = zero_decorator(dummy)
    assert zero_decorated is dummy
    assert zero_decorated.genty_repeat_count == 0

    # Negative count: should raise ValueError
    with pytest.raises(ValueError) as excinfo:
        genty_repeat(-1)
    assert "Can't have -1 iterations" in str(excinfo.value)
