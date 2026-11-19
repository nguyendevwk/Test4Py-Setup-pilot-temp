import importlib
import importlib.util
import pathlib
import pytest

def _load_genty_repeat():
    module_path = pathlib.Path(__file__).resolve().parents[4] / "genty" / "genty_repeat.py"
    spec = importlib.util.spec_from_file_location("genty_repeat", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.genty_repeat

def test_genty_repeat_sets_count_attribute():
    genty_repeat = _load_genty_repeat()

    def dummy_test(self):
        pass

    assert not hasattr(dummy_test, "genty_repeat_count")

    decorated = genty_repeat(3)(dummy_test)

    assert decorated is dummy_test
    assert getattr(dummy_test, "genty_repeat_count") == 3
