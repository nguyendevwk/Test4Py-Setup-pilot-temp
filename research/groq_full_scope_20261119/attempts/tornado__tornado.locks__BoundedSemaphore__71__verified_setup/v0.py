import pytest
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop
import asyncio

@pytest.mark.asyncio
async def test_bounded_semaphore_normal_acquire_release():
    """Acquire and release within bounds should succeed."""
    sem = BoundedSemaphore(value=2)
    # Acquire twice, should succeed
    await sem.acquire()
    await sem.acquire()
    # Now semaphore value should be 0
    assert sem._value == 0
    # Release twice, should bring back to initial value
    sem.release()
    sem.release()
    assert sem._value == 2
    # Further acquire should block until release
    async def acquire_task():
        await sem.acquire()
        return "acquired"
    task = asyncio.create_task(acquire_task())
    await asyncio.sleep(0.1)
    assert not task.done()
    sem.release()
    result = await task
    assert result == "acquired"

@pytest.mark.asyncio
async def test_bounded_semaphore_release_too_many_times():
    """Releasing more times than the initial value raises ValueError."""
    sem = BoundedSemaphore(value=1)
    await sem.acquire()
    # Release once to return to initial value
    sem.release()
    # Now releasing again should raise ValueError
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()

@pytest.mark.asyncio
async def test_bounded_semaphore_initial_value_boundary():
    """Semaphore should not allow value to exceed initial value."""
    sem = BoundedSemaphore(value=3)
    # Acquire all permits
    await sem.acquire()
    await sem.acquire()
    await sem.acquire()
    assert sem._value == 0
    # Release all permits
    sem.release()
    sem.release()
    sem.release()
    assert sem._value == 3
    # Attempt to release one more should raise ValueError
    with pytest.raises(ValueError):
        sem.release()
