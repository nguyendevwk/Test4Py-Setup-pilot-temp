import pytest
from py_backwards.transformers.base import import_rewrite

# Helper to create a callable that records calls
class CallRecorder:
    def __init__(self):
        self.calls = []

    def __call__(self, arg):
        self.calls.append(arg)

def test_import_rewrite_calls_previous_on_success(monkeypatch):
    # Arrange: patch extend to record calls and succeed
    recorder = CallRecorder()
    monkeypatch.setattr("py_backwards.transformers.base.extend", recorder)

    previous = "prev_module"
    current = "curr_module"

    # Act
    import_rewrite(previous, current)

    # Assert: extend called once with previous, current not called
    assert recorder.calls == [previous], "extend should be called once with previous"

def test_import_rewrite_calls_current_on_import_error(monkeypatch):
    # Arrange: patch extend to raise ImportError on first call, then record
    call_order = []

    def extend_side_effect(arg):
        call_order.append(arg)
        if arg == "prev_module":
            raise ImportError("simulated import error")
        # else succeed silently

    monkeypatch.setattr("py_backwards.transformers.base.extend", extend_side_effect)

    previous = "prev_module"
    current = "curr_module"

    # Act
    import_rewrite(previous, current)

    # Assert: extend called twice, first with previous (raising), then with current
    assert call_order == [previous, current], "extend should be called with previous then current"

def test_import_rewrite_does_not_raise_when_extend_succeeds(monkeypatch):
    # Arrange: patch extend to succeed for both arguments
    recorder = CallRecorder()
    monkeypatch.setattr("py_backwards.transformers.base.extend", recorder)

    previous = "prev_module"
    current = "curr_module"

    # Act & Assert: no exception should be raised
    try:
        import_rewrite(previous, current)
    except Exception as e:
        pytest.fail(f"import_rewrite raised an unexpected exception: {e}")

    # Verify calls
    assert recorder.calls == [previous], "extend should be called only with previous when no ImportError"
