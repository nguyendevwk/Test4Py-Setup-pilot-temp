import asyncio
import pytest
from tornado.queues import PriorityQueue


@pytest.mark.asyncio
async def test_priority_queue_ordering():
    """Normal behavior: items are retrieved in ascending priority order."""
    q = PriorityQueue()
    # Put items with varying priorities
    q.put((5, "low"))
    q.put((1, "high"))
    q.put((3, "medium"))
    # Retrieve items and assert order
    assert await q.get() == (1, "high")
    assert await q.get() == (3, "medium")
    assert await q.get() == (5, "low")
    # Queue should now be empty; get() will block, so we test that it raises
    # a TimeoutError when we try to get with a short timeout
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(q.get(), timeout=0.01)


@pytest.mark.asyncio
async def test_priority_queue_maxsize():
    """Boundary behavior: maxsize limits the number of items that can be queued."""
    q = PriorityQueue(maxsize=2)
    # Put two items; should succeed immediately
    q.put((2, "second"))
    q.put((1, "first"))
    # Queue is full; next put should block until an item is removed
    async def delayed_get():
        await asyncio.sleep(0.05)
        await q.get()
    # Start a task that will remove an item after a short delay
    asyncio.create_task(delayed_get())
    # Put third item; should block until the delayed_get removes one
    await asyncio.wait_for(q.put((3, "third")), timeout=0.2)
    # Now the queue should contain two items again
    assert await q.get() == (1, "first")
    assert await q.get() == (2, "second")
    # The third item should be next
    assert await q.get() == (3, "third")


def test_priority_queue_incomparable_items():
    """Error behavior: inserting items that cannot be compared raises TypeError."""
    q = PriorityQueue()
    # Insert a tuple with a comparable priority
    q.put((1, "valid"))
    # Attempt to insert a tuple where the priority is a string (non-comparable)
    with pytest.raises(TypeError):
        q.put(("invalid", "data"))
    # The queue should still contain the valid item
    assert q.get_nowait() == (1, "valid")
