import pytest
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop

@pytest.mark.asyncio
async def test_semaphore_normal_acquire_release():
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
async def test_semaphore_release_too_many_times():
    sem = BoundedSemaphore(value=1)
    await sem.acquire()
    # Release once back to 1
    sem.release()
    # Now releasing again should raise ValueError
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()

@pytest.mark.asyncio
async def test_semaphore_acquire_blocks_and_wakes():
    sem = BoundedSemaphore(value=1)
    await sem.acquire()  # acquire the only permit
    # Start a coroutine that will wait for the semaphore
    async def waiter():
        await sem.acquire()
        return "acquired"
    future = gen.convert_yielded(waiter())
    # Ensure the future is not done yet (blocked)
    assert not future.done()
    # Release the semaphore to wake the waiter
    sem.release()
    # Now the future should complete
    result = await future
    assert result == "acquired"
    # The semaphore value should be back to 1
    assert sem._value == 1
