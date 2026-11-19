import time

import pytest

from codetiming._timer import Timer


def test_timer_stop_records_elapsed_and_updates_timers_and_logger():
    log = []

    t = Timer(name="demo", text="Elapsed: {:0.4f}s", logger=lambda msg: log.append(msg))
    t.start()
    time.sleep(0.01)
    elapsed = t.stop()

    # elapsed time should be positive
    assert elapsed > 0

    # logger should have received one message with the elapsed time
    assert len(log) == 1
    assert log[0].startswith("Elapsed:")
    assert log[0].endswith("s")
    # extracted numeric part matches elapsed within tolerance
    logged_value = float(log[0].split(": ")[1][:-1])
    assert logged_value == pytest.approx(elapsed, rel=1e-2)

    # Timer.timers should record the elapsed time under the given name
    assert Timer.timers.total("demo") == pytest.approx(elapsed, rel=1e-2)

    # internal state should be reset after stop
    assert t._start_time is None
