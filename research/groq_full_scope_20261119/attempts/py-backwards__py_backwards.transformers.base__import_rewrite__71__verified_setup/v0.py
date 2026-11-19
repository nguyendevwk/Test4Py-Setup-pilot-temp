import importlib
import pytest
from py_backwards.transformers.base import import_rewrite

# Helper to create a dummy object that can be passed to extend
class Dummy:
    def __init__(self, name):
        self.name = name

def test_import_rewrite_success(monkeypatch):
    """extend(previous) succeeds, extend(current) is not called."""
    called = {"previous": False, "current": False}

    def fake_extend(obj):
        if obj.name == "previous":
            called["previous"] = True
        else:
            called["current"] = True

    monkeypatch.setattr(importlib.import_module("py_backwards.utils.snippet"), "extend", fake_extend)

    import_rewrite(Dummy("previous"), Dummy("current"))

    assert called["previous"] is True
    assert called["current"] is False

def test_import_rewrite_fallback(monkeypatch):
    """extend(previous) raises ImportError, extend(current) succeeds."""
    called = {"previous": False, "current": False}

    def fake_extend(obj):
        if obj.name == "previous":
            called["previous"] = True
            raise ImportError("simulated failure")
        else:
            called["current"] = True

    monkeypatch.setattr(importlib.import_module("py_backwards.utils.snippet"), "extend", fake_extend)

    import_rewrite(Dummy("previous"), Dummy("current"))

    assert called["previous"] is True
    assert called["current"] is True

def test_import_rewrite_both_fail(monkeypatch):
    """extend(previous) raises ImportError and extend(current) also raises ImportError."""
    def fake_extend(obj):
        raise ImportError("simulated failure")

    monkeypatch.setattr(importlib.import_module("py_backwards.utils.snippet"), "extend", fake_extend)

    with pytest.raises(ImportError, match="simulated failure"):
        import_rewrite(Dummy("previous"), Dummy("current"))
