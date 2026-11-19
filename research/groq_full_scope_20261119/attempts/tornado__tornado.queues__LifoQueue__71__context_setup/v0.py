import pytest
import asyncio
from tornado.queues import LifoQueue

@pytest.mark.asyncio
async def test_lifo_order_and_empty_behavior(tmp_path):
    """Test that items are retrieved in LIFO order and that get on empty raises."""
    q = LifoQueue()
    # Put items in ascending order
    q.put(1)
    q.put(2)
    q.put(3)

    # Retrieve items; should be in reverse order
    assert await q.get() == 3
    assert await q.get() == 2
    assert await q.get() == 1

    # Queue should now be empty; get should raise QueueEmpty
    with pytest.raises(asyncio.QueueEmpty):
        await q.get()

@pytest.mark.asyncio
async def test_maxsize_and_blocking(tmp_path):
    """Test that maxsize limits the queue and that put blocks when full."""
    q = LifoQueue(maxsize=2)
    q.put('a')
    q.put('b')
    # Queue is now full; next put should block until an item is removed
    async def delayed_get():
        await asyncio.sleep(0.1)
        await q.get()  # remove one item

    # Run put in background; it should block until delayed_get runs
    put_task = asyncio.create_task(q.put('c'))
    await asyncio.sleep(0.05)  # give put_task time to block
    assert not put_task.done()  # still waiting because queue is full

    await delayed_get()
    await put_task  # now should complete

    # After unblocking, queue should contain two items
    assert q.qsize() == 2
    # LIFO order: 'c' was last put
    assert await q.get() == 'c'
    assert await q.get() == 'b'

@pytest.mark.asyncio
async def test_put_none_and_get_none(tmp_path):
    """Test that None can be stored and retrieved correctly."""
    q = LifoQueue()
    q.put(None)
    q.put(42)
    assert await q.get() == 42
    assert await q.get() is None
