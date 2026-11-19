import pytest
from codetiming import Timer, TimerError

def test_timer_start_stop_with_logger_and_timers(monkeypatch):
    # Capture logger output
    logs = []
    def logger(msg: str) -> None:
        logs.append(msg)

    # Fake time.perf_counter to control elapsed time
    counter = iter([1.0, 3.0])  # start at 1.0, stop at 3.0 → elapsed 2.0
    monkeypatch.setattr("codetiming._timer.time.perf_counter", lambda: next(counter))

    # Ensure timers are empty before test
    Timer.timers.clear()

    # Create timer with custom text and initial message
    t = Timer(
        name="test",
        text="Elapsed: {:0.4f}s",
        initial_text="Starting timer",
        logger=logger,
    )

    # Start the timer
    t.start()
    assert logs == ["Starting timer"], "Initial text should be logged on start"

    # Stop the timer and verify return value, last, and logger output
    elapsed = t.stop()
    assert elapsed == 2.0, "Elapsed time should be 2.0 seconds"
    assert t.last == 2.0, "Timer.last should be updated to elapsed time"
    assert logs[-1] == "Elapsed: 2.0000s", "Formatted elapsed time should be logged on stop"

    # Verify that the timer value was added to the class-level Timers
    assert Timer.timers["test"] == 2.0, "Timer value should be stored in Timers"
    assert Timer.timers.data["test"] == 2.0, "Timer data should reflect the elapsed time"
