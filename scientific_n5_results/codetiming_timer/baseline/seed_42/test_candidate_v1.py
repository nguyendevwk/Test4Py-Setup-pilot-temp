import math
import time

import pytest

from codetiming._timer import Timer


def test_timer_start_stop_logging_and_last():
    logs = []

    def logger(msg: str) -> None:
        logs.append(msg)

    t = Timer(name="test", initial_text=True, text="Elapsed: {:0.2f}s", logger=logger)

    t.start()
    assert logs[0] == "Timer test started"
    assert t._start_time is not None

    time.sleep(0.01)
    elapsed = t.stop()

    assert isinstance(elapsed, float)
    assert elapsed > 0
    assert t.last == pytest.approx(elapsed)
    assert t._start_time is None
    assert logs[1].startswith("Elapsed: ")
    assert not math.isnan(t.last)
