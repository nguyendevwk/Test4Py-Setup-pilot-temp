import importlib
import importlib.util
import pytest

# Load GentyArgs without executing genty/__init__.py (which imports missing six)
spec = importlib.util.find_spec("genty.genty_args")
assert spec is not None, "Could not find genty.genty_args module"
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
GentyArgs = module.GentyArgs


def test_genty_args_iteration_and_properties():
    """Verify that GentyArgs stores args/kwargs correctly and iterates
    over formatted values in the expected order."""
    g = GentyArgs(1, 2, key="val")

    # Property access should return the original values
    assert isinstance(g.args, tuple)
    assert g.args == (1, 2)
    assert isinstance(g.kwargs, dict)
    assert g.kwargs == {"key": "val"}

    # Iteration should yield formatted positional args followed by
    # sorted keyword args in "key='val'" form
    iterated = list(g)
    assert iterated == ["1", "2", "key='val'"]
