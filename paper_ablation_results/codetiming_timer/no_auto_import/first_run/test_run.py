import pytest
from unittest.mock import patch
from codetiming._timer import Timer

def test_timer_stop_logs_and_updates():
    logs = []
    t = Timer(name='test', logger=lambda s: logs.append(s))
    Timer.timers.clear()
    with patch('codetiming._timer.time.perf_counter', side_effect=[0.0, 1.2345]):
        t.start()
        elapsed = t.stop()
    assert elapsed == 1.2345
    assert t.last == 1.2345
    assert t._start_time is None
    assert logs == ["Elapsed time: 1.2345 seconds"]
    assert Timer.timers.data['test'] == 1.2345
    assert Timer.timers._timings['test'] == [1.2345]
