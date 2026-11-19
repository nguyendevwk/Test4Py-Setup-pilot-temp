import pytest
from py_backwards.transformers.base import import_rewrite

# Helper to replace the extend function in the module
def replace_extend(monkeypatch, func):
    monkeypatch.setattr("py_backwards.transformers.base.extend", func)

def test_import_rewrite_calls_previous(monkeypatch):
    called = {"prev": False, "curr": False}

    def fake_extend(arg):
        if arg == "prev":
            called["prev"] = True
        elif arg == "curr":
            called["curr"] = True
        else:
            raise ValueError("Unexpected argument")

    replace_extend(monkeypatch, fake_extend)

    import_rewrite("prev", "curr")

    assert called["prev"] is True, "extend(previous) should be called"
    assert called["curr"] is False, "extend(current) should not be called when no ImportError"

def test_import_rewrite_falls_back_on_importerror(monkeypatch):
    called = {"prev": False, "curr": False}

    def fake_extend(arg):
        if arg == "prev":
            called["prev"] = True
            raise ImportError("Simulated import error")
        elif arg == "curr":
            called["curr"] = True
        else:
            raise ValueError("Unexpected argument")

    replace_extend(monkeypatch, fake_extend)

    import_rewrite("prev", "curr")

    assert called["prev"] is True, "extend(previous) should be called first"
    assert called["curr"] is True, "extend(current) should be called after ImportError"

def test_import_rewrite_propagates_other_exceptions(monkeypatch):
    def fake_extend(arg):
        raise RuntimeError("Unexpected error")

    replace_extend(monkeypatch, fake_extend)

    with pytest.raises(RuntimeError, match="Unexpected error"):
        import_rewrite("prev", "curr")
