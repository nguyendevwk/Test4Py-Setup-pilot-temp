import asyncio
import datetime
import pytest
from tornado.locks import Event
from tornado.util import TimeoutError

@pytest.mark.asyncio
async def test_event_set_and_wait(tmp_path):
    """Test that waiters are awakened when the event is set."""
    event = Event()
    results = []

    async def waiter(name):
        await event.wait()
        results.append(name)

    # Start two waiters
    task1 = asyncio.create_task(waiter("first"))
    task2 = asyncio.create_task(waiter("second"))

    # Give the event loop a moment to schedule the waiters
    await asyncio.sleep(0.01)

    # Set the event; both waiters should resume
    event.set()

    await asyncio.gather(task1, task2)

    # Order of completion is not guaranteed, but both names must be present
    assert set(results) == {"first", "second"}
    # After being set, subsequent waits should not block
    await event.wait()
    await event.wait()


@pytest.mark.asyncio
async def test_event_clear_and_wait(tmp_path):
    """Test that clearing the event causes waiters to block until set again."""
    event = Event()
    event.set()  # Initially set

    async def waiter():
        await event.wait()
        return "done"

    # Clear the event; waiter should block
    event.clear()
    task = asyncio.create_task(waiter())
    await asyncio.sleep(0.01)  # Ensure waiter is waiting
    assert not task.done()

    # Set the event again; waiter should resume
    event.set()
    result = await task
    assert result == "done"


@pytest.mark.asyncio
async def test_event_timeout(tmp_path):
    """Test that wait raises TimeoutError when a timeout is exceeded."""
    event = Event()

    async def waiter():
        await event.wait(timeout=0.05)

    with pytest.raises(TimeoutError):
        await waiter()
