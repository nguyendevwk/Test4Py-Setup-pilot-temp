import math
import time
import pytest
from codetiming._timer import Timer

def test_timer_start_stop_logs_and_elapsed():
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    # Create a timer with a name, custom text format, and an initial text
    t = Timer(
        name="demo",
        text="Elapsed: {seconds:.2f}s",
        initial_text="Starting timer {name}",
        logger=logger,
    )

    # Start the timer and verify the initial log
    t.start()
    assert logs == ["Starting timer demo"], "Initial text not logged correctly"

    # Wait a short period to generate measurable elapsed time
    time.sleep(0.01)

    # Stop the timer and verify the elapsed log and returned value
    elapsed = t.stop()
    assert len(logs) == 2, "Elapsed log not recorded"
    assert logs[1].startswith("Elapsed: "), "Elapsed log format incorrect"
    # Extract the numeric part from the log
    logged_seconds = float(logs[1].split()[1][:-1])  # remove trailing 's'
    assert math.isclose(elapsed, logged_seconds, rel_tol=1e-2), "Elapsed time mismatch"
    assert elapsed > 0, "Elapsed time should be positive"
