import time
import pytest
from codetiming._timer import Timer, TimerError


def test_timer_start_stop_records_elapsed_and_logs():
    logged = []

    def logger(msg: str) -> None:
        logged.append(msg)

    t = Timer(name="demo", text="Elapsed: {:.2f}s", logger=logger)
    t.start()
    # Ensure start sets the internal start time
    assert t._start_time is not None

    # Sleep a short, deterministic amount of time
    time.sleep(0.01)

    elapsed = t.stop()
    # After stop, _start_time should be cleared
    assert t._start_time is None
    # The elapsed time should be a positive float
    assert isinstance(elapsed, float) and elapsed > 0
    # The last recorded time should match the returned value
    assert t.last == elapsed
    # Logger should have been called once with the formatted elapsed time
    assert len(logged) == 1
    assert logged[0].startswith("Elapsed: ")
    assert logged[0].endswith("s")
