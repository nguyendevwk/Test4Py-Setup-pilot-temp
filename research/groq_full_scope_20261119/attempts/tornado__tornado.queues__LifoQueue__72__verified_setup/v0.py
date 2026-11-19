import pytest
import asyncio
from tornado.queues import LifoQueue
from tornado import gen

@pytest.mark.asyncio
async def test_lifo_order():
    """Items are retrieved in LIFO order."""
    q = LifoQueue()
    q.put(1)
    q.put(2)
    q.put(3)
    assert await q.get() == 3
    assert await q.get() == 2
    assert await q.get() == 1

@pytest.mark.asyncio
async def test_maxsize_behavior():
    """Queue respects the maxsize limit."""
    q = LifoQueue(maxsize=2)
    q.put_nowait(10)
    q.put_nowait(20)
    with pytest.raises(ValueError):
        q.put_nowait(30)  # exceeds maxsize
    # Ensure we can still get the two items
    assert await q.get() == 20
    assert await q.get() == 10

@pytest.mark.asyncio
async def test_get_nowait_empty():
    """get_nowait raises Empty when queue is empty."""
    q = LifoQueue()
    with pytest.raises(asyncio.QueueEmpty):
        q.get_nowait()
