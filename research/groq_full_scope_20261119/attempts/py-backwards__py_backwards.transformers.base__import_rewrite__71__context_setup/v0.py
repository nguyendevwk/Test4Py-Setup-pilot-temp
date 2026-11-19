import importlib
import pytest

# Import the target module
from py_backwards.transformers.base import import_rewrite

# Helper objects to pass to import_rewrite
class Dummy:
    pass

dummy_prev = Dummy()
dummy_curr = Dummy()

def test_import_rewrite_success(monkeypatch):
    """
    Test that import_rewrite calls extend on the previous argument
    when extend does not raise an ImportError.
    """
    called = []

    def fake_extend(arg):
        called.append(arg)

    monkeypatch.setattr("py_backwards.transformers.base.extend", fake_extend)

    import_rewrite(dummy_prev, dummy_curr)

    # extend should be called once with dummy_prev
    assert called == [dummy_prev]

def test_import_rewrite_fallback(monkeypatch):
    """
    Test that import_rewrite falls back to calling extend on the current
    argument when extend(previous) raises ImportError.
    """
    called = []

    def fake_extend(arg):
        if arg is dummy_prev:
            raise ImportError("previous failed")
        called.append(arg)

    monkeypatch.setattr("py_backwards.transformers.base.extend", fake_extend)

    import_rewrite(dummy_prev, dummy_curr)

    # extend should be called once with dummy_curr after failure on dummy_prev
    assert called == [dummy_curr]

def test_import_rewrite_propagates_error(monkeypatch):
    """
    Test that import_rewrite propagates an ImportError if both
    extend(previous) and extend(current) raise ImportError.
    """
    def fake_extend(arg):
        raise ImportError("both failed")

    monkeypatch.setattr("py_backwards.transformers.base.extend", fake_extend)

    with pytest.raises(ImportError, match="both failed"):
        import_rewrite(dummy_prev, dummy_curr)
