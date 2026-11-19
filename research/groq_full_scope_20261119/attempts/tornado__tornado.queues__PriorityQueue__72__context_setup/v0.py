import asyncio
import pytest
from tornado.queues import PriorityQueue


@pytest.mark.asyncio
async def test_priority_queue_order_and_size():
    """Normal behavior: items are retrieved in ascending priority order."""
    q = PriorityQueue()
    # Put items with varying priorities
    q.put((5, "low"))
    q.put((1, "high"))
    q.put((3, "medium"))
    # Queue size should reflect number of items
    assert q.qsize() == 3
    # Retrieve items and check order
    assert await q.get() == (1, "high")
    assert await q.get() == (3, "medium")
    assert await q.get() == (5, "low")
    # After all items are consumed, queue should be empty
    assert q.empty()


@pytest.mark.asyncio
async def test_priority_queue_with_equal_priorities():
    """Boundary case: items with equal priority are ordered by insertion order."""
    q = PriorityQueue()
    # Insert items with the same priority but different data
    q.put((2, "first"))
    q.put((2, "second"))
    q.put((2, "third"))
    # Since heapq compares the second element when priorities are equal,
    # the items will be ordered lexicographically by the data string.
    # "first" < "second" < "third" alphabetically.
    assert await q.get() == (2, "first")
    assert await q.get() == (2, "second")
    assert await q.get() == (2, "third")


@pytest.mark.asyncio
async def test_priority_queue_type_error_on_uncomparable_items():
    """Error behavior: retrieving items that cannot be compared raises TypeError."""
    q = PriorityQueue()
    # Insert items where the second element is not comparable (e.g., a set)
    q.put((1, {"a"}))
    q.put((1, {"b"}))
    # The heap will try to compare the second elements when priorities are equal,
    # which will raise a TypeError because sets are not orderable.
    with pytest.raises(TypeError):
        await q.get()
