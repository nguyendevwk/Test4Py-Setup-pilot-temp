import pytest
import time
from codetiming._timer import Timer, TimerError

def test_timer_start_stop_and_logging():
    logs = []
    t = Timer(name='perf', text='Elapsed: {:0.4f}s', initial_text='Starting timer', logger=logs.append)

    # Start the timer and check initial log
    t.start()
    assert logs[0] == 'Starting timer'

    # Starting again should raise
    with pytest.raises(TimerError, match="Timer is running"):
        t.start()

    # Stop after a short delay
    time.sleep(0.01)
    elapsed = t.stop()
    assert isinstance(elapsed, float)
    assert elapsed > 0
    assert logs[1].startswith('Elapsed:')

    # Timer state and collection updated
    assert t.last == elapsed
    assert t.timers.total('perf') == pytest.approx(elapsed)

    # Stopping again should raise
    with pytest.raises(TimerError, match="Timer is not running"):
        t.stop()

    # Context manager usage
    logs2 = []
    with Timer(name='ctx', text='Ctx: {:0.4f}s', initial_text='Ctx start', logger=logs2.append) as ctx:
        time.sleep(0.005)
    assert logs2[0] == 'Ctx start'
    assert logs2[1].startswith('Ctx:')
    assert ctx.last > 0
    assert ctx.timers.total('ctx') == pytest.approx(ctx.last)
