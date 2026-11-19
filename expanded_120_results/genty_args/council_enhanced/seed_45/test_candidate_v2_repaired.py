import importlib
import pytest
import importlib.util
from pathlib import Path

def load_genty_args():
    """Load GentyArgs directly from source, bypassing package init."""
    module_path = Path(__file__).resolve().parents[4] / "genty" / "genty_args.py"
    spec = importlib.util.spec_from_file_location("genty_args", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.GentyArgs

def test_genty_args_iteration_and_properties():
    GentyArgs = load_genty_args()
    g = GentyArgs(1, "two", key="val", another=3)
    assert g.args == (1, "two")
    assert g.kwargs == {"key": "val", "another": 3}
    # Positional args first, then keyword args sorted alphabetically by key
    assert list(g) == ["1", "'two'", "another=3", "key='val'"]
    g_empty = GentyArgs()
    assert list(g_empty) == []
