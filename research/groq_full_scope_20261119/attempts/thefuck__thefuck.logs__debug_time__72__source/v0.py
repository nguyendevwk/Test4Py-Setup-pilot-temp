import time
import types
import pytest
from contextlib import contextmanager

# Import the module under test
import thefuck.logs as logs


def test_debug_time_yields_and_calls_debug(monkeypatch):
    """Verify that debug_time yields control and calls debug with a time delta."""
    called = {}
    def fake_debug(msg):
        called['msg'] = msg
    monkeypatch.setattr(logs, 'debug', fake_debug)

    with logs.debug_time('test') as ctx:
        # Inside the context manager, ctx should be None
        assert ctx is None
    # After exiting, debug should have been called
    assert 'msg' in called
    assert called['msg'].startswith('test took: ')
    # The time delta should be a string representation of a timedelta
    assert isinstance(called['msg'].split('took: ')[1], str)


def test_debug_time_with_sleep(monkeypatch):
    """Ensure that the reported time delta reflects actual elapsed time."""
    called = {}
    def fake_debug(msg):
        called['msg'] = msg
    monkeypatch.setattr(logs, 'debug', fake_debug)

    with logs.debug_time('sleep'):
        time.sleep(0.05)  # sleep for 50 ms
    # Extract the numeric part of the timedelta string
    delta_str = called['msg'].split('took: ')[1]
    # Convert to seconds (approximate)
    seconds = float(delta_str.split(' ')[0])
    # The elapsed time should be at least 0.05 seconds
    assert seconds >= 0.05


def test_debug_time_propagates_exceptions(monkeypatch):
    """Check that exceptions inside the context are propagated and debug is still called."""
    called = {}
    def fake_debug(msg):
        called['msg'] = msg
    monkeypatch.setattr(logs, 'debug', fake_debug)

    with pytest.raises(RuntimeError):
        with logs.debug_time('error'):
            raise RuntimeError('boom')
    # Even though an exception occurred, debug should still have been called
    assert 'msg' in called
    assert called['msg'].startswith('error took: ')
