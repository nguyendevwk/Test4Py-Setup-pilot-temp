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

    # Start two waiters that will block until the event is set
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

    # Subsequent waits should not block because the event remains set
    await event.wait()
    await event.wait()
    # No new entries should be added
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
    """Event.wait raises TimeoutError when a timeout expires."""
    event = Event()

    async def waiter():
        await event.wait(timeout=0.01)

    # The event is not set; the waiter should timeout
    with pytest.raises(TimeoutError):
        await waiter()


@pytest.mark.asyncio
async def test_event_clear_and_rewait(tmp_path):
    """Event.clear resets the flag so subsequent waits block again."""
    event = Event()
    event.set()
    assert event.is_set()

    # Clear the event
    event.clear()
    assert not event.is_set()

    # A waiter should now block until the event is set again
    async def waiter():
        await event.wait()
        return "done"

    task = asyncio.create_task(waiter())
    await asyncio.sleep(0.01)
    assert not task.done()

    # Set the event again; waiter should resume
    event.set()
    result = await task
    assert result == "done"
