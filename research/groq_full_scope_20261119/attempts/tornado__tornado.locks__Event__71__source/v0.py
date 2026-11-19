import asyncio
import datetime

import pytest
from tornado.locks import Event
from tornado.util import TimeoutError


@pytest.mark.asyncio
async def test_event_set_and_wait(tmp_path):
    """Event wakes all waiters when set and stays set until cleared."""
    event = Event()
    results = []

    async def waiter(name):
        await event.wait()
        results.append(name)

    # Start two waiters that will block until event is set
    task1 = asyncio.create_task(waiter("first"))
    task2 = asyncio.create_task(waiter("second"))

    # Give the event loop a moment to schedule the waiters
    await asyncio.sleep(0.01)

    # The event is not set yet, so no results should be recorded
    assert results == []

    # Set the event; both waiters should resume
    event.set()
    await asyncio.sleep(0.01)

    # Both waiters should have appended their names
    assert set(results) == {"first", "second"}

    # Subsequent wait should not block
    await event.wait()
    # No new results appended
    assert set(results) == {"first", "second"}

    # Clean up tasks
    task1.cancel()
    task2.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task1
    with pytest.raises(asyncio.CancelledError):
        await task2


@pytest.mark.asyncio
async def test_event_timeout(tmp_path):
    """Event.wait raises TimeoutError when a timeout is exceeded."""
    event = Event()

    async def waiter():
        await event.wait(timeout=0.01)

    # The waiter should raise TimeoutError after the timeout
    with pytest.raises(TimeoutError):
        await waiter()


@pytest.mark.asyncio
async def test_event_clear_and_reuse(tmp_path):
    """Event can be cleared and reused, resetting its state."""
    event = Event()
    event.set()
    assert event.is_set() is True

    # Clear the event
    event.clear()
    assert event.is_set() is False

    # After clearing, a waiter should block until set again
    async def waiter():
        await event.wait()

    task = asyncio.create_task(waiter())
    await asyncio.sleep(0.01)
    assert not task.done()

    # Set again to release the waiter
    event.set()
    await asyncio.sleep(0.01)
    assert task.done()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
