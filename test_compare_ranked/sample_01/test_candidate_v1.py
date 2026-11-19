import time
from codetiming._timer import Timer

def test_timer_start_stop_logging_and_timers():
    logs = []
    Timer.timers.clear()
    t = Timer(name="test", initial_text=True, logger=lambda msg: logs.append(msg))
    t.start()
    time.sleep(0.01)
    elapsed = t.stop()
    assert elapsed > 0
    assert logs[0] == "Timer test started"
    assert logs[1].startswith("Elapsed time:")
    elapsed_str = logs[1].split()[2]
    assert abs(float(elapsed_str) - elapsed) < 0.001
    assert t._start_time is None
    assert Timer.timers.data["test"] == elapsed
