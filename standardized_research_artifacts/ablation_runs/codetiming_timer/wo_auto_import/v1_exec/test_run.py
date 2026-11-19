import math
import time
import pytest
from codetiming import Timer, TimerError

def test_timer_start_stop_and_logging():
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    t = Timer(
        name="test",
        text="Elapsed: {:0.4f}s",
        initial_text="Starting timer {name}",
        logger=logger,
    )

    # Start the timer and check initial log
    t.start()
    assert logs[0] == "Starting timer test"

    # Starting again while running should raise an error
    with pytest.raises(TimerError):
        t.start()

    # Let the timer run a bit
    time.sleep(0.01)

    # Stop the timer and verify elapsed time and logs
    elapsed = t.stop()
    assert isinstance(elapsed, float)
    assert elapsed > 0
    assert logs[1].startswith("Elapsed: ")
    assert logs[1].endswith("s")
    assert math.isclose(t.last, elapsed, rel_tol=1e-6)
    assert math.isclose(Timer.timers.data["test"], elapsed, rel_tol=1e-6)
    assert Timer.timers._timings["test"][-1] == elapsed

    # Stopping again should raise an error
    with pytest.raises(TimerError):
        t.stop()
