import pytest
from tornado.locks import BoundedSemaphore
from tornado import gen, ioloop

# Test 1: Normal acquire and release flow
def test_bounded_semaphore_basic():
    sem = BoundedSemaphore(value=2)
    # Acquire twice successfully
    sem.acquire()
    sem.acquire()
    # Value should be 0 now
    assert sem._value == 0
    # Release twice, value back to 2
    sem.release()
    sem.release()
    assert sem._value == 2

# Test 2: Release too many times raises ValueError
def test_bounded_semaphore_over_release():
    sem = BoundedSemaphore(value=1)
    sem.acquire()
    sem.release()
    # Now value is back to 1; next release should raise
    with pytest.raises(ValueError, match="Semaphore released too many times"):
        sem.release()

# Test 3: Asynchronous acquire with timeout
@pytest.mark.asyncio
async def test_bounded_semaphore_async_acquire():
    sem = BoundedSemaphore(value=1)
    # Acquire synchronously
    sem.acquire()
    # Attempt async acquire with timeout; should raise TimeoutError
    async def try_acquire():
        await gen.with_timeout(0.01, sem.acquire)
    with pytest.raises(TimeoutError):
        await try_acquire()
    # Release and then async acquire should succeed
    sem.release()
    await sem.acquire()
    assert sem._value == 0
