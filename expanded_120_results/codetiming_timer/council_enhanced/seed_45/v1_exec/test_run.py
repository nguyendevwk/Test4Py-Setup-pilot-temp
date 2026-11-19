import pytest
import time
from codetiming import Timer
from codetiming._timer import TimerError

def test_timer_start_stop_and_logging():
    logs = []

    def logger(msg): logs.append(msg)

    def text_callable(seconds): return f"Done in {seconds:.3f}s"

    t = Timer(name='test', text=text_callable, initial_text=True, logger=logger)

    t.start()
    assert logs[0] == "Timer test started"

    time.sleep(0.01)
    elapsed = t.stop()
    assert logs[1].startswith("Done in")
    assert isinstance(elapsed, float)
    assert t.last == elapsed
    assert t.timers.total('test') == pytest.approx(elapsed)

    t.start()
    time.sleep(0.005)
    t.stop()
    assert t.timers.count('test') == 2

    with pytest.raises(TimerError):
        t.stop()
