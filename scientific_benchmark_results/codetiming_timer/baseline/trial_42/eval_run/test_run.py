import pytest
from codetiming._timer import Timer, TimerError

def test_timer_start_initial_text_and_error():
    logs = []
    t = Timer(name="mytimer", initial_text="Timer {name} started", logger=logs.append)
    t.start()
    assert logs == ["Timer mytimer started"]
    assert t._start_time is not None
    with pytest.raises(TimerError):
        t.start()
