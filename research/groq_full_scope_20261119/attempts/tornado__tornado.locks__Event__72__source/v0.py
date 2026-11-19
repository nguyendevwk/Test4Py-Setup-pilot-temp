import asyncio
import datetime
import pytest
from tornado.locks import Event
from tornado.util import TimeoutError


@pytest.mark.asyncio
async def test_event_set_and_wait():
    """Event wakes all waiters when set."""
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

    # Set the event; both waiters should resume
    event.set()

    # Wait for both tasks to finish
    await asyncio.gather(task1, task2)

    # The order of completion is not guaranteed, but both names must be present
    assert set(results) == {"first", "second"}


@pytest.mark.asyncio
async def test_event_timeout_raises():
    """Event.wait raises TimeoutError when timeout expires."""
    event = Event()

    async def waiter():
        await event.wait(timeout=0.01)

    # The waiter should raise TimeoutError after the timeout
    with pytest.raises(TimeoutError):
        await waiter()


@pytest.mark.asyncio
async def test_event_clear_resets_behavior():
    """Clearing the event causes subsequent waiters to block again."""
    event = Event()
    event.set()  # Initially set

    # First waiter should not block
    await event.wait()

    # Clear the event
    event.clear()
    assert not event.is_set()

    # Start a waiter that should block until the event is set again
    waiter_task = asyncio.create_task(event.wait())

    # Give the loop a moment; the task should still be pending
    await asyncio.sleep(0.01)
    assert not waiter_task.done()

    # Set the event again; waiter should resume
    event.set()
    await waiter_task
    assert waiter_task.done()
