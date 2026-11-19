import pytest
from codetiming._timer import Timer, TimerError


def test_timer_behavior(monkeypatch):
    # Capture logger output
    logged_messages = []

    def fake_logger(msg: str) -> None:
        logged_messages.append(msg)

    # Dummy Timers that records add calls
    class DummyTimers:
        def __init__(self):
            self.calls = []

        def add(self, name, elapsed):
            self.calls.append((name, elapsed))

    dummy_timers = DummyTimers()
    monkeypatch.setattr(Timer, "timers", dummy_timers, raising=False)

    # Mock perf_counter to produce deterministic elapsed time
    counter = -5.0

    def fake_perf_counter():
        nonlocal counter
        counter += 5.0
        return counter

    monkeypatch.setattr("codetiming._timer.time.perf_counter", fake_perf_counter)

    # Create timer with initial_text=True and a name
    timer = Timer(name="test", initial_text=True, logger=fake_logger)

    # Start the timer – should log the initial message
    timer.start()
    assert logged_messages[0] == "Timer test started"

    # Stop the timer – should log the elapsed time and return it
    elapsed = timer.stop()
    assert elapsed == 5.0
    assert logged_messages[1] == "Elapsed time: 5.0000 seconds"

    # Timers.add should have been called with the correct arguments
    assert dummy_timers.calls == [("test", 5.0)]

    # Starting an already running timer should raise TimerError
    timer2 = Timer(name="t2", logger=fake_logger)
    timer2.start()
    with pytest.raises(TimerError, match="Timer is running"):
        timer2.start()
    timer2.stop()

    # Stopping a timer that hasn't been started should raise TimerError
    timer3 = Timer(name="t3", logger=fake_logger)
    with pytest.raises(TimerError, match="Timer is not running"):
        timer3.stop()
