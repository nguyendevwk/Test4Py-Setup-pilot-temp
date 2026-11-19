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


@pytest.mark.asyncio
async def test_event_timeout(tmp_path):
    """wait() raises TimeoutError when a timeout is supplied and the event is not set."""
    event = Event()

    # Use a very short timeout to trigger the error
    with pytest.raises(TimeoutError):
        await event.wait(timeout=0.01)

    # After the timeout, the event should still be clear
    assert not event.is_set()


@pytest.mark.asyncio
async def test_event_clear_and_rewait(tmp_path):
    """clear() resets the event so that subsequent wait() blocks again."""
    event = Event()
    event.set()
    assert event.is_set()

    # Clear the event
    event.clear()
    assert not event.is_set()

    # Start a waiter that should block until the event is set again
    waiter_task = asyncio.create_task(event.wait())

    # Give the loop a moment; the waiter should not be done yet
    await asyncio.sleep(0.01)
    assert not waiter_task.done()

    # Set the event again; the waiter should resume
    event.set()
    await asyncio.sleep(0.01)
    assert waiter_task.done()
