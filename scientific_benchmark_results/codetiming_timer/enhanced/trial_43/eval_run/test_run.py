import pytest
from unittest.mock import patch
from codetiming._timer import Timer, TimerError

def test_timer_stop_logs_and_updates_timers():
    # Ensure a clean timers state
    Timer.timers.clear()

    logs = []

    # Patch perf_counter to return deterministic values
    with patch('codetiming._timer.time.perf_counter', side_effect=[0.0, 5.0]):
        t = Timer(name='perf', text='Elapsed: {:0.4f}s', logger=logs.append)
        t.start()
        elapsed = t.stop()

    # Verify elapsed time is as expected
    assert elapsed == 5.0
    assert t.last == 5.0

    # Verify logger output
    assert logs == ["Elapsed: 5.0000s"]

    # Verify timers data updated
    assert Timer.timers.data['perf'] == 5.0
    assert Timer.timers._timings['perf'] == [5.0]
