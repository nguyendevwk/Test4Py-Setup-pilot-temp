import pytest
from codetiming._timer import Timer


def test_timer_start_logs_initial_text():
    """Timer.start should log the correct initial text based on the `initial_text` setting."""
    logs: list[str] = []

    def logger(msg: str) -> None:
        logs.append(msg)

    # Case 1: initial_text is a formatted string
    timer1 = Timer(name="mytimer", initial_text="Starting {name}", logger=logger)
    timer1.start()
    assert logs == ["Starting mytimer"]
    logs.clear()

    # Case 2: initial_text is True, triggers default message
    timer2 = Timer(name="mytimer", initial_text=True, logger=logger)
    timer2.start()
    assert logs == ["Timer mytimer started"]
    logs.clear()

    # Case 3: initial_text is False, no message should be logged
    timer3 = Timer(name="mytimer", initial_text=False, logger=logger)
    timer3.start()
    assert logs == []
