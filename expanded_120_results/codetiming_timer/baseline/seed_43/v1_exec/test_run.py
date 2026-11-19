import time
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_and_logging():
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    t = Timer(
        name="my_timer",
        logger=logger,
        initial_text=True,
        text=lambda x: f"Elapsed: {x:.2f}s",
    )

    # Start the timer and check initial log
    t.start()
    assert t._start_time is not None
    assert logs[-1] == "Timer my_timer started"

    # Wait a short time and stop the timer
    time.sleep(0.01)
    elapsed = t.stop()
    assert isinstance(elapsed, float)
    assert t.last == elapsed
    assert logs[-1] == f"Elapsed: {elapsed:.2f}s"

    # Verify the timer was recorded in the global Timers collection
    assert t.timers.get("my_timer") == elapsed

    # Restart the timer and stop again
    t.start()
    t.stop()

    # Starting an already running timer should raise TimerError
    with pytest.raises(TimerError):
        t.start()
        t.start()

    # Stopping a timer that hasn't been started should raise TimerError
    t2 = Timer(name="t2", logger=logger)
    with pytest.raises(TimerError):
        t2.stop()
