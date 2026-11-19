import asyncio
import pytest
from tornado.queues import LifoQueue
from tornado.queues import QueueEmpty

@pytest.mark.asyncio
async def test_lifo_behavior():
    q = LifoQueue()
    q.put(10)
    q.put(20)
    q.put(30)
    # LIFO: last in first out
    assert await q.get() == 30
    assert await q.get() == 20
    assert await q.get() == 10

@pytest.mark.asyncio
async def test_get_nowait_on_empty_raises():
    q = LifoQueue()
    with pytest.raises(QueueEmpty):
        q.get_nowait()

@pytest.mark.asyncio
async def test_put_and_get_nowait():
    q = LifoQueue()
    q.put("a")
    q.put("b")
    # get_nowait should return the most recently put item
    assert q.get_nowait() == "b"
    assert q.get_nowait() == "a"
