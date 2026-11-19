import asyncio
import pytest
from tornado.queues import PriorityQueue
from tornado import queues

# Test 1: Normal priority ordering
@pytest.mark.asyncio
async def test_priority_ordering():
    q = PriorityQueue()
    q.put((2, "low"))
    q.put((0, "high"))
    q.put((1, "medium"))
    assert await q.get() == (0, "high")
    assert await q.get() == (1, "medium")
    assert await q.get() == (2, "low")

# Test 2: Equal priorities preserve tuple ordering
@pytest.mark.asyncio
async def test_equal_priority_order():
    q = PriorityQueue()
    q.put((5, "b"))
    q.put((5, "a"))
    q.put((5, "c"))
    # heapq compares the second element when first elements are equal
    assert await q.get() == (5, "a")
    assert await q.get() == (5, "b")
    assert await q.get() == (5, "c")

# Test 3: get_nowait raises Empty on empty queue
def test_get_nowait_empty():
    q = PriorityQueue()
    with pytest.raises(queues.Empty):
        q.get_nowait()
