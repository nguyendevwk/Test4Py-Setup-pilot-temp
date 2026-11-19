import asyncio
import pytest
from tornado.queues import PriorityQueue


@pytest.mark.asyncio
async def test_priority_order():
    """Items are retrieved in ascending priority order."""
    q = PriorityQueue()
    q.put((2, "medium"))
    q.put((0, "high"))
    q.put((10, "low"))

    first = await q.get()
    second = await q.get()
    third = await q.get()

    assert first == (0, "high")
    assert second == (2, "medium")
    assert third == (10, "low")


@pytest.mark.asyncio
async def test_maxsize_blocks():
    """Putting into a full queue blocks until space is available."""
    q = PriorityQueue(maxsize=1)
    q.put((1, "only"))

    async def try_put():
        # This put should block because the queue is full.
        await q.put((2, "blocked"))

    # Run the put with a short timeout; it should raise a TimeoutError.
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(try_put(), timeout=0.1)

    # After removing the item, the blocked put should succeed.
    await q.get()
    await q.put((2, "blocked"))  # should not block now
    assert await q.get() == (2, "blocked")


def test_internal_heap_property():
    """The underlying list is maintained as a heap."""
    q = PriorityQueue()
    q.put((5, "five"))
    q.put((1, "one"))
    q.put((3, "three"))

    # The smallest priority should be at index 0 of the heap.
    assert q._queue[0][0] == 1
    # The heap property ensures that every parent is <= its children.
    heap = q._queue
    for i in range(len(heap)):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(heap):
            assert heap[i][0] <= heap[left][0]
        if right < len(heap):
            assert heap[i][0] <= heap[right][0]
