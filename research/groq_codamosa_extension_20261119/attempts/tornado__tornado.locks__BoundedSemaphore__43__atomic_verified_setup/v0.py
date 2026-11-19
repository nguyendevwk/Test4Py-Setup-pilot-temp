import pytest
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop

@pytest.mark.asyncio
async def test_normal_acquire_release():
    sem = BoundedSemaphore(value=2)
    # Acquire twice successfully
    await sem.acquire()
    await sem.acquire()
    # Value should be 0 now
    assert sem._value == 0
    # Release twice
    sem.release()
    sem.release()
    # Value should return to initial
    assert sem._value == 2

@pytest.mark.asyncio
async def test_release_too_many_times():
    sem = BoundedSemaphore(value=1)
    await sem.acquire()
    # Release once to restore to initial
    sem.release()
    # Now releasing again should raise ValueError
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()

@pytest.mark.asyncio
async def test_acquire_blocks_until_release():
    sem = BoundedSemaphore(value=1)
    await sem.acquire()
    # Start a coroutine that will acquire after release
    async def waiter():
        await sem.acquire()
        return "acquired"
    task = gen.Task(waiter)
    # Ensure the task is pending
    assert not task.done()
    # Release the semaphore to allow waiter to proceed
    sem.release()
    # Wait for the task to complete
    result = await task
    assert result == "acquired"
    # After waiter has acquired, semaphore value should be 0 again
    assert sem._value == 0
