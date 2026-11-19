import asyncio
import pytest
from tornado.queues import PriorityQueue


@pytest.mark.asyncio
async def test_priority_ordering():
    """Items are retrieved in ascending priority order."""
    q = PriorityQueue()
    q.put((5, "low"))
    q.put((1, "high"))
    q.put((3, "medium"))

    # qsize should reflect number of items
    assert q.qsize() == 3

    first = await q.get()
    assert first == (1, "high")
    second = await q.get()
    assert second == (3, "medium")
    third = await q.get()
    assert third == (5, "low")

    # After all items are consumed, queue is empty
    assert q.qsize() == 0


@pytest.mark.asyncio
async def test_equal_priority_stability():
    """Items with equal priority are returned in FIFO order."""
    q = PriorityQueue()
    q.put((2, "first"))
    q.put((2, "second"))
    q.put((2, "third"))

    assert q.qsize() == 3

    first = await q.get()
    second = await q.get()
    third = await q.get()

    assert first == (2, "first")
    assert second == (2, "second")
    assert third == (2, "third")


@pytest.mark.asyncio
async def test_put_after_get():
    """Queue can accept new items after some have been retrieved."""
    q = PriorityQueue()
    q.put((10, "a"))
    q.put((5, "b"))

    first = await q.get()
    assert first == (5, "b")
    assert q.qsize() == 1

    # Put a new item with higher priority
    q.put((1, "c"))
    assert q.qsize() == 2

    second = await q.get()
    assert second == (1, "c")
    third = await q.get()
    assert third == (10, "a")
