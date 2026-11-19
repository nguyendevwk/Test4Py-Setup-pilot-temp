import asyncio
import pytest
from tornado.queues import LifoQueue


@pytest.mark.asyncio
async def test_lifo_order(tmp_path):
    """Items are retrieved in LIFO order."""
    q = LifoQueue()
    q.put(1)
    q.put(2)
    q.put(3)

    # The queue should return items in reverse order of insertion
    assert await q.get() == 3
    assert await q.get() == 2
    assert await q.get() == 1


@pytest.mark.asyncio
async def test_get_blocks_until_put(tmp_path):
    """`get` waits until an item is available."""
    q = LifoQueue()

    async def producer():
        await asyncio.sleep(0.1)
        q.put(42)

    async def consumer():
        return await q.get()

    # Run producer and consumer concurrently
    result = await asyncio.gather(producer(), consumer())
    # The consumer should receive the value put by the producer
    assert result[1] == 42


@pytest.mark.asyncio
async def test_get_after_close_raises(tmp_path):
    """After closing the queue, `get` raises RuntimeError."""
    q = LifoQueue()
    q.close()
    with pytest.raises(RuntimeError):
        await q.get()
