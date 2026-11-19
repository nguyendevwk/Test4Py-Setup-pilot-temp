import math
import time
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_and_errors():
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    # Create timer with custom text and initial_text
    t = Timer(name="test", text="Elapsed: {seconds:.2f}s", initial_text="Starting timer {name}", logger=logger)

    # Start timer: should log initial_text
    t.start()
    assert logs == ["Starting timer test"]
    assert t._start_time is not None

    # Stop timer: should log formatted elapsed time and record in timers
    time.sleep(0.01)  # allow some elapsed time
    elapsed = t.stop()
    assert math.isclose(elapsed, t.last, rel_tol=1e-2)
    assert t._start_time is None
    assert len(logs) == 2
    assert logs[1].startswith("Elapsed: ")
    # Check timers collection updated
    recorded = t.timers.get("test")
    assert recorded is not None
    assert math.isclose(recorded, elapsed, rel_tol=1e-2)

    # Starting an already running timer raises TimerError
    t2 = Timer(logger=logger)
    t2.start()
    with pytest.raises(TimerError, match="Timer is running"):
        t2.start()
    t2.stop()

    # Stopping a timer that hasn't started raises TimerError
    t3 = Timer(logger=logger)
    with pytest.raises(TimerError, match="Timer is not running"):
        t3.stop()
