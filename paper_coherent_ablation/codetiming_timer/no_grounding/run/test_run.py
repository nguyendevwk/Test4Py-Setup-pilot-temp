import math
import re
import time

import pytest

from codetiming._timer import Timer, TimerError


def test_timer_start_and_stop_logs_initial_and_elapsed_text():
    """Verify that a Timer logs the initial text when started and the elapsed time when stopped."""
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    # Create a timer with a name and a custom initial text
    t = Timer(name="foo", initial_text="Starting foo timer", logger=logger)

    # Start the timer – should log the initial text
    t.start()
    assert logs == ["Starting foo timer"], f"Unexpected logs after start: {logs}"

    # Wait a short time to produce a measurable elapsed time
    time.sleep(0.01)

    # Stop the timer – should log the elapsed time
    elapsed = t.stop()
    assert not math.isnan(elapsed), "Elapsed time should be a number, not NaN"

    # The second log entry should contain the formatted elapsed time
    assert len(logs) == 2, f"Expected two log entries, got {len(logs)}"
    elapsed_log = logs[1]
    # The default text format is "Elapsed time: {:0.4f} seconds"
    assert re.match(r"Elapsed time: \d+\.\d{4} seconds", elapsed_log), (
        f"Elapsed log does not match expected format: {elapsed_log}"
    )

    # Starting the timer again without stopping should raise TimerError
    with pytest.raises(TimerError, match="Timer is running"):
        t.start()
