import asyncio
import pytest
from tornado.queues import LifoQueue
from tornado import gen
from tornado.concurrent import Future
from tornado import ioloop

# Test 1: Verify LIFO ordering of items
@pytest.mark.asyncio
async def test_lifo_ordering():
    q = LifoQueue()
    q.put(1)
    q.put(2)
    q.put(3)
    # Items should be retrieved in reverse order of insertion
    assert await q.get() == 3
    assert await q.get() == 2
    assert await q.get() == 1

# Test 2: Verify that get on an empty queue times out with asyncio.wait_for
@pytest.mark.asyncio
async def test_get_timeout_on_empty():
    q = LifoQueue()
    # Use asyncio.wait_for to enforce a timeout; expect asyncio.TimeoutError
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(q.get(), timeout=0.1)

# Test 3: Verify bounded queue behavior: put blocks until space is available
@pytest.mark.asyncio
async def test_bounded_queue_blocks_and_unblocks():
    q = LifoQueue(maxsize=1)
    q.put(42)  # queue now full

    async def delayed_get():
        # Wait a moment to ensure put is blocked
        await asyncio.sleep(0.05)
        return await q.get()

    # Schedule a get that will free space
    get_task = asyncio.create_task(delayed_get())

    # The following put should block until get_task retrieves the item
    # We use a timeout to ensure it does not return immediately
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(q.put(99), timeout=0.05)

    # Now the get_task should complete and free space
    result = await get_task
    assert result == 42

    # After the get, we can put another item without blocking
    await q.put(99)
    assert await q.get() == 99
