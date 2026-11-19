import asyncio
import pytest
from tornado.queues import LifoQueue
from tornado.concurrent import Future
from tornado import gen
from queue import Empty

@pytest.mark.asyncio
async def test_lifo_order():
    """Items are retrieved in reverse order of insertion."""
    q = LifoQueue()
    q.put(1)
    q.put(2)
    q.put(3)
    assert await q.get() == 3
    assert await q.get() == 2
    assert await q.get() == 1

@pytest.mark.asyncio
async def test_maxsize_and_blocking():
    """Queue respects maxsize and blocks on put until space is available."""
    q = LifoQueue(maxsize=1)
    q.put(10)  # fills the queue
    assert q.full()
    # Start a coroutine that will put another item; it should block until we get.
    async def delayed_put():
        await q.put(20)
        return "done"
    task = asyncio.create_task(delayed_put())
    # Give the event loop a moment to run the put coroutine (it should block)
    await asyncio.sleep(0.1)
    assert not task.done()  # still blocked
    # Now get an item to free space
    assert await q.get() == 10
    # The put coroutine should now complete
    assert await task == "done"
    # Queue should contain the second item
    assert await q.get() == 20

def test_get_nowait_empty():
    """get_nowait raises Empty when the queue is empty."""
    q = LifoQueue()
    with pytest.raises(Empty):
        q.get_nowait()
