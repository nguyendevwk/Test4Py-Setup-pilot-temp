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
    # Release once
    sem.release()
    assert sem._value == 1
    # Release second time
    sem.release()
    assert sem._value == 2
    # Acquire again to ensure semaphore works after releases
    await sem.acquire()
    assert sem._value == 1

@pytest.mark.asyncio
async def test_release_too_many_times_raises():
    sem = BoundedSemaphore(value=1)
    await sem.acquire()
    # Release once to return to initial value
    sem.release()
    # Now releasing again should raise ValueError
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()

@pytest.mark.asyncio
async def test_acquire_blocks_when_exhausted():
    sem = BoundedSemaphore(value=1)
    await sem.acquire()
    # Start a coroutine that will try to acquire and should block
    async def try_acquire():
        await sem.acquire()
        return "acquired"
    future = ioloop.IOLoop.current().run_in_executor(None, lambda: None)  # dummy to keep loop running
    task = gen.Task(try_acquire)
    # Ensure task is pending (not finished)
    assert not task.done()
    # Release semaphore to unblock
    sem.release()
    result = await task
    assert result == "acquired"
