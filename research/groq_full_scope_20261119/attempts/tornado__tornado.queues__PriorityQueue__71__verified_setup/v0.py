import asyncio
import pytest
from tornado.queues import PriorityQueue
from tornado.concurrent import Future
from tornado.locks import Event

@pytest.mark.asyncio
async def test_priority_order():
    """Items are retrieved in ascending priority order."""
    q = PriorityQueue()
    # Put items with varying priorities
    await q.put((5, "low"))
    await q.put((1, "high"))
    await q.put((3, "medium"))
    # Retrieve items and check order
    first = await q.get()
    second = await q.get()
    third = await q.get()
    assert first == (1, "high")
    assert second == (3, "medium")
    assert third == (5, "low")
    # Queue should now be empty
    assert q.empty()

@pytest.mark.asyncio
async def test_maxsize_and_put_nowait():
    """put_nowait raises QueueFull when the queue reaches its maxsize."""
    maxsize = 2
    q = PriorityQueue(maxsize=maxsize)
    # Fill the queue to its maxsize
    await q.put_nowait((10, "item1"))
    await q.put_nowait((20, "item2"))
    # Next put_nowait should raise QueueFull
    with pytest.raises(asyncio.QueueFull):
        q.put_nowait((30, "item3"))
    # Ensure the queue still contains the two items
    assert q.qsize() == maxsize
    assert await q.get() == (10, "item1")
    assert await q.get() == (20, "item2")

@pytest.mark.asyncio
async def test_get_nowait_on_empty():
    """get_nowait raises QueueEmpty when the queue is empty."""
    q = PriorityQueue()
    # Queue is initially empty
    with pytest.raises(asyncio.QueueEmpty):
        q.get_nowait()
    # Put an item and then get it
    await q.put_nowait((0, "only"))
    assert q.qsize() == 1
    assert q.get_nowait() == (0, "only")
    # Queue should be empty again
    with pytest.raises(asyncio.QueueEmpty):
        q.get_nowait()
